Extract the 2015 world cup scores of all Indian matches (from espncricinfo) by loading them in a firefox browser using Selenium.

1. For each match
    a. Write the match summary to a file  in the given format (top 2 batsmen, bowlers from each team)
        [
            {
                "team_name": "India",
                "top_batsmen": [
                    {
                        "player_name": "Player 1",
                        "score": 100
                    },
                    {
                        "player_name": "Player 2",
                        "score": 90
                    },
                ],
                "top_bowlers": [
                    {
                        "player_name": "Player 3",
                        "wickets": 3,
                        "runs_conceded": 10
                    },
                    {
                        "player_name": "Player 4",
                        "wickets": 2,
                        "runs_conceded": 20
                    }
                ]
            },
            {
                "team_name": "Australia",
                "top_batsmen": [
                    {
                        "player_name": "Player 1",
                        "score": 100
                    },
                    {
                        "player_name": "Player 2",
                        "score": 90
                    },
                ],
                "top_bowlers": [
                    {
                        "player_name": "Player 3",
                        "wickets": 3,
                        "runs_conceded": 10
                    },
                    {
                        "player_name": "Player 4",
                        "wickets": 2,
                        "runs_conceded": 20
                    }
                ]
            }
        ]
    b. Upload the individual scores of all batsmen along with team scores to a google sheet.
    c. Keep track of the response times for the web-pages loaded using selenium. Find the average response time at the end
4. Fetch the data from sheets and plot the line-chart of scores when India batted first
5. Fetch the data from sheets and plot the average scores (take floor value of decimals) of all Indian players across the tournament in a bar chart. Assign a random colour to each player's bar

Use appropriate python modules/libraries whenever necessary - json, math, matplotlib, plotly, datetime, uuid, random, Google Sheets APIs
