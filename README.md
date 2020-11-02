# StravaFab

Dit script dient om automatisch alle data uit een stravagroep te verweken en op te slaan in een databank op een manier die gemakkelijk te gebruiken valt voor de client.
Het komt ook met een script die alle data uit de databank mooi verwerkt in een csvfile om te distributen.
Het script is momnteel aangepast om te weken met de dynamiek voor de fabiola, maar dit kan zonder veel moeite aangepast worden.


## Usage
* clone deze repo
* maak de folder data aan met daarin de file users.csv ( voornaam;achternaam;kamernr;strava_id )
* install de requirements met `pip3 install -r requirements.txt`
* voer main.py uit met python3

## filestructure
* `data/` : hierin moet users.csv gestoken worden en wordt de databank in opgeslagen.
* `main.py` : hierin zit alle code die de parts aan elkaar hecht en zit ook de grootste functionaliteit in geprogrammeerd
* `src/` : hierin zit `scraper.py` met de functies om de data van strava te scrapen en `models.py` die specificaties van de databank vastleggen. 

## costum instellingen
### andere groep
Pas in `main.py` de `club_id` variable aan

### andere velden voor user
We gebruiken SqlAlchemy, dus je kan de velden aanpassen in `models.py`.
verder moet je dan ook de functies `add_to_db` en `add_users` aan te passen in `main.py`.
en ten slotte moet je dan ook de `dump_csv.py` aanpassen om de costum velden te gebruiken>
Dit zit allemaal heel straightforward in elkaar en zou zonder veel moeite aangepast moeten kunnen worden.

## Python versie
Het script is getest met versie 3.6 en 3.8, er is dus geen zekerheid dat het ook
werkt met 3.5 of lager.
