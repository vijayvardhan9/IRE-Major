import csv
import sys
with open("movies.txt", "r") as f:
    csvreader = csv.reader(f, delimiter = '\t')
    for line in csvreader:
        if line[2].lower() == sys.argv[1]:
            print(line[0])