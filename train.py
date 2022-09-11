import pickle
import random
#=======================================================================================================================
#-----------------------------------------------Загрузка текста---------------------------------------------------------
#=======================================================================================================================
def LoadT(s):
    Docs = []    # -- массив документов
    with open(s, 'r') as Fdocs:
        for line in Fdocs:
            doc = line  # -- считываем документ(строку)
            Docs.append(doc)

    return Docs

#=======================================================================================================================
#--------------------------Обработка документов(строк). Выделяем слова из строк-----------------------------------------
#=======================================================================================================================
def Preparing(docs):
    sep = '.,:;&()<>!?"- \n'
    words = []

    for doc in docs:
        doc = doc.lower()
        word = ''
        for sym in doc:
            if sym in sep:
                if word != '':
                    words.append(word)
                    word = ''
                    if sym == '.':
                        words.append('END')
            else:
                word += sym

    return words

#=======================================================================================================================
#-------------------------------------------Получаем список n-грамм-----------------------------------------------------
#=======================================================================================================================
def get_ngrams(n, words):
    words = (n-1)*['START']+words
    ngrams = []

    for i in range(len(words)-(n-1)):
        ngrams.append( tuple(words[i+p] for p in range(n)) )

    return ngrams

#=======================================================================================================================
#-----------------------------Обучение модели, расчет вероятностей в словаре--------------------------------------------
#=======================================================================================================================
def train(ngrams):
    NDict = {ngram: {} for ngram in ngrams}
    n = len(ngrams[0])

    for i in range(len(ngrams)-1):
        next_word = ngrams[i+1][n-1]
        if next_word == 'END':
            continue
        if next_word in NDict[ngrams[i]]:
            NDict[ngrams[i]][next_word] += 1
        else:
            NDict[ngrams[i]][next_word] = 1

    for elem_dict in NDict:
        LenElemDict = 0
        if elem_dict != {}:
            for elem in NDict[elem_dict]:
                LenElemDict += NDict[elem_dict][elem]
            for elem in NDict[elem_dict]:
                NDict[elem_dict][elem] = NDict[elem_dict][elem] / LenElemDict

    return NDict

#=======================================================================================================================
#----------------------------------------------Основная программа-------------------------------------------------------
#=======================================================================================================================
n = 3
PATH = 'C:\\Users\\ivr0m\\Desktop\\work\\projects\\MSU projects\\text_generator\\voyna-i-mir-tom-1.txt'

docs = LoadT(PATH)
words = Preparing(docs)
ngrams = get_ngrams(n, words)
NDict = train(ngrams)
with open('data.pickle', 'wb') as f:
    pickle.dump(NDict, f)
    pickle.dump(words, f)
    pickle.dump(n, f)