import json
import requests
import sys
import csv
from collections import defaultdict
import sys
from googletrans import Translator
translator = Translator()

pairs = defaultdict(list)

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def preprocessTitle():
    with open('transliteration_pairs.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            pairs[line.split("\t")[1]].append(line.split("\t")[0])

    movie = sys.argv[1]
    movie = movie.split(" ")

    for i in range(len(movie)):
        temp = []
        if len(pairs[movie[i]]) > 0:
            for word in pairs[movie[i]]:
                temp.append(word)
            movie[i] = temp
        else:
            movie[i] = [movie[i]]

    for i in range(len(movie)):
        for j in range(len(movie[i])):
            if(isEnglish(movie[i][j]) == False):
                translation = translator.translate(movie[i][j], dest="en")
                movie[i][j]= translation.text
    return movie

def extractInfobox(title):
    data_url = "http://www.omdbapi.com/?t=" + str(title) + "&apikey=54394774"
    try: 
        df = requests.get(data_url).json()
        title = df["Title"]
        released_date = df["Released"]
        runtime = df["Runtime"]
        genre = df["Genre"].split(", ")
        director = df["Director"]
        writer = df["Writer"]
        actors = df["Actors"].split(", ")
        poster = df["Poster"]
        production = df["Production"].split(", ")
        language = df["Language"]
        country = df["Country"]
        IMDbid = df["imdbID"]
        boxoffice = df["BoxOffice"]
        print("नाम: ", translator.translate(title, dest="hi").text)
        print("Poster: ", poster)
        print("निर्देशक: ", translator.translate(director, dest="hi").text)
        try:
            print("स्टूडियो: ", translator.translate(production, dest="hi").text)
        except:
            pass
        print("लेखक: ", translator.translate(writer, dest="hi").text)
        all_actors = ""
        for actor in actors:
            all_actors += translator.translate(actor, dest="hi").text + ", "
        all_actors = all_actors[:-2]
        print("अभिनेता: ", all_actors)
        all_genres = ""
        for gen in genre:
            all_genres += translator.translate(gen, dest="hi").text + ", "
        all_genres = all_genres[:-2]
        print("शैली: ", all_genres)
        print("समय सीमा: ", runtime.split(" ")[0] + " " + "मिनट")
        print("प्रदर्शन तिथि: ", translator.translate(released_date, dest="hi").text)
        print("भाषा: ", translator.translate(language, dest="hi").text)
        print("देश: ", translator.translate(country, dest="hi").text)
        print("आईएम्डीबी आईडी: ", IMDbid)
        if(boxoffice != "N/A"):
            print("Box Office: ", boxoffice)
        # print(title, released_date, runtime, genre, director, writer, actors, production, poster)
        return True
    except:
        return False

def find(movie):
    length = len(movie)

    title = ""

    if length == 1:
        for i in range(len(movie[0])):
            title = movie[0][i].lower()
            print(title)
            if extractInfobox(title):
                return
        print("The movie does not exist probably")

    elif length == 2:
        for i in range(len(movie[0])):
            for j in range(len(movie[1])):
                title = movie[0][i].lower() + "_" + movie[1][j].lower()
                # print(title)
                if extractInfobox(title):
                    return
        print("The movie does not exist probably")

    elif length == 3:
        for i in range(len(movie[0])):
            for j in range(len(movie[1])):
                for k in range(len(movie[2])):
                    title = movie[0][i].lower() + "_" + movie[1][j].lower() + "_" + movie[2][k].lower()
                    # print(title)
                    if extractInfobox(title):
                        return
        print("The movie does not exist probably")

    elif length == 4:
        for i in range(len(movie[0])):
            for j in range(len(movie[1])):
                for k in range(len(movie[2])):
                    for l in range(len(movie[3])):
                        title = movie[0][i].lower() + "_" + movie[1][j].lower() + "_" + movie[2][k].lower() + "_" + movie[3][l].lower()
                        # print(title)
                        if extractInfobox(title):
                            return
        print("The movie does not exist probably")

if __name__ == "__main__":
    title = preprocessTitle()
    find(title)