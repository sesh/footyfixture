from datetime import datetime
import json
from thttp import request
from datetime import datetime
from zoneinfo import ZoneInfo


matches = json.loads(open("matches.json").read())
print(json.dumps(matches[0], indent=2))

html = ""
roundNumber = 0

for m in matches:
    if m["round"]["roundNumber"] != roundNumber:
        # is new round
        roundNumber = m["round"]["roundNumber"]
        if html:
            html += "</ul></section>"

        html += f"<section><h2>Round {roundNumber}</h2><ul>"

    home = m["home"]["team"]["abbreviation"]
    away = m["away"]["team"]["abbreviation"]
    venue = m["venue"]["abbreviation"]
    start_time_utc = datetime.fromisoformat(m["utcStartTime"].replace("+0000", "+00:00"))
    start_time_local = start_time_utc.astimezone(tz=ZoneInfo(m["venue"]["timezone"]))

    if m["home"].get("score"):
        home_score = m["home"]["score"]["totalScore"]
        away_score = m["away"]["score"]["totalScore"]
        home_win = home_score > away_score
        if home_score == away_score: home_win = None  # draw
    else:
        home_score, away_score, home_win = None, None, None

    html += "<li>"
    html += f'<time class="start-time-local" datetime="{start_time_utc}">{start_time_local.strftime("%d/%m %H:%M")}</time>'
    html += f'<span class="match"><span class="home{" win" if home_win == True else ""}">{home}</span>'

    if home_score:
        html += f'<span class="score"><span class="home-score{" win" if home_win == True else ""}">{home_score}</span> - <span class="away-score{" win" if home_win == False else ""}">{away_score}</span></span>'
    else:
        html += '<span class="vs">vs</span>'

    html += f'<span class="away{" win" if home_win == False else ""}">{away}</span></span>'
    html += f'<span class="venue">{venue}</span>'
    html += "</li>"

html += "</ul></section>"

template = request("https://basehtml.xyz").content.decode().split("<!-- Delete this part -->")[0]
template = template.replace("<title>Minimal base.html</title>", "<title>Footy Calendar - 2022 Edition</title>")
template = template.replace("width=device-width", "width=464px")
template = template.replace("<body>", """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700" rel="stylesheet"> 

    <style>
        body {
            font-family: 'IBM Plex Mono', monospace;
        }

        h2 {
            font-size: 1.1em;
        }

        ul {
            list-style: none;
            padding: 0;
        }

        section {
            margin: 0 12px 2em;
            width: 440px;
        }
        
        .start-time-local {
            display: inline-block;
            width: 8em;
        }

        .score, .vs {
            padding: 0 0.6em;
        }

        .match {
            display: inline-block;
            width: 14em;
        }

        .win {
            font-weight: 700;
        }
    </style>
<body>""")
template += html
template += "</body></html>"

with open("_build/index.html", "w") as f:
    f.write(template)