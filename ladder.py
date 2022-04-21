import json


def get_ladder():
    teams = {}

    matches = json.load(open("matches.json"))

    for m in matches:
        if m["status"] == "CONCLUDED":
            home_score = m["home"]["score"]["totalScore"]
            away_score = m["away"]["score"]["totalScore"]

            print(
                m["home"]["team"]["abbreviation"],
                m["away"]["team"]["abbreviation"],
                home_score,
                away_score,
            )

            for t in ["home", "away"]:
                if m[t]["team"]["abbreviation"] not in teams:
                    teams[m[t]["team"]["abbreviation"]] = {
                        "wins": 0,
                        "losses": 0,
                        "draws": 0,
                        "for": 0,
                        "against": 0,
                        "results": [],
                    }

            teams[m["home"]["team"]["abbreviation"]]["for"] += home_score
            teams[m["home"]["team"]["abbreviation"]]["against"] += away_score
            teams[m["away"]["team"]["abbreviation"]]["for"] += away_score
            teams[m["away"]["team"]["abbreviation"]]["against"] += home_score

            if home_score > away_score:
                teams[m["home"]["team"]["abbreviation"]]["wins"] += 1
                teams[m["home"]["team"]["abbreviation"]]["results"].append("W")

                teams[m["away"]["team"]["abbreviation"]]["losses"] += 1
                teams[m["away"]["team"]["abbreviation"]]["results"].append("L")
            elif away_score > home_score:
                teams[m["home"]["team"]["abbreviation"]]["losses"] += 1
                teams[m["home"]["team"]["abbreviation"]]["results"].append("L")

                teams[m["away"]["team"]["abbreviation"]]["wins"] += 1
                teams[m["away"]["team"]["abbreviation"]]["results"].append("W")
            else:
                teams[m["home"]["team"]["abbreviation"]]["draws"] += 1
                teams[m["home"]["team"]["abbreviation"]]["results"].append("D")

                teams[m["away"]["team"]["abbreviation"]]["draws"] += 1
                teams[m["away"]["team"]["abbreviation"]]["results"].append("D")

    teams = {
        k: teams[k]
        for k in sorted(
            teams, key=lambda x: teams[x]["for"] / teams[x]["against"], reverse=True
        )
    }
    teams = teams = {
        k: teams[k]
        for k in sorted(
            teams,
            key=lambda x: teams[x]["wins"] * 4 + teams[x]["draws"] * 2,
            reverse=True,
        )
    }

    html = ""
    html += "<section><h2>Ladder</h2><ol>"
    html += '<li><span class="team"></span><span class="wins">W</span><span class="losses">L</span><span class="draws">D</span><span class="percentage"></span><span class="results">Last 5</span></li>'

    for team in teams:
        html += "<li>"
        html += f'<span class="team">{team}</span>'
        html += f'<span class="wins">{teams[team]["wins"]}</span>'
        html += f'<span class="losses">{teams[team]["losses"]}</span>'
        html += f'<span class="draws">{teams[team]["draws"]}</span>'
        html += f'<span class="percentage">{teams[team]["for"] / teams[team]["against"] * 100:.1f}%</span>'
        html += f'<span class="results">{"".join(teams[team]["results"][-5:])}</span>'
        html += "</li>"

    html += "</ol></section>"
    return html
