import pandas as pd
import numpy as np
from flask import Flask, render_template, url_for, request
import requests
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
from collections import Counter

"""
TODO:


"""

app = Flask(__name__)

with open("pkmnData.json") as data:
    pkmnData = json.load(data)

def getResultsList(): # this makes the results list, with pokemon with the same votes counted as having the same placement
    data = json.load(open("scores.json", "r"))
    data = sorted(data.items(), key=lambda x:x[1], reverse=True) # opens, then sorts the pokemon by votes
    stringInfo = [] # going to calculate placement uniquness

    placement = 1 # starts from 1
    for value in data: # goes through each one
        if stringInfo.__len__() != 0: # means that theres a pokemon in it
            previousPkmn = stringInfo[-1] 
            currentPkmn = {"votes": value[1], "name": value[0]}
            if previousPkmn['votes'] != currentPkmn['votes']:
                placement += 1 # this is saying: if the last pokemon before me had a different amount of votes, up the placement (my placement) up by one
        else:
            currentPkmn = {"votes": value[1], "name": value[0]} # this is just for the first one

        currentPkmn['placement'] = placement
        stringInfo.append(currentPkmn) # append it

    final = []
    for pkmn in stringInfo:
        final.append(f"#{pkmn['placement']}: {pkmn['name']} - {pkmn['votes']} votes") # curate it
    return final # return it

def increaseScore(pkmn): # self explanatory, just updates the json file
    with open("scores.json", "r") as data:
        parsed = json.load(data)
    parsed[pkmn] += 1
    with open("scores.json", "w") as old:
        json.dump(parsed, old, indent=4)

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == "POST":
        increaseScore(request.form['pkmn'])
    return render_template('main.html', data=pkmnData)

@app.route('/results', methods=['POST', 'GET'])
def results():
    return render_template('results.html', data=getResultsList())

app.run()