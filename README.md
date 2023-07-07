# clubbaseball

## v1 (Deprecated)
Need to copy/paste stats tables from "Season Stats" tab into the corresponding variables. Must log in on your own in a browser, navigate to the tab, and select the stat range (typically one game at a time) for 
- Hitting stat tables: "Standard", "Patience, Speed & Power", "QABs & Team Impact"
- Pitching stat tables: "Standard", "Command", "Batter Results", "Runs & Running Game"

## v2
This is a more automated option. It will log in for you and output the same information with you doing less work. All you need to do is the setup, and then you are good to go.

### .env
1. `touch v2/.env`
2. Open the file `v2/.env` in any text editor and paste the following into it. Fill in the email and password you use to log into GameChanger:

```
email=
password=
```


**Note:** that you must be admin (or have GameChanger premium) to access the stats.

### Instructions to Execute the Program
1. Navigate to GameChanger Classic. Log in and select the "Season Stats" tab. Select the appropriate date range
2. Copy the URL in the top bar.
3. Execute "./run \<your_copied_url\>".
4. If you would like to name the output spreadsheets, you can do so by appending "--hit \<name\>" and "--pitch \<name\>"'. If you do not specify names, they will be called "hit_stats" and "pitch_stats", respectively.

### Example Usage
- To access the help at any time, enter "./run --help-me"
- The general structure of the command is "./run \<your_copied_url\> --hit \<name\> --pitch \<name\>"
- A concrete example of the command is "./run https://gc.com/t/spring-2023/northeastern-university-huskies-club-640424614cea87ae8c000001/stats --hit UConn_hit1 --pitch UConn_pitch1"