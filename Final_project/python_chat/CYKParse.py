# Code for CS 171, Winter, 2021
import Tree

verbose = False


def printV(*args):
    if verbose:
        print(*args)


# A Python implementation of the AIMA CYK-Parse algorithm in Fig. 23.5 (p. 837).
def CYKParse(words, grammar):
    T = {}
    P = {}
    # Instead of explicitly initializing all P[X, i, k] to 0, store
    # only non-0 keys, and use this helper function to return 0 as needed.

    def getP(X, i, k):
        key = str(X) + '/' + str(i) + '/' + str(k)
        if key in P:
            return P[key]
        else:
            return 0
    # Insert lexical categories for each word
    for i in range(len(words)):
        fla = False
        for X, p in getGrammarLexicalRules(grammar, words[i]):
            P[X + '/' + str(i) + '/' + str(i)] = p
            T[X + '/' + str(i) + '/' + str(i)] = Tree.Tree(X,
                                                           None, None, lexiconItem=words[i])
            fla = True
        if fla == False:
            return None, None

    printV('T:', [str(t)+':'+str(T[t]) for t in T])
    printV("")

    for i, j, k in subspans(len(words)):
        # ['S', 'NP', 'VP', 0.9 * 0.45 * 0.6]
        for X, Y, Z, p in getGrammarSyntaxRules(grammar):
            if(Z != ''):

                # printV('i:', i, 'j:', j, 'k:', k, '', X, '->', Y, Z, '['+str(p)+']',
                #        'PYZ =', getP(Y, i, j), getP(Z, j+1, k), p, '=', getP(Y, i, j) * getP(Z, j+1, k) * p)

                PYZ = getP(Y, i, j) * getP(Z, j+1, k) * p
                if PYZ > getP(X, i, k):
                    P[X + '/' + str(i) + '/' + str(k)] = PYZ
                    T[X + '/' + str(i) + '/' + str(k)] = Tree.Tree(X,
                                                                   T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)])

                    # printV('inserting from', i, '-', k, ' ', X, '->', T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)], 'because', PYZ, '=', getP(
                    #     Y, i, j), '*', getP(Z, j+1, k), '*', p, '>', getP(X, i, k), '=', 'getP(' + X + ',' + str(i) + ',' + str(k) + ')')

            else:
                PYZ = getP(Y, j, k) * p
                if PYZ > getP(X, i, k):
                    printV('     inserting from', i, '-', k, ' ', X, '->', T[X+'/'+str(i)+'/'+str(i)], T[Y+'/'+str(j)+'/'+str(k)],
                           'because', PYZ, '=', getP(
                               Y, j, k), '*', p, '>', getP(X, j, k), '=',
                           'getP(' + X + ',' + str(j) + ',' + str(k) + ')')
                    P[X + '/' + str(i) + '/' + str(k)] = PYZ
                    T[X + '/' + str(i) + '/' + str(k)] = Tree.Tree(X,
                                                                   T[X+'/'+str(i)+'/'+str(i)], T[Y+'/'+str(j)+'/'+str(k)])

    printV('T:', [str(t)+':'+str(T[t]) for t in T])
    return T, P


# Python uses 0-based indexing, requiring some changes from the book's
# 1-based indexing: i starts at 0 instead of
def subspans(N):
    for length in range(2, N+1):
        for i in range(N+1 - length):
            k = i + length - 1
            for j in range(i, k):
                yield i, j, k


# These two getXXX functions use yield instead of return so that a single pair can be sent back,
# and since that pair is a tuple, Python permits a friendly 'X, p' syntax
# in the calling routine.
def getGrammarLexicalRules(grammar, word):
    for rule in grammar['lexicon']:
        if rule[1] == word:
            yield rule[0], rule[2]


def getGrammarSyntaxRules(grammar):
    rulelist = []
    for rule in grammar['syntax']:
        if(len(rule) == 4):
            yield rule[0], rule[1], rule[2], rule[3]
        else:
            yield rule[0], rule[1], '', rule[2]


def getGrammarWeatherC1F():
    return {
        'syntax': [
            ['Greeting', 'Greeting', 'S', 0.25],
            ['S', 'NP', 'VP', 0.25],
            ['S', 'VP', 'NP', 0.25],
            ['S', 'Pronoun', 'VP', 0.25],
            ['Pronoun', 'Pronoun', 'Adjective', 0.25],
            ['S', 'Pronoun', 'S', 0.25],
            ['S', 'WQuestion', 'VP', 0.25],
            ['S', 'WQuestion', 'NP', 0.25],
            ['S', 'WQuestion', 'S', 0.25],
            ['S', 'WQuestion', 'Conj', 0.25],
            ['S', 'S', 'Conj', 0.5],
            ['Conj', 'Conj', 'S', 0.5],
            ['WQuestion', 'Verb', 'Pronoun', 0.25],
            ['WQuestion', 'WQuestion', 'WQuestion', 0.25],
            ['WQuestion', 'WQuestion', 'Adjective', 0.25],
            ['S', 'Time', 'AdverbPhrase', 0.25],
            ['S', 'Time', 'AdverbPhrase', 0.25],
            ['S', 'AdverbPhrase', 'S', 0.1],
            ['S', 'WQuestion', 'NP+AdverbPhrase', 0.25],
            ['VP', 'Verb', 'Name', 0.2],
            ['VP', 'Verb', 'Noun', 0.2],
            ['VP', 'VP', 'Time', 0.2],
            ['VP', 'WQuestion', 'Verb', 0.1],
            ['VP', 'Verb', 'NP', 0.1],
            ['VP', 'NP', 'Verb', 0.1],
            ['VP', 'VP', 'Adjective', 0.1],
            ['VP', 'Verb', 'AdverbPhrase', 0.1],
            ['VP', 'Time', 'VP', 0.6 * 0.15],
            ['VP', 'Verb', 'Adjective', 0.6 * 0.15],
            ['VP', 'Verb', 'S', 0.3],
            ['NP', 'Article', 'Noun', 0.5],
            ['NP', 'Article', 'NP', 0.5],
            ['NP', 'Article', 'Time', 0.5],
            ['NP', 'Preposition', 'NP', 0.5],
            ['NP', 'NP', 'Time', 0.5],
            ['NP', 'NP', 'Noun', 0.5],
            ['NP', 'Adjective', 'Noun', 0.5],
            ['NP', 'Adjective', 'AdverbPhrase', 0.8],
            ['NP', 'Adjective', 'Time', 0.8],
            ['Adjective', 'Adjective', 'Adjective', 0.8],
            ['S', 'NP', 'AdverbPhrase', 0.2],
            ['AdverbPhrase', 'Preposition', 'Adress', 0.2],
            ['AdverbPhrase', 'Preposition', 'AdverbPhrase', 0.2],
            ['AdverbPhrase', 'Time', 'AdverbPhrase', 0.2],
            ['AdverbPhrase', 'AdverbPhrase', 'Time', 0.2],
            ['AdverbPhrase', 'Noun', 'AdverbPhrase', 0.2],
            ['Time', 'Preposition', 'Time', 0.6],
            ['Time', 'Num', 'Time', 0.6],
            ['Conj', 'Conj', 'Conj', 0.25],
        ],
        'lexicon': [
            ['Greeting', 'hi', 0.5],
            ['Greeting', 'hello', 0.5],
            ['WQuestion', 'what', 0.5],
            ['WQuestion', 'will', 0.5],
            ['WQuestion', 'when', 0.25],
            ['WQuestion', 'which', 0.25],
            ['WQuestion', 'how’s', 0.25],
            ['WQuestion', 'how', 0.25],
            ['Verb', 'am', 0.5],
            ['Verb', 'are', 0.5],
            ['Verb', 'is', 0.5],
            ['Verb', 'be', 0.5],
            ['Verb', 'was', 0.5],
            ['Verb', 'change', 0.5],
            ['Verb', 'tell', 0.5],
            ['Verb', 'wear', 0.5],
            ['Verb', 'should', 0.5],
            ['Verb', 'bring', 0.5],
            ['Verb', 'go', 0.5],
            ['Verb', 'compared', 0.5],
            ['Name', 'peter', 0.1],
            ['Name', 'sue', 0.1],
            ['Adress', 'irvine', 0.8],
            ['Adress', 'bakersfield', 0.8],
            ['Adress', 'riverside', 0.8],
            ['Adress', 'stockton', 0.8],
            ['Adress', 'fresno', 0.8],
            ['Adress', 'fremont', 0.8],
            ['Adress', 'sacramento', 0.8],
            ['Adress', 'oakland', 0.8],
            ['Adress', 'modesto', 0.8],
            ['Adress', 'anaheim', 0.8],
            ['Adress', 'tustin', 0.8],
            ['Adress', 'pasadena', 0.8],
            ['Pronoun', 'i', 1.0],
            ['Pronoun', 'it', 1.0],
            ['Noun', 'there', 1.0],
            ['Noun', 'man', 0.2],
            ['Noun', 'name', 0.2],
            ['Noun', 'temperature', 0.6],
            ['Noun', 'weather', 0.6],
            ['Noun', 'sunglasses', 0.6],
            ['Noun', 'clothes', 0.6],
            ['Article', 'the', 0.7],
            ['Article', 'a', 0.3],
            ['Adjective', 'my', 1.0],
            ['Adjective', 'me', 1.0],
            ['Adjective', 'hotter', 0.5],
            ['Adjective', 'future', 0.5],
            ['Adjective', 'suitable', 0.5],
            ['Adjective', 'okay', 0.5],
            ['Adjective', 'too', 0.5],
            ['Adjective', 'much', 0.5],
            ['Adjective', 'windy', 0.5],
            ['Adjective', 'still', 0.5],
            ['Time', 'now', 0.4],
            ['Time', 'yesterday', 0.3],
            ['Time', 'today', 0.3],
            ['Time', 'today’s', 0.3],
            ['Time', 'tomorrow', 0.3],
            ['Time', 'tomorrow’s', 0.3],
            ['Time', '5-day', 0.3],
            ['Time', '4-day', 0.3],
            ['Time', '3-day', 0.3],
            ['Time', '2-day', 0.3],
            ['Time', 'days', 0.3],
            ['Time', 'day', 0.3],
            ['Time', 'hours', 0.3],
            ['Time', 'hour', 0.3],
            ['Num', '1', 0.3],
            ['Num', '2', 0.3],
            ['Num', '3', 0.3],
            ['Num', '4', 0.3],
            ['Num', '5', 0.3],
            ['Num', '6', 0.3],
            ['Num', '7', 0.3],
            ['Num', '8', 0.3],
            ['Num', '9', 0.3],
            ['Num', '10', 0.3],
            ['Conj', 'if', 0.3],
            ['Conj', 'that', 0.3],
            ['Preposition', 'with', 0.5],
            ['Preposition', 'after', 0.5],
            ['Preposition', 'than', 1],
            ['Preposition', 'in', 0.5],
            ['Preposition', 'on', 0.5],
            ['Preposition', 'to', 0.5],
            ['Preposition', 'like', 0.5]
        ]
    }


# Unit testing code
if __name__ == '__main__':
    verbose = True
    CYKParse("hi my name is Peter".replace(
        ',', '').lower().split(' '), getGrammarWeatherC1F())
