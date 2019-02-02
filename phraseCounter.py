#!/usr/bin/python3
# Phrase counter
#Usage: python3 phrasecounter.py file.txt

import re
import argparse
import collections

#parse args
parser = argparse.ArgumentParser(description='Count phrases in a text.')
parser.add_argument('-c', '--clip', dest="clip", action='store_true', help='Use text from the clipboard.')
parser.add_argument(dest='file', help='Use text from a file', nargs='?')
args = parser.parse_args()

if args.file: # read a text file
    with open(args.file, "r") as file:
        text = file.read()
elif args.clip: # read text from the clipboard
    try:
        import pyperclip
        text = pyperclip.paste()
    except ModuleNotFoundError:
        text = input("pyperclip module not found. Get it from https://pypi.org but meanwhile paste your text here manually: ")
else: # type text in manually
    text = input("Type your text here: ")

def depunctuate(phrase):
    '''Remove punctuation from a text'''
    phrase = re.sub("[^a-zA-Z0-9áéíóöőúüűćčđšžÁÉÍÓÖŐÚÜŰĆČĐŠŽ']+", " ", phrase.lower())
    return re.sub("\\s+'|'\\s+", " ", phrase)

def tokenise(passage):
    '''Returns a dictionary of all the words in the passage and how many times they occur'''
    #return collections.Counter(passage)
    tokens = {}
    for token in passage:
        if token.strip() not in tokens:
            tokens[token.strip()] = 1
        else:
            tokens[token.strip()] += 1
    return tokens

def findNeighbours(worddict, counter):
    '''If phrases of length n occur more than once in a text, find the words that precede or 
    follow them, creating a dictionary of phrases of length n+1. Use recursion to build
    dictionaries of longer and longer phrases until there are no more phrases that occur
    more than once, or until we reach the recursion limit of 10. Returns a list of ordered
    dictionaries and a counter to keep track of the recursion. 
    worddict[n] is a dictionary whose keys are phrases of length n+1 and values are how many times 
    they occured.'''
    done = False
    while not done and counter < 10:
        new = []
        worddict.append({})
        for key, value in worddict[-2].copy().items():
            if value > 1:
                left = re.compile(f"\S+\s{key}\s") #find the word left of this phrase
                right = re.compile(f"\s{key}\s\S+") #find the word right of this phrase
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

#assemble a list of the 10 most repeated phrased by length and frequency descending
mostFrequent = []
width = 1
while len(mostFrequent) < 10:
    for i in range(length):
        for phrase in phrases[i]:
            if len(mostFrequent) < 1: #add the first item
                if len(phrase) > width + 1: #line things up neatly
                    width = len(phrase) + 1
                mostFrequent.append((str(len(phrase.split())) + ' words\t', str(phrase), '\t' + str(phrases[i][phrase]) + ' times'))
                continue
            found = False
            for item in mostFrequent:
                if phrase.strip() in item[1]:
                    #this repeated phrase is a substring of one we've already mentioned
                    found = True 
                    break
            if not found: #user don't know about this repeated phrase yet
                if len(phrase) > width + 1:
                    width = len(phrase) + 2
                mostFrequent.append((str(len(phrase.split())) + ' words\t', str(phrase), '\t' + str(phrases[i][phrase]) + ' times'))
            if len(mostFrequent) == 10:
                break
    break

#print the list
counter = 0
for i in range(len(mostFrequent)):
    for j in range(len(mostFrequent[i])):
        if j == 1:
            print(mostFrequent[i][j].ljust(width), end="")
        else:
            print(mostFrequent[i][j].ljust(9), end="")
    print("\n", end="")
    counter += 1
    if counter == 10:
        break

#expected results for first two stanzas of Mary had a little lamb:
#
# 5 words  mary had a little lamb         2 times 
# 4 words  everywhere that mary went      2 times 
# 2 words  went mary                      2 times 
# 2 words  lamb little                    2 times 
# 1 words  was                            2 times 
