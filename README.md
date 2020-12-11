# IRE Major Project - Generating infoboxes for Hindi Wikipedia articles
Building models using wikidata and external databases to automatically generate key-value pairs in the infobox for Hindi Wikipedia articles not having infoboxes.
## Instructions to run the code
### Using wikidata
Requirements: 
networkx, googletrans
```python
pip3 install networkx, googletrans
```
Build network graphs-heading
```python
python3 build_graph.py "json_file"
```
Get infoboxes
```python
python3 ranking.py entity_id  1/2/3/4/5
```
### Using external databases
#### Movie domain
filmWithoutInfoboxes.txt contains the films not having infoboxes. To run the code, put transliteration_pairs.txt in the same directory as extractMovies.py and run the following command.
```python
python3 extractMovies.py "movie_title"
```
#### Actors domain
Requirements:
wptools, googletrans
```python
pip3 install wptools
pip3 install googletrans
```
Run all the cells in the python notebook "extractActors.ipynb"
#### Cricketers domain
Requirements:
wptools, googletrans
```python
pip3 install wptools
pip3 install googletrans
```
Run all the cells in the python notebook "extractCricketers.ipynb"
