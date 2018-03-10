import random
import numpy
import re
import operator


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


def compareStrings(pattern, word):
    for i in range(len(pattern)):
        if pattern[i] != word[i]:
            return False
    return True


def getNextLetter(dictionary, patternWord):
    matchingWords = []
    sumProbabilities = 0
    for word in dictionary:
        if compareStrings(patternWord, word):
            matchingWords.append(word)
            sumProbabilities += dictionary.get(word)
    probabilities = []
    for word in matchingWords:
        probabilities.append(dictionary.get(word) / sumProbabilities)
    if len(matchingWords) == 0:
        nextWord = numpy.random.choice(list(dictionary.keys()), 1, p=list(dictionary.values()))
    else:
        nextWord = numpy.random.choice(matchingWords, 1, p=probabilities)
    return nextWord[0][len(nextWord[0]) - 1]


def generateMarkowLevelDictionary(content, level):
    dictionary = dict()
    previousLetter = ""
    for i in range(level):
        previousLetter += content[i]
    length = 0
    count = 0
    for letter in content:
        if count == level - 1:
            word = previousLetter + letter
            if word not in dictionary:
                dictionary[word] = 1
            else:
                dictionary[word] += 1
            length += 1
            previousLetter += letter
            previousLetter = previousLetter[-level:]
        else:
            count += 1
    for phase in dictionary:
        dictionary[phase] = dictionary.get(phase) / length
    return dictionary


def markowString(dictionary, startWord, markowLevel, signsNumber):
    lastString = startWord[-markowLevel:]
    message = startWord
    for i in range(signsNumber):
        nextSign = getNextLetter(dictionary, lastString)
        message = message + nextSign
        lastString += nextSign
        lastString = lastString[-markowLevel:]
        if i % (signsNumber / 10) == 0:
            print(i, " in ", signsNumber)
    print("markow", markowLevel, " = ", message)
    countAverage(message.split(' '))
    return message


def saveFile(content, filename, sufix):
    name = "output" + filename + sufix + ".txt"
    file = open(name, "w")
    file.write(content)
    file.close()


def main():
    startWord = "probability"
    signsNumber = 1000
    filename = "norm_wiki_sample"
    # generateZad1(500000)
    # hamlet = readFile("norm_hamlet.txt")
    # romeo = readFile("norm_romeo_and_juliet.txt")
    wiki = readFile(filename + ".txt")
    # countAverage(hamlet.split(' '))
    # countAverage(romeo.split(' '))
    print("wiki ")
    countAverage(wiki.split(' '))
    # countLetterIntensivity(hamlet)
    # countLetterIntensivity(romeo)
    # dictionary = countLetterIntensivity(wiki)
    # generateZad3(dictionary, 500000)
    dictionary = generateMarkowLevelDictionary(wiki, 1)
    content = markowString(dictionary, startWord, 1, signsNumber)
    saveFile(content, filename, "1-" + str(signsNumber))
    dictionary = generateMarkowLevelDictionary(wiki, 3)
    content = markowString(dictionary, startWord, 3, signsNumber)
    saveFile(content, filename, "3-" + str(signsNumber))
    dictionary = generateMarkowLevelDictionary(wiki, 5)
    content = markowString(dictionary, startWord, 5, signsNumber)
    saveFile(content, filename, "5-" + str(signsNumber))


if __name__ == "__main__": main()
