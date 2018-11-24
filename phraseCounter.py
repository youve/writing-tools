#!/usr/bin/python3
# Phrase counter

import re
from optparse import OptionParser
import collections

#Usage: python3 phrasecounter.py file.txt

parser = OptionParser()

parser.add_option("-c", "--clipboard", dest="clip",
                  help="paste from clipboard", metavar="CLIPBOARD")

(options, args) = parser.parse_args()

if args:
    with open(args[0], "r") as file:
        text = file.read()
elif options.clip:
    try:
        import pyperclip
        text = pyperclip.paste()
    except ModuleNotFoundError:
        text = input("pyperclip module not found. Get it from https://pypi.org but meanwhile paste your text here manually: ")
else:
    text = input("Type your text here: ")

def depunctuate(string):
    string = string.replace(',', '', -1)
    string = string.replace(';', '', -1)
    string = string.replace('.', '', -1)
    string = string.replace('?', '', -1)
    string = string.replace('"', '', -1)
    string = string.replace('!', '', -1)
    string = string.replace('\n', ' ', -1)
    string = string.replace('--', '', -1)
    string = string.replace('  ', ' ', -1)
    return string

def tokenise(passage):
    tokens = {}
    for token in passage:
        if token.strip() not in tokens:
            tokens[token.strip()] = 1
        else:
            tokens[token.strip()] += 1
    return tokens

def findNeighbours(worddict, counter):
    done = False
    while not done and counter < 10:
        new = []
        worddict.append({})
        for key, value in worddict[-2].copy().items():
            if value > 1:
                left = re.compile(f"\S+\s{key}\s")
                right = re.compile(f"\s{key}\s\S+")
                worddict[-1].update(tokenise(left.findall(text)))
                worddict[-1].update(tokenise(right.findall(text)))
                worddict[-1] = collections.OrderedDict(worddict[-1])
            else:
                del worddict[-2][key]
        new = worddict[-1]
        counter += 1
        if len(new) >= 1:
            nextbatch, counter = findNeighbours([new], counter)
            for item in nextbatch:
                if item not in worddict:
                    worddict.append(item)
        else:
            done = True
            break
    return worddict, counter

text = depunctuate(text.lower()) #str(text)
listedText = text.split() #list(text)
words = tokenise(listedText) # dict(words)
phrases, counter = findNeighbours([words], 0) #list(OrderedDict(string, int)), int
length = len(phrases)

phrases.reverse() # longest strings at first
for i in range(len(phrases)): # sort each dict in phrases by value descending
    phrases[i] = collections.OrderedDict(sorted(phrases[i].items(), key=lambda t: t[1], reverse=True))

mostFrequent = []
width = 1
while len(mostFrequent) < 10:
    for i in range(length):
        for phrase in phrases[i]:
            if len(mostFrequent) < 1:
                if len(phrase) > width + 1:
                    width = len(phrase) + 1
                mostFrequent.append((str(len(phrase.split())) + ' words\t', str(phrase), '\t' + str(phrases[i][phrase]) + ' times'))
                continue
            found = False
            for item in mostFrequent:
                if phrase.strip() in item[1]:
                    found = True
                    break
            if not found:
                if len(phrase) > width + 1:
                    width = len(phrase) + 1
                mostFrequent.append((str(len(phrase.split())) + ' words\t', str(phrase), '\t' + str(phrases[i][phrase]) + ' times'))
            if len(mostFrequent) == 10:
                break
    break

for i in range(len(mostFrequent)):
    for j in range(len(mostFrequent[i])):
        if j == 1:
            print(mostFrequent[i][j].ljust(width), end="")
        else:
            print(mostFrequent[i][j].ljust(9), end="")
    print("\n", end="")

#expected results for first two stanzas of Mary had a little lamb:
#
#5 words    mary had a little lamb  2 times
#4 words    mary went mary went     2 times
#4 words    little lamb little lamb 2 times
#4 words    everywhere that mary went   2 times
#1 words    was                   2 times