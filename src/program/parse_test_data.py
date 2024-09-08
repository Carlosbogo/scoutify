import csv

def parse(path):
    with open(path, newline="", encoding="utf8") as f:
        reader = csv.reader(f, delimiter=";")
        data = list(reader)

    return data