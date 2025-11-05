from bs4 import BeautifulSoup, ResultSet, Tag
from enum import Enum, auto
import requests

class TypyNalady(Enum):
    DOBRÁ_NÁLADA = auto(),
    VELMI_DOBRÁ_NÁLADA = auto(),
    ŠPATNÁ_NÁLADA = auto(),
    VELMI_ŠPATNÁ_NÁLADA = auto(),
    VELMI_VELMI_ŠPATNÁ_NÁLADA = auto(),
    NEUTRÁLNÍ_NÁLADA = auto()

def main() -> None:
    url: str = "https://www.arsenal.com/results"

    response: requests.Response = requests.get(url)

    soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

    all_team_names: ResultSet[Tag] = soup.select(".accordion__content")
    last_match_html: Tag = all_team_names[0]

    teams: ResultSet[Tag] = last_match_html.select(".fixture-match__team")
    scores: ResultSet[Tag] = last_match_html.select(".scores__score")

    last_match_teams: list[str] = []
    last_match_scores: list[str] = []

    nalada: TypyNalady = TypyNalady.NEUTRÁLNÍ_NÁLADA

    for i in range(0, 2):
        last_match_teams.append(teams[i].select_one(".team-crest__name-value").text)
        last_match_scores.append(scores[i].text)

    top_team_name: str = ""
    top_team_score: int = -1

    remiza: bool = False

    team_names: list[str] = []

    for i, team_name in enumerate(last_match_teams):
        team_score: int = int(last_match_scores[i])
        
        if team_score > top_team_score:
            team_score = team_score
            top_team_name = team_name
        elif team_score == top_team_score:
            remiza = True
        
        team_names.append(team_name)
    
    if remiza:
        nalada = TypyNalady.ŠPATNÁ_NÁLADA
    elif top_team_name == "Arsenal":
        nalada = TypyNalady.DOBRÁ_NÁLADA
    else:
        nalada = TypyNalady.VELMI_ŠPATNÁ_NÁLADA
    
    if "Tottenham" in team_names or "Slavia Prague" in team_names:
        if nalada == TypyNalady.DOBRÁ_NÁLADA:
            nalada = TypyNalady.VELMI_DOBRÁ_NÁLADA
        elif nalada == TypyNalady.ŠPATNÁ_NÁLADA:
            nalada = TypyNalady.VELMI_ŠPATNÁ_NÁLADA
        elif nalada == TypyNalady.VELMI_ŠPATNÁ_NÁLADA:
            nalada = TypyNalady.VELMI_VELMI_ŠPATNÁ_NÁLADA  
                
    print(nalada.name)

if __name__ == "__main__":
    main()