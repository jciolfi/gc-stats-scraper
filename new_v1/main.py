import argparse, csv
from dataclasses import astuple
from classes import Offsense, Pitching
import ncba_upload

# column order matches the Offsense / Pitching fields, which are in NCBA order
HITTING_COLUMNS = ["AB", "R", "H", "2B", "3B", "HR", "RBI", "BB", "IBB", "SO", "SB", "CS", "SAC_F", "SAC_B", "HBP"]
PITCHING_COLUMNS = ["Started", "W", "L", "CG", "SHO", "SV", "SVO", "IP", "H", "R", "ER", "HR", "HBP", "BB", "IBB", "SO", "BK", "WP", "PK"]

offensive_stats = {}
pitching_stats = {}

def find_columns(sections, names):
    """Map (section, column name) -> index from GameChanger's two header rows.

    The first row has the section ("Batting", "Pitching", ...) above the first
    column of each section; the second has the column names. Names repeat across
    sections (H, HR, BB, SO, ...), and GameChanger adds columns over time, so
    columns are looked up by section and name rather than by fixed position."""
    columns, section = {}, ""
    for i, name in enumerate(names):
        if i < len(sections) and sections[i].strip():
            section = sections[i].strip()
        columns.setdefault((section, name.strip()), i)
    return columns


def parse_stats(fp):
    reader = csv.reader(fp)
    columns = find_columns(next(reader), next(reader))

    def indices(section, names):
        missing = [name for name in names if (section, name) not in columns]
        if missing:
            raise SystemExit(f"The GameChanger export has no {section} column named: {', '.join(missing)}")
        return {name: columns[(section, name)] for name in names}

    bat = indices("Batting", ["PA", "AB", "R", "H", "2B", "3B", "HR", "RBI", "BB", "SO", "SB", "CS", "SF", "SAC", "HBP"])
    pit = indices("Pitching", ["#P", "GS", "W", "L", "SV", "SVO", "IP", "H", "R", "ER", "HR", "HBP", "BB", "SO", "BK", "WP", "PIK"])

    for row in reader:
        if row[0] == "Totals":
            break

        player_name = f"{row[1]}, {row[2]}"
        b = lambda name: row[bat[name]]
        p = lambda name: row[pit[name]]

        # player got > 0 PAs
        if int(b("PA")) > 0:
            # AB, R, H, 2B, 3B, HR, RBI, BB, IBB, SO, SB, CS, SAC-F, SAC-B, HBP
            offensive_stats[player_name] = Offsense(b("AB"), b("R"), b("H"), b("2B"), b("3B"), b("HR"), b("RBI"), b("BB"), 'N/A', b("SO"), b("SB"), b("CS"), b("SF"), b("SAC"), b("HBP"))

        # player threw more than 0 pitches
        if int(p("#P")) > 0:
            # started, W, L, CG, SHO, SV, SVO, IP, H, R, ER, HR, HBP, BB, IBB, SO, BK, WP, PK
            pitching_stats[player_name] = Pitching(p("GS"), p("W"), p("L"), '0', '0', p("SV"), p("SVO"), p("IP"), p("H"), p("R"), p("ER"), p("HR"), p("HBP"), p("BB"), 'N/A', p("SO"), p("BK"), p("WP"), p("PIK"))

    if len(pitching_stats) == 1:
        for pitcher in pitching_stats:
            pitcher_stats = pitching_stats[pitcher]
            pitcher_stats.cg = '1'
            pitcher_stats.sho = '1' if pitcher_stats.r == '0' else '0'


def stat_tables():
    """Hitting and pitching stats as {"Last, First": {column: value}}, sorted by name."""
    hitters = {name: dict(zip(HITTING_COLUMNS, astuple(offensive_stats[name]))) for name in sorted(offensive_stats)}
    pitchers = {name: dict(zip(PITCHING_COLUMNS, astuple(pitching_stats[name]))) for name in sorted(pitching_stats)}
    return hitters, pitchers


def export_stats(filename):
    hitters, pitchers = stat_tables()
    with open(filename, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["OFFENSIVE STATS"])
        writer.writerow(["Name", *HITTING_COLUMNS])
        for name, stats in hitters.items():
            writer.writerow([name, *stats.values()])

        writer.writerow([])
        writer.writerow(["PTICHING STATS"])
        writer.writerow(["Name", *PITCHING_COLUMNS])
        for name, stats in pitchers.items():
            writer.writerow([name, *stats.values()])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a GameChanger stats export into NCBA order and upload it to the NCBA site.")
    parser.add_argument("stats_path", help="CSV exported from GameChanger")
    parser.add_argument("--save", metavar="NAME", help="also save the converted stats to NAME.csv")
    parser.add_argument("--no-upload", action="store_true",
                        help="only convert the stats to a CSV (gc_stats.csv unless --save is given), don't upload")
    ncba_upload.add_upload_arguments(parser)
    args = parser.parse_args()
    if args.no_upload and any([args.opponent, args.week, args.game_name, args.game_id, args.dry_run, args.yes]):
        parser.error("the NCBA upload options can't be used with --no-upload")

    stats_path = args.stats_path
    fp = None
    try:
        fp = open(stats_path)
    except:
        print(f"Could not find path to file: {stats_path}")
        exit(1)

    print("Parsing...")
    parse_stats(fp)
    fp.close()

    if args.save or args.no_upload:
        filename = (args.save or "gc_stats").removesuffix(".csv") + ".csv"
        export_stats(filename)
        print(f"\nExported stats to {filename}")

    if not args.no_upload:
        ncba_upload.upload_from_args(*stat_tables(), args)
