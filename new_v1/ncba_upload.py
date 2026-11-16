"""Upload converted GameChanger stats to the NCBA stats portal (CollClubSports).

CollClubSports doesn't publish an API, but its admin site
(admin.collclubsports.com) is a single-page app backed by a JSON API under
/api. This module calls the same endpoints the site's "Game Stats" form uses,
logged in as you, so the result is the same as typing every player's line in
by hand: one offensive and one pitching entry per player per game.

The API is undocumented. Endpoints and field names come from the admin site's
own JavaScript (js/admin.min.js, v1.9.5), so if CollClubSports changes the site
this module may need updating.
"""

import argparse
import csv
import difflib
import getpass
import json
import os
import re
import ssl
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://admin.collclubsports.com/api"
TEAM_MANAGER_ROLE = 4
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

# converted CSV column -> CollClubSports offensive stat field
HITTING_FIELDS = {
    "AB": "ab", "R": "r", "H": "h", "2B": "twob", "3B": "threeb", "HR": "hr",
    "RBI": "rbi", "BB": "bb", "IBB": "ibb", "SO": "so", "SB": "sb", "CS": "cs",
    "SAC_F": "sacf", "SAC_B": "sacb", "HBP": "hbp",
}
# pitching columns shown as checkboxes on the site
PITCHING_FLAGS = {
    "Started": "gamestart", "W": "w", "L": "l", "CG": "cg", "SHO": "sho", "SV": "sv",
}
# pitching columns entered as numbers (IP is handled separately)
PITCHING_COUNTS = {
    "SVO": "svo", "H": "h", "R": "r", "ER": "er", "HR": "hr", "HBP": "hbp",
    "BB": "bb", "IBB": "ibb", "SO": "so", "BK": "bk", "WP": "wp", "PK": "pk",
}


class CCSError(Exception):
    pass


def encode_form(data, prefix=""):
    """Flatten a dict the way jQuery's $.param does (statsdetails[ab]=3),
    which is the format the site's API expects."""
    pairs = []
    for key, value in data.items():
        name = f"{prefix}[{key}]" if prefix else key
        if isinstance(value, dict):
            pairs.extend(encode_form(value, name))
        elif isinstance(value, bool):
            pairs.append((name, "true" if value else "false"))
        elif value is None:
            pairs.append((name, ""))
        else:
            pairs.append((name, str(value)))
    return pairs


def _items(payload):
    """List endpoints return either a bare list or {"items": [...], "total": n}."""
    if isinstance(payload, dict):
        return payload.get("items") or payload.get("Items") or []
    return payload or []


class CCSClient:
    def __init__(self, base_url=API_BASE):
        self.base_url = base_url
        self.token = None

    def _request(self, method, path, data=None):
        headers = {"Accept": "application/json", "User-Agent": "Mozilla/5.0 (gc-stats-scraper)"}
        body = None
        if data is not None:
            body = urllib.parse.urlencode(encode_form(data)).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        request = urllib.request.Request(self.base_url + path, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            try:
                parsed = json.loads(detail)
                if isinstance(parsed, dict):
                    detail = parsed.get("Message") or parsed.get("error_description") or detail
            except ValueError:
                pass
            raise CCSError(f"{method} {path} returned HTTP {e.code}: {detail}") from None
        except urllib.error.URLError as e:
            hint = ""
            if isinstance(e.reason, ssl.SSLCertVerificationError):
                hint = " (on macOS with the python.org installer, run 'Install Certificates.command')"
            raise CCSError(f"could not reach {self.base_url}: {e.reason}{hint}") from None
        return json.loads(raw) if raw.strip() else None

    def login(self, email, password):
        try:
            # field names as sent by the site's AuthenticationService.Login
            session = self._request("POST", "/login", {"username": email, "password": password, "leagueid": None})
        except CCSError as e:
            raise CCSError(f"login failed, check CCS_EMAIL and CCS_PASSWORD ({e})") from None
        if not session or not session.get("accesstoken"):
            raise CCSError("login failed: no access token in the response")
        self.token = session["accesstoken"]
        return session

    def account_roles(self):
        return _items(self._request("GET", "/v1/account/role"))

    def current_season(self, league_id):
        return self._request("GET", f"/v1/league/{league_id}/season/current")

    def weeks(self, league_id, season_id):
        return _items(self._request("GET", f"/v1/league/{league_id}/season/{season_id}/week"))

    def games(self, season_id, team_id):
        games, offset = [], 0
        while True:
            page = self._request(
                "GET",
                f"/v1/season/{season_id}/game?weekid=null&conferenceid=null&teamid={team_id}"
                f"&count=100&offset={offset}",
            )
            batch = _items(page)
            games.extend(batch)
            total = page.get("total") if isinstance(page, dict) else None
            if not batch or total is None or len(games) >= total:
                return games
            offset += len(batch)

    def roster(self, season_id, team_id):
        return _items(self._request("GET", f"/v1/season/{season_id}/team/{team_id}/player?count=500"))

    def _stats_path(self, kind, team_id, game_id):
        return f"/v1/team/{team_id}/game/{game_id}/stats/baseball/{kind}"

    def get_stats(self, kind, team_id, game_id):
        return _items(self._request("GET", self._stats_path(kind, team_id, game_id)))

    def save_stats(self, kind, team_id, game_id, body, stats_id=None):
        path = self._stats_path(kind, team_id, game_id)
        if stats_id:
            return self._request("PUT", f"{path}/{stats_id}", body)
        return self._request("POST", path, body)


def read_converted_csv(path):
    """Read the hitting and pitching tables from a CSV written by main.py.
    Returns two dicts of {"Last, First": {column: value}}."""
    hitters, pitchers = {}, {}
    table = header = None
    with open(path, newline="") as f:
        for row in csv.reader(f):
            if len(row) <= 1:  # blank separator or a section title
                table = None
                continue
            if row[0] == "Name":
                header = row
                table = pitchers if "Started" in row else hitters
                continue
            if table is not None:
                table[row[0]] = dict(zip(header, row))
    return hitters, pitchers


def _count(value):
    """'3' -> 3. Blanks and 'N/A' (stats GameChanger doesn't export) -> 0."""
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def _innings(value, player):
    """Innings pitched in baseball notation (5.2 means 5 2/3), as the site expects."""
    value = (value or "").strip()
    if value in ("", "N/A", "-"):
        return "0"
    if not re.fullmatch(r"\d+(\.[0-2])?", value):
        raise ValueError(f"{player}: IP should look like 5, 5.1 or 5.2, got {value!r}")
    return value


def hitting_details(stats):
    return {field: _count(stats.get(column)) for column, field in HITTING_FIELDS.items()}


def pitching_details(player, stats):
    details = {field: _count(stats.get(column)) > 0 for column, field in PITCHING_FLAGS.items()}
    details["ip"] = _innings(stats.get("IP"), player)
    details.update({field: _count(stats.get(column)) for column, field in PITCHING_COUNTS.items()})
    return details


def _normalize(name):
    name = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z]", "", name.lower())


def match_players(names, roster):
    """Match "Last, First" names from the CSV to players on the NCBA roster.
    Returns ({name: player}, [names matched loosely], [names not found])."""
    by_key = {}
    for player in roster:
        by_key.setdefault((_normalize(player.get("lastname")), _normalize(player.get("firstname"))), player)
    labels = {f"{last} {first}": (last, first) for last, first in by_key}

    matches, loose, missing, claimed = {}, [], [], set()
    for name in names:
        last, _, first = name.partition(",")
        key = (_normalize(last), _normalize(first))
        player = by_key.get(key)

        if not player:
            # same last name and first initial (Mike vs Michael), if that's unique
            same_last = [p for (l, f), p in by_key.items() if l == key[0] and f[:1] == key[1][:1]]
            if len(same_last) == 1:
                player = same_last[0]
            else:
                close = difflib.get_close_matches(f"{key[0]} {key[1]}", labels, n=1, cutoff=0.85)
                player = by_key[labels[close[0]]] if close else None
            if player:
                loose.append(name)

        if player and player["playerid"] not in claimed:
            matches[name] = player
            claimed.add(player["playerid"])
        else:
            missing.append(name)
    return matches, loose, missing


def _team_name(game, side):
    team = game.get(side)
    return (team or {}).get("teamname") or game.get(f"{side}writein") or "TBD"


def _is_home(game, team_id):
    return ((game.get("hometeam") or {}).get("teamid") or "").lower() == team_id.lower()


def _week(game, weeks):
    return weeks.get(game.get("weekid")) or game.get("week") or {}


def _week_name(week):
    """Weeks only have a number; the site displays them as "Week <ordinalnumber>"."""
    if week.get("weekname"):
        return week["weekname"]
    if week.get("ordinalnumber") is not None:
        return f"Week {week['ordinalnumber']}"
    return "Unknown week"


def describe_game(game, weeks):
    wk = _week(game, weeks)
    week = _week_name(wk)
    start = (wk.get("startdate") or "")[:10].split("-")
    if len(start) == 3:
        week += f" (starting {int(start[1])}/{int(start[2])})"
    visitor, home = _team_name(game, "visitingteam"), _team_name(game, "hometeam")
    vs, hs = game.get("visitingteamscore"), game.get("hometeamscore")
    if vs is not None and hs is not None:
        visitor, home = f"{visitor} ({vs})", f"{home} ({hs})"
    return f"{week}, {game.get('gamename') or 'Game'}: {visitor} vs {home}"


def _numbers(text):
    return re.findall(r"\d+", text or "")


def filter_games(games, weeks, team_id, opponent=None, week=None, game_name=None):
    def keep(game):
        if opponent:
            other = _team_name(game, "visitingteam" if _is_home(game, team_id) else "hometeam")
            if opponent.lower() not in other.lower():
                return False
        if week:
            name = _week_name(_week(game, weeks))
            if _numbers(week) != _numbers(name)[:1] and week.lower() != name.lower():
                return False
        if game_name and _numbers(game_name) != _numbers(game.get("gamename"))[:1]:
            return False
        return True

    def order(game):
        return (_week(game, weeks).get("startdate") or "", game.get("gamename") or "")

    return sorted(filter(keep, games), key=order)


def choose(items, describe, what):
    if not items:
        raise SystemExit(f"No {what} matched.")
    if len(items) == 1:
        return items[0]
    for i, item in enumerate(items, 1):
        print(f"  [{i}] {describe(item)}")
    if not sys.stdin.isatty():
        raise SystemExit(f"{len(items)} {what}s match. Narrow it down with the filter options.")
    while True:
        answer = input(f"Choose a {what} [1-{len(items)}]: ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(items):
            return items[int(answer) - 1]


def _role_id(role):
    """The API returns roles as a bare number; the site's cookie stores them as {"id": n, ...}."""
    return role.get("id") if isinstance(role, dict) else role


def pick_team(client, session):
    """The (league id, team id, label) this account manages. Prompts if there are several."""
    teams = []
    for role in client.account_roles():
        league = role.get("league") or {}
        if _role_id(role.get("role")) == TEAM_MANAGER_ROLE and league.get("leagueid") and role.get("entityid"):
            label = f"{league.get('leaguealias') or league.get('leaguename', '')} - {role.get('entityname', '')}"
            teams.append((league["leagueid"], role["entityid"], label))

    if not teams and _role_id(session.get("role")) == TEAM_MANAGER_ROLE:
        teams.append((session["leagueid"], session["entityid"], "your team"))
    if not teams:
        raise CCSError("this account isn't a Team Manager for any team, so it can't enter stats")
    return choose(teams, lambda t: t[2], "team")


def _stats_body(player, game_id, details, existing):
    if existing:
        # same as the site: send back the saved entry with the new numbers
        body = {k: v for k, v in existing.items() if not isinstance(v, (dict, list))}
    else:
        body = {
            "playerid": player["playerid"],
            "firstname": player.get("firstname"),
            "middlename": player.get("middlename"),
            "lastname": player.get("lastname"),
            "gameid": game_id,
            "isnew": True,
        }
    body["hasplayed"] = True
    body["statsdetails"] = details
    return body


def load_credentials():
    values = {}
    try:
        with open(ENV_PATH) as f:
            for line in f:
                key, sep, value = line.strip().partition("=")
                if sep and not key.startswith("#"):
                    values[key.strip()] = value.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass

    email = os.environ.get("CCS_EMAIL") or values.get("CCS_EMAIL")
    password = os.environ.get("CCS_PASSWORD") or values.get("CCS_PASSWORD")
    if (not email or not password) and not sys.stdin.isatty():
        raise SystemExit(f"Set CCS_EMAIL and CCS_PASSWORD in {ENV_PATH}")
    if not email:
        email = input("CollClubSports email: ").strip()
    if not password:
        password = getpass.getpass("CollClubSports password: ")
    return email, password


def upload(hitters, pitchers, game_id=None, opponent=None, week=None, game_name=None,
           dry_run=False, assume_yes=False, client=None):
    """Upload one game's stats. hitters/pitchers are {"Last, First": {column: value}}
    using the converted CSV's column names (see main.stat_tables / read_converted_csv)."""
    if not hitters and not pitchers:
        raise SystemExit("No player stats to upload.")
    # convert everything up front so a bad value stops us before anything is sent
    try:
        hitting = {name: hitting_details(stats) for name, stats in hitters.items()}
        pitching = {name: pitching_details(name, stats) for name, stats in pitchers.items()}
    except ValueError as e:
        raise SystemExit(f"Bad stat value: {e}")

    client = client or CCSClient()
    print("\nLogging in to CollClubSports...")
    session = client.login(*load_credentials())
    league_id, team_id, team_label = pick_team(client, session)
    season = client.current_season(league_id)
    season_id = season["seasonid"]
    weeks = {w["weekid"]: w for w in client.weeks(league_id, season_id)}

    games = client.games(season_id, team_id)
    if game_id:
        candidates = [g for g in games if g.get("gameid", "").lower() == game_id.lower()]
    else:
        candidates = filter_games(games, weeks, team_id, opponent, week, game_name)
        if len(candidates) > 1:
            print(f"\nGames for {team_label} this season:")
    game = choose(candidates, lambda g: describe_game(g, weeks), "game")
    gid = game["gameid"]

    names = list(dict.fromkeys([*hitting, *pitching]))
    matches, loose, missing = match_players(names, client.roster(season_id, team_id))
    existing = {
        kind: {s.get("playerid"): s for s in client.get_stats(kind, team_id, gid)}
        for kind in ("offensive", "pitching")
    }

    plan = []  # (kind, csv name, player, details, existing entry)
    for kind, table in (("offensive", hitting), ("pitching", pitching)):
        for name, details in table.items():
            if name in matches:
                player = matches[name]
                plan.append((kind, name, player, details, existing[kind].get(player["playerid"])))

    print(f"\nGame: {describe_game(game, weeks)}")
    for kind, label in (("offensive", "Hitting"), ("pitching", "Pitching")):
        rows = [p for p in plan if p[0] == kind]
        updates = sum(1 for p in rows if p[4])
        print(f"{label}: {len(rows)} players ({len(rows) - updates} new, {updates} already entered and will be overwritten)")
    if loose:
        print("\nMatched by a close name, double-check these:")
        for name in loose:
            p = matches[name]
            print(f"  {name}  ->  {p.get('lastname')}, {p.get('firstname')}")
    if missing:
        print("\nNot found on the NCBA roster, skipped:")
        for name in missing:
            print(f"  {name}")

    if not plan:
        raise SystemExit("\nNothing to upload.")
    if dry_run:
        print("\nDry run, nothing was uploaded.")
        return
    if not assume_yes:
        if not sys.stdin.isatty():
            raise SystemExit("\nRe-run with --yes to upload without a prompt.")
        if input("\nUpload these stats to CollClubSports? [y/N] ").strip().lower() not in ("y", "yes"):
            print("Cancelled, nothing was uploaded.")
            return

    for i, (kind, name, player, details, entry) in enumerate(plan, 1):
        try:
            client.save_stats(kind, team_id, gid, _stats_body(player, gid, details, entry),
                              entry.get("statsid") if entry else None)
        except CCSError as e:
            raise CCSError(f"stopped at {name} ({kind}) after {i - 1} of {len(plan)} uploads: {e}. "
                           "Re-running is safe: entries already uploaded are updated, not duplicated.") from None
        print(f"  [{i}/{len(plan)}] {kind:9s} {name}")
    print(f"\nUploaded {len(plan)} stat lines. The NCBA site refreshes public stats periodically, "
          "so they may take a while to appear on clubbaseball.org.")


def add_upload_arguments(parser):
    group = parser.add_argument_group("NCBA upload options")
    group.add_argument("--opponent", help="only consider games against this team (part of the name is fine)")
    group.add_argument("--week", help='only consider games in this week, e.g. 16 or "Week 16"')
    group.add_argument("--game", dest="game_name", metavar="N", help="game number within the week, e.g. 2 for Game 2")
    group.add_argument("--game-id", help="CollClubSports game id, skips game selection")
    group.add_argument("--dry-run", action="store_true",
                       help="log in and show what would be uploaded without changing anything")
    group.add_argument("-y", "--yes", action="store_true", help="upload without asking for confirmation")


def upload_from_args(hitters, pitchers, args):
    try:
        upload(hitters, pitchers, game_id=args.game_id, opponent=args.opponent, week=args.week,
               game_name=args.game_name, dry_run=args.dry_run, assume_yes=args.yes)
    except CCSError as e:
        sys.exit(f"\nUpload failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload an already converted CSV (from ./run --save) to the NCBA site (admin.collclubsports.com).")
    parser.add_argument("csv_path", help="converted CSV saved by ./run --save, e.g. bc_game1.csv")
    add_upload_arguments(parser)
    args = parser.parse_args()
    if not os.path.exists(args.csv_path):
        parser.error(f"could not find {args.csv_path}")
    upload_from_args(*read_converted_csv(args.csv_path), args)
