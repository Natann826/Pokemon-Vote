import requests
from bs4 import BeautifulSoup
import json


request_ = requests.get("https://pokemondb.net/pokedex/all")
soup = BeautifulSoup(request_.content, "html.parser")
pokedex = soup.find(id="pokedex")

pokemonRows = pokedex.tbody.find_all("tr")


def pkmnNameToLinkName(pkmnName):
    pkmnName = pkmnName.replace(" ", "-")
    pkmnName = pkmnName.replace(".", "-")
    return pkmnName

def hasOfficialArtwork(url):
    r = requests.get(url)
    return (r.status_code == 200)

def getImgUrl(pokemonRow):
    data = []
    nameTd = pokemonRow[1] # nameTD?!?!?!?! more like BLASSTD!!!! 😲😲😲

    if nameTd.string: # if its not a weird form thing
        data.append(nameTd.string)
        name = nameTd.string.lower()
        name = pkmnNameToLinkName(name)
        data.append(f"https://img.pokemondb.net/artwork/{name}.jpg")
    else: # if it is
        data.append(f"{nameTd.a.string} ({nameTd.small.string})")
        name = pokemonRow[0].span.img['src'].split("/")[-1].split(".")[0] # lol
        data.append(f"https://img.pokemondb.net/artwork/{name}.jpg")
    return data

def getPkmnWithoutArtwork():
    pkmnWithoutArtwork = []
    for pokemonRow in getSplitPkmnRows():
        data = getImgUrl(pokemonRow)
        if not hasOfficialArtwork(data[1]):
            pkmnWithoutArtwork.append(data[0])
    return pkmnWithoutArtwork

def getPkmnData():
    pixelPokemon = json.loads(open("bad_list.json", "r").read())
    pkmnData = []
    id_ = 0

    splitRows = getSplitPkmnRows()
    for pokemonRow in splitRows:
        pkmn = {}
        tds = pokemonRow

        pkmn['page'] = f"https://pokemondb.net{tds[1].a['href']}"




        page = requests.get(pkmn['page'])
        soupedupboi = BeautifulSoup(page.content, 'html.parser')
        parsed = ""
        for child in soupedupboi.find(id="main").find("p").children:
            parsed += child.string

        pkmn['info'] = parsed

        td0spans = tds[0].find_all("span")
        pkmn['pokedexNumber'] = td0spans[1].string

        data = getImgUrl(pokemonRow)
        pkmn['name'] = data[0]
        url = data[1]

        if pkmn['name'] in pixelPokemon: # if its in the "bad list" json file
            pkmn['img'] = td0spans[0].img['src'] # set it to be the pixel icon
        else:
            pkmn['img'] = url

        pkmn['id'] = id_

        pkmnData.append(pkmn)

        id_ += 1

    return pkmnData

def getSplitPkmnRows():
    splitRows = []
    for pokemonRow in pokemonRows:
        tds = pokemonRow.find_all('td')
        splitRows.append(tds)

    return splitRows

def updateBadListJson():
    with open("bad_list.json", "w") as jsonFile:
        json.dump(getPkmnWithoutArtwork(), jsonFile)

def updatePkmnData():
    with open("pkmnData.json", "w") as jsonFile:
        json.dump(getPkmnData(), jsonFile, indent=4)