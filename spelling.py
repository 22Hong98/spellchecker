import re, collections,nltk
#from nltk.corpus import gutenberg
import math
import nltk.data
import itertools
UnigramCounts = collections.defaultdict(lambda: 0)
BigramCounts = collections.defaultdict(lambda: 0)
def known(words):
    suggests = []
    final_suggest=[]
    for w in words:
        if w in UnigramCounts:
            suggests.append(w)
    for w in suggests:
        if w in WORDS:
            final_suggest.append(w)
    #suggests = list(set(suggests))
    return final_suggest,len(final_suggest)
def know(word):
    if word in WORDS:
        return True
    else:
        return False
def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model
def words(text): return re.findall(r'\w+', text.lower())
WORDS = train(words(open('copus/ukenglish.txt','r',encoding='UTF-8').read()))
total=0
sentences = []

def tokenize_file():
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    content =open('copus/big.txt').read()
    for sentence in tokenizer.tokenize(content):
        sentence_clean = [i.lower() for i in re.split(r'\W+', sentence) if i]
        sentences.append(sentence_clean)
def train1():
    global total,sentences
    for sentence in sentences:
        sentence.insert(0, '<s>')
        sentence.append('</s>')
        for i in range(len(sentence) - 1):
            token1 = sentence[i]
            token2 = sentence[i + 1]
            UnigramCounts[token1] += 1
            BigramCounts[(token1, token2)] += 1
            total += 1
        total += 1
        UnigramCounts[sentence[-1]] += 1
def edits1(word):# Code reference peter norvig
    letters= 'abcdefghijklmnopqrstuvwxyz'
    splits= [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes= [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces= [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts= [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits_s(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i + 1], word[i + 1:]) for i in range(len(word))]
    #print(splits)
    deletes = [word[:0] + L + R[1:] for L, R in splits if R]
    transposes = [word[:0] + L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [word[:0] + L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [word[:0] + L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts+[word])
def edits2(word):
    input=list(edits1(word))
    total=[]
    for i in range(len(input)):
        k=edits1(input[i])
        total+=k
    return set(total)
def edits3(word):
    input = list(edits2(word))
    total = []
    for i in range(len(input)):
        k = edits1(input[i])
        total += k
    return set(total)
def P(word):
    return UnigramCounts[word]
def non_word_correct(word):
    candidates = set(known([word])[0]) or set(known(edits1(word))[0]) or set(known(edits2(word))[0]) or [word]
    #print(candidates)
    return max(candidates, key=P)
def candidate_sentence(sentence):
    candidate_sentences = []
    words_count = {}
    if len(sentence)<7:
        for i in range(len(sentence)):
            candidate_sentences.append(known(edits_s(sentence[i]))[0] or [sentence[i]])
            words_count[sentence[i]] = known(edits_s(sentence[i]))[1]
    else:
        for i in range(len(sentence) - 1):
            if BigramCounts[(sentence[i], sentence[i + 1])] > 1:
                candidate_sentences.append([sentence[i]])
                words_count[sentence[i]] = 1
            else:
                candidate_sentences.append(known(edits_s(sentence[i]))[0] or [sentence[i]])
                words_count[sentence[i]] = known(edits_s(sentence[i]))[1]
        candidate_sentences.append([sentence[len(sentence)-1]])
        words_count[sentence[len(sentence)-1]]=1

    candidate_sentences = list(itertools.product(*candidate_sentences))
    return candidate_sentences, words_count

def correction_score(words_count, old_sentence, new_sentence) :
    score = 1
    for i in range(len(new_sentence)) :
        if new_sentence[i] in words_count :
            score *= 0.95
        else :
            score *= (0.05 / (words_count[old_sentence[i]] - 1))
    return math.log(score)

def score(sentence):
    #global total
    score = 0.0
    for i in range(len(sentence) - 1):
        if BigramCounts[(sentence[i],sentence[i + 1])] > 0:
            score += math.log(BigramCounts[(sentence[i],sentence[i + 1])])
            score -= math.log(UnigramCounts[sentence[i]])
        else:
            score += (math.log(UnigramCounts[sentence[i + 1]] + 1)+math.log(0.4))
            score -= math.log(len(UnigramCounts))
    return score

def real_word_correction(old_sentence) :
    bestScore = float('-inf')
    bestSentence = []
    sentences, word_count = candidate_sentence(old_sentence)
    for new_sentence in sentences:
        new_sentence = list(new_sentence)
        score1 = correction_score(word_count, new_sentence, old_sentence)
        new_sentence.insert(0, '<s>')
        new_sentence.append('</s>')
        score1 += score(new_sentence)
        if score1 >= bestScore:
            bestScore = score1
            bestSentence = new_sentence
    bestSentence = ' '.join(bestSentence[1:-1])
    return bestSentence, bestScore

"""
def _init():
    tokenize_file()
    train1()
    flag=True
    while flag==True:
        c = input('input a string: ')
        print(return_best_sentence(c))
        a = input('Y/N: ')
        if a.lower()=='n':
            flag=False
"""



