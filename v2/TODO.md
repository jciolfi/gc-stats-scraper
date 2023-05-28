TODOs
- Ensure logout is working correctly, debug with verbose output
- Get stats
    - Take in user-friendly url, extract team id (e.g. 640424614cea87ae8c000001), start_ts, and end_ts
        - keep in mind there may be no input for either start/end, but there must be input for team id
        - start_ts is omitted: range starts from first qualified game of season
        - end_ts is omitted: range ends at last qualified game of season
    - Set team id, append start_ts and end_ts (if applicable) to stats uri's
        - there are different query params for each table
    - Send request (will be json response this time), can yank out stats more easily?
- Improve command line args
    - have option to set name with -o <name>
        - will output name_hitting.csv and name_pitching.csv
        - otherwise default to game_hitting.csv and game_pitching.csv
    - have option to ask for help with --help?