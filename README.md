# clubbaseball

## Motivation
The National Club Baseball Association (NCBA) wants teams to report each game's statistics by uploading them onto their website. Stats are uploaded in a particular order player-by-player:

![NCBA Hitting Stats](media/entering%20stats/NCBA/NCBA%20hitting.png)

In GameChanger, the most popular digital option for recording baseball game statistics, the information required to enter statistics into the NCBA spans across separate, disparate tables. 

On the NCBA website, all statistics that weren't submitted are cleared when the currently selected player is switched. This means that filling out each player requires switching across 3+ tables on the GameChanger website, which is extremely inefficient and tedious.

This code aims to automate the process of collecting statistics by pulling data from relevant tables in GameChanger and outputting the statistics in the order expected by the NCBA. **Note:** that you must be admin (or have GameChanger premium) to access the stats.

## Versions
There are different scrapers for two different versions of GameChanger: "GameChanger" and "GameChanger Classic." Classic is being deprecated by the end of 2023 and uses different API calls and authentication. Scrapers prefaced with `new` are for "GameChanger," and scrapers prefaced with "classic" are for "GameChanger Classic."

## new_v1

**NOTE: You will probably be using this one**

**This only works with the new version of GameChanger. To scraper GameChanger classic, see classic_v2.**

`./run` reads a GameChanger stats export, puts the stats in NCBA order, and enters them into the NCBA site (admin.collclubsports.com) for one game, so you don't have to type each player into the Game Stats form. You need a Team Manager login for the team.

CollClubSports has no public API. The uploader uses the same internal API that the admin site's Game Stats form uses, so if CollClubSports changes their site it may stop working.

### Setup (once)
Copy the .env.example to a new file called .env in the new_v1 folder, then fill in your CollClubSports login in `new_v1/.env`. If you skip this, you will be asked for it each time.

### Uploading a game
1. Navigate to GameChanger, sign in, and choose the team/season.
2. Go to the stats tab and filter to the one game you want to upload ("Filter Stats" on the right side).
3. Click "Export Stats." There's no need to move or rename the file; you can pass its path directly.
4. Run `./run "path_to_stats.csv" --opponent "Oppponent Name on CollClubSports" --week {NUM} --game {NUM}` with filters that pick the game on the NCBA site. If more than one game matches, you pick it from a list:
   - Example usage: `./run ~/Downloads/fall_bc_1.csv --opponent "Boston College" --week 8 --game 1`
   - Add `--dry-run` to log in and see what would be uploaded without changing anything.
5. Before uploading it shows the game, how many players are new vs. already entered, players matched by a close name (e.g. "Mike" vs. "Michael"), and players not found on the NCBA roster (these are skipped). Confirm with `y`, or pass `--yes` to skip the prompt.

### Saving the converted CSV
- `--save NAME` also writes the converted stats to `NAME.csv`.
- `--no-upload` only converts (to `gc_stats.csv`, or `NAME.csv` with `--save`) and doesn't touch the NCBA site.
- To upload a CSV you saved earlier (for example after fixing something in it by hand), run `./upload NAME.csv --opponent "Boston College" --week 8 --game 1`.

### Notes
- Export one game at a time from GameChanger. This way each game's stats is in its own .csv file which you need to upload per game to CollClubSports.
- Players that already have stats for that game are updated, not duplicated, so re-running is safe.
- Make sure to match the opponent name exactly as it is on CollClubSports. Binghamton for example would be "SUNY - Binghamton" and BC would be "Boston College".


## classic_v2

**This only works with GameChanger classic, which will be deprecated at the end of 2023**

### Demo
See the following [video](https://youtu.be/wzqZL1Tiu7w) for a demo on the setup and execution for this stats scraper. Fast forward to 0:45 to skip the setup and just see a demo.

This is a more automated option. It will sign in for you and output the same information with you doing less work. All you need to do is the setup, and then you are good to go.

### .env
1. `touch classic_v2/.env`
2. Open the file `classic_v2/.env` in any text editor and paste the following into it. Fill in the email and password you use to sign into GameChanger:

```
email=
password=
```

### Instructions to Execute the Program
1. Navigate to GameChanger Classic. Sign in and select the "Season Stats" tab. Select the appropriate date range
2. Copy the URL in the top bar.
3. Execute "./run \<your_copied_url\>".
4. If you would like to name the output spreadsheets, you can do so by appending "--hit \<name\>" and "--pitch \<name\>"'. If you do not specify names, they will be called "hit_stats" and "pitch_stats", respectively.

### Example Usage
- To access the help at any time, enter "./run --help-me"
- The general structure of the command is "./run \<your_copied_url\> --hit \<name\> --pitch \<name\>"
- A concrete example of the command is "./run https://gc.com/t/spring-2023/northeastern-university-huskies-club-640424614cea87ae8c000001/stats --hit UConn_hit1 --pitch UConn_pitch1"


## classic_v1

**Please see classic_v2. classic_v1 is deprecated**

Need to copy/paste stats tables from "Season Stats" tab into the corresponding variables. Must sign in on your own in a browser, navigate to the tab, and select the stat range (typically one game at a time) for 
- Hitting stat tables: "Standard", "Patience, Speed & Power", "QABs & Team Impact"
- Pitching stat tables: "Standard", "Command", "Batter Results", "Runs & Running Game"
