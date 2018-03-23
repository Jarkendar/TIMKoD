import random
import numpy
from datetime import datetime
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


def countWordsIntensivity(content):
    dictionary = dict()
    length = 0
    words = content.split(' ')
    for word in words:
        length += 1
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    dictProbably = dict()
    for i in dictionary:
        dictProbably[i] = dictionary[i] / length
    dictio = sorted(dictProbably.items(), key=operator.itemgetter(1), reverse=True)

    sum30000 = 0
    sum6000 = 0
    iterator = 30000
    for i in dictio:
        sum30000 += i[1]
        if iterator > 24000:
            sum6000 += i[1]
        iterator -= 1
        if iterator == 0:
            break
    print("Dla 30000 = ", sum30000 * 100, "%")
    print("Dla 6000 = ", sum6000 * 100, "%")
    return dictProbably


def generateZad3(dictionary, size):
    message = ""
    letters = numpy.random.choice(list(dictionary.keys()), size, p=list(dictionary.values()))
    for i in letters:
        message += i + ' '
    print(message)
    countAverage(message.split(' '))


def getNextLetter(dictionary, patternWord):
    if patternWord in dictionary:
        nextWord = numpy.random.choice(list(dictionary[patternWord].keys()), 1,
                                       p=list(dictionary[patternWord].values()))
    else:
        word = numpy.random.choice(list(dictionary.keys()), 1)
        nextWord = numpy.random.choice(list(dictionary[word[0]].keys()), 1, p=list(dictionary[word[0]].values()))
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


def generateMarkowWordLevelDictionary(content, level):
    dictionary = dict()
    previousWords = ""
    for i in range(level - 1):
        previousWords += content[i] + ' '
    previousWords += content[level - 1]
    length = 0
    for i in range(level, len(content)):
        word = content[i]
        if length == level - 1:
            if previousWords not in dictionary:
                dictionary[previousWords] = dict()
                dictionary[previousWords][word] = 1
            else:
                if word not in dictionary[previousWords]:
                    dictionary[previousWords][word] = 1
                else:
                    dictionary[previousWords][word] += 1
            prev = previousWords.split(' ')
            previousWords = ""
            for j in range(1, len(prev)):
                previousWords += prev[j] + ' '
            previousWords += word
        else:
            length += 1
    for previous in dictionary:
        length = 0
        for word in dictionary[previous]:
            length += dictionary[previous][word]
        for word in dictionary[previous]:
            dictionary[previous][word] = dictionary[previous].get(word) / length
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


def markowWordSequence(markow1, markow2, startWord, wordNumber):
    lastWord = startWord + ' '
    sentence = ""
    lastWord += getNextLetter(markow1, startWord)
    sentence += lastWord
    for i in range(wordNumber):
        nextWord = getNextLetter(markow2, lastWord)
        prev = lastWord.split(' ')
        lastWord = ""
        for j in range(1, len(prev)):
            lastWord += prev[j] + ' '
        lastWord += nextWord
        sentence += ' ' + nextWord
    print("markow = ", sentence)
    countAverage(sentence.split(' '))


def saveFile(content, filename, sufix):
    name = "lab1/output_" + filename + sufix + ".txt"
    file = open(name, "w")
    file.write(content)
    file.close()


def main():
    startWord = "probability"
    startWord = ""
    signsNumber = 10000
    filename = "norm_wiki_sample"
    sufix = "-optimizetets-"
    # generateZad1(500000)
    # hamlet = readFile("lab1/norm_hamlet.txt")
    # romeo = readFile("lab1/norm_romeo_and_juliet.txt")
    wiki = readFile("lab1/" + filename + ".txt")
    # countAverage(hamlet.split(' '))
    # countAverage(romeo.split(' '))
    print("wiki ")
    wikiSplited = wiki.split(' ')
    countAverage(wikiSplited)
    # countLetterIntensivity(hamlet)
    # countLetterIntensivity(romeo)
    # dictionary = countLetterIntensivity(wiki)
    # generateZad3(dictionary, 500000)

    # start = datetime.now()
    # startLevel = 1
    # dictionary = generateMarkowLevelDictionary(wiki, startLevel)
    # content = markowString(dictionary, startWord, startLevel, signsNumber)
    # saveFile(content, filename, "_markow-" + str(startLevel) + sufix + str(signsNumber))
    # startLevel += 2
    # dictionary = generateMarkowLevelDictionary(wiki, startLevel)
    # content = markowString(dictionary, startWord, startLevel, signsNumber)
    # saveFile(content, filename, "_markow-" + str(startLevel) + sufix + str(signsNumber))
    # startLevel += 2
    # dictionary = generateMarkowLevelDictionary(wiki, startLevel)
    # content = markowString(dictionary, startWord, startLevel, signsNumber)
    # saveFile(content, filename, "_markow-" + str(startLevel) + sufix + str(signsNumber))
    # stop = datetime.now()
    # print(stop - start)

    # generateZad3(countWordsIntensivity(wiki), 1000)

    markow1 = generateMarkowWordLevelDictionary(wikiSplited, 1)
    # print(markow1)
    intensity = countWordsIntensivity(wiki)
    startWord = numpy.random.choice(list(intensity.keys()), 1, p=list(intensity.values()))
    markow2 = generateMarkowWordLevelDictionary(wikiSplited, 2)
    # print(markow2)
    markowWordSequence(markow1, markow2, startWord[0], 1000)


if __name__ == "__main__": main()
