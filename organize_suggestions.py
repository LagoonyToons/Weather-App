lines = []
with open("suggestions.txt", 'r') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

myList = sorted(set(lines))

with open('suggestions.txt', 'w') as file:
    for item in myList:
        file.write("%s\n" % item)
