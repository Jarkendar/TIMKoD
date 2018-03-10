import random
import numpy
from datetime import datetime


def countAverage(tab):
    suma = 0
    for word in tab:
        if len(word) != 0:
            suma += len(word)
    print("average = ", suma / len(tab))


def generateZad1(i):
    signs = "qwertyuiopasdfghjklzxcvbnm "
    message = ""
    for x in range(i):
        message += signs[random.randint(0, len(signs) - 1)]
    countAverage(message.split(' '))


def readFile(filename):
    file = open(filename)
    content = ""
    while True:
        line = file.readline()
        if len(line) == 0:
            break
        content += line
    return content


def countLetterIntensivity(content):
    dictionary = dict()
    length = 0
    for i in content:
        if i not in dictionary:
            dictionary[i] = 1
        else:
            dictionary[i] += 1
        length += 1
    for i in dictionary:
        # print(i, "->", dictionary.get(i) / length, "%")
        dictionary[i] = dictionary.get(i) / length
    # print(dictionary)
    return dictionary


def generateZad3(dictionary, size):
    message = ""
    letters = numpy.random.choice(list(dictionary.keys()), size, p=list(dictionary.values()))
    for i in letters:
        message += i
    countAverage(message.split(' '))


def getNextLetter(dictionary, patternWord):
    if patternWord in dictionary:
        nextWord = numpy.random.choice(list(dictionary[patternWord].keys()), 1,
                                       p=list(dictionary[patternWord].values()))
    else:
        word = numpy.random.choice(dictionary.keys(), 1)
        nextWord = numpy.random.choice(list(dictionary[word].keys()), 1, p=list(dictionary[word].values()))
    return nextWord[0]


def generateMarkowLevelDictionary(content, level):
    dictionary = dict()
    previousLetter = ""
    for i in range(level):
        previousLetter += content[i]
    count = 0
    for letter in content:
        if count == level - 1:
            if previousLetter not in dictionary:
                dictionary[previousLetter] = dict()
                dictionary[previousLetter][letter] = 1
            else:
                if letter not in dictionary[previousLetter]:
                    dictionary[previousLetter][letter] = 1
                else:
                    dictionary[previousLetter][letter] += 1
            previousLetter += letter
            previousLetter = previousLetter[-level:]
        else:
            count += 1
    for previous in dictionary:
        length = 0
        for letter in dictionary[previous]:
            length += dictionary[previous][letter]
        for letter in dictionary[previous]:
            dictionary[previous][letter] = dictionary[previous].get(letter) / length
    # print(dictionary)
    return dictionary


def markowString(dictionary, startWord, markowLevel, signsNumber):
    lastString = startWord[-markowLevel:]
    message = startWord
    for i in range(signsNumber):
        nextSign = getNextLetter(dictionary, lastString)
        message = message + nextSign
        lastString += nextSign
        lastString = lastString[-markowLevel:]
    print("markow", markowLevel, " = ", message)
    countAverage(message.split(' '))
    return message


def saveFile(content, filename, sufix):
    name = "lab1/output_" + filename + sufix + ".txt"
    file = open(name, "w")
    file.write(content)
    file.close()


def main():
    startWord = "probability"
    signsNumber = 10000
    filename = "norm_wiki_sample"
    sufix = "-optimizetets-"
    # generateZad1(500000)
    # hamlet = readFile("norm_hamlet.txt")
    # romeo = readFile("norm_romeo_and_juliet.txt")
    wiki = readFile("lab1/" + filename + ".txt")
    # countAverage(hamlet.split(' '))
    # countAverage(romeo.split(' '))
    print("wiki ")
    countAverage(wiki.split(' '))
    # countLetterIntensivity(hamlet)
    # countLetterIntensivity(romeo)
    # dictionary = countLetterIntensivity(wiki)
    # generateZad3(dictionary, 500000)
    start = datetime.now()
    startLevel = 7
    dictionary = generateMarkowLevelDictionary(wiki, startLevel)
    content = markowString(dictionary, startWord, startLevel, signsNumber)
    saveFile(content, filename, "_markow-"+str(startLevel) + sufix + str(signsNumber))
    startLevel += 2
    dictionary = generateMarkowLevelDictionary(wiki, startLevel)
    content = markowString(dictionary, startWord, startLevel, signsNumber)
    saveFile(content, filename, "_markow-"+str(startLevel) + sufix + str(signsNumber))
    startLevel += 2
    dictionary = generateMarkowLevelDictionary(wiki, startLevel)
    content = markowString(dictionary, startWord, startLevel, signsNumber)
    saveFile(content, filename, "_markow-"+str(startLevel) + sufix + str(signsNumber))
    stop = datetime.now()
    print(stop - start)


if __name__ == "__main__": main()
