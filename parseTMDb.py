import json
import requests
from collections import defaultdict

# 208 pages

# https://api.themoviedb.org/4/discover/movie?api_key=325b2fbacc27736c5d13e4cf0cc50b18&with_original_language=hi&page=1

# Action          28
# Adventure       12
# Animation       16
# Comedy          35
# Crime           80
# Documentary     99
# Drama           18
# Family          10751
# Fantasy         14
# History         36
# Horror          27
# Music           10402
# Mystery         9648
# Romance         10749
# Science Fiction 878
# TV Movie        10770
# Thriller        53
# War             10752
# Western         37

titles = []
release_dates = []
genres = defaultdict(list)


for page in range(1, 209):
    data_url = "https://api.themoviedb.org/4/discover/movie?api_key=325b2fbacc27736c5d13e4cf0cc50b18&with_original_language=hi&page=" + str(page)
    df = requests.get(data_url).json()
    # print(df['page'])
    results = df['results']
    for i in range(20):
        try:
            titles.append(results[i]['original_title'])
        except:
            break
        try:
            release_dates.append(results[i]['release_date'])
        except:
            release_dates.append('NULL')
        for j in range(len(results[i]['genre_ids'])):
            genres[results[i]['original_title']].append(results[i]['genre_ids'][j])


with open('titles.txt', 'w') as f:
    for title in titles:
        f.write("%s\n" % title)

with open('release_dates.txt', 'w') as f:
    for release_date in release_dates:
        f.write("%s\n" % release_date)

with open('genres.txt', 'w') as f:
    f.write(json.dumps(genres))

# for title in titles:
#     print(title)