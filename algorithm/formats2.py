import csv
count = {}

with open("Crimes.csv", newline='') as f:
    crimes = csv.DictReader(f)
    for row in crimes:
        t = row['Primary Type']
        count[t] = count.get(t, 0) + 1

print(max(count.items(), key= lambda x: x[1])[0])
