import numpy
from bitarray import bitarray
from tqdm import tqdm

CODE = numpy.matrix([["a", "000000"],
                     ["b", "000001"],
                     ["c", "000010"],
                     ["d", "000011"],
                     ["e", "000100"],
                     ["f", "000101"],
                     ["g", "000110"],
                     ["h", "000111"],
                     ["i", "001000"],
                     ["j", "001001"],
                     ["k", "001010"],
                     ["l", "001011"],
                     ["m", "001100"],
                     ["n", "001101"],
                     ["o", "001110"],
                     ["p", "001111"],
                     ["q", "010000"],
                     ["r", "010001"],
                     ["s", "010010"],
                     ["t", "010011"],
                     ["u", "010100"],
                     ["v", "010101"],
                     ["w", "010110"],
                     ["x", "010111"],
                     ["y", "011000"],
                     ["z", "011001"],
                     ["0", "011010"],
                     ["1", "011011"],
                     ["2", "011100"],
                     ["3", "011101"],
                     ["4", "011110"],
                     ["5", "011111"],
                     ["6", "100000"],
                     ["7", "100001"],
                     ["8", "100010"],
                     ["9", "100011"],
                     [" ", "100100"]])


def compareString(content, decode):
    if len(content) != len(decode):
        print("Length is incorrect")
        return
    else:
        for i in range(len(content)):
            if content[i] != decode[i]:
                print("Incorrect symbol")
                return
        print("Strings are equals")
        return


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


def checkCodeInDict(dictionary, letter):
    return dictionary[letter]


def checkLetterInDict(dictionary, code):
    return dictionary[code]


def checkCodeInTable(letter):
    for i in range(len(CODE)):
        if CODE[i, 0] == letter:
            return CODE[i, 1]


def checkLetterInTable(code):
    for i in range(len(CODE)):
        if CODE[i, 1] == code:
            return CODE[i, 0]


def encode(content, dictionary):
    bits = bitarray(endian='big')
    for i in tqdm(content):
        bits.extend(checkCodeInDict(dictionary, i))
    return bits


def decode(bits, decodeDict):
    result = []
    for i in tqdm(range(0, int(len(bits))-6, 6)):
        letterCode = bits[i:i + 6]
        codeList = []
        for j in letterCode:
            if j:
                codeList.append("1")
            else:
                codeList.append("0")
        result.append(checkLetterInDict(decodeDict, "".join(codeList)))
    return "".join(result)


def save(codeDict, text, name):
    text.tofile(open(name + ".bin", 'wb'))
    codeString = ""
    for key, value in codeDict.items():
        codeString += key + ";" + value + "\n"
    open(name + "_dictionary.txt", "w").write(codeString)


def load(name):
    filename = name + "_encode"
    content = bitarray()
    content.fromfile(open(filename + ".bin", 'rb'))
    dictContent = readFile(filename + "_dictionary.txt")
    dictArray = dictContent.split("\n")
    dictionary = dict()
    for row in dictArray[:-1]:
        cells = row.split(";")
        dictionary[cells[1]] = cells[0]
    return content, dictionary


def doLetterDictFromTable(table):
    dictionary = dict()
    for i in range(len(table)):
        dictionary[table[i, 0]] = table[i, 1]
    return dictionary


def doCodeDictFromTable(table):
    dictionary = dict()
    for i in range(len(table)):
        dictionary[table[i, 1]] = table[i, 0]
    return dictionary


def main():
    filename = "norm_wiki_sample"
    file = "note"
    wiki = readFile(filename + ".txt")
    dictionaryLetter = doLetterDictFromTable(CODE)
    dictionaryCode = doCodeDictFromTable(CODE)
    bits = encode(wiki, dictionaryLetter)
    save(dictionaryLetter, bits, filename + "_encode")
    c, d = load(filename)
    decodeString = decode(c, d)
    compareString(wiki, decodeString)


if __name__ == "__main__": main()
