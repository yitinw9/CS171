import CYKParse
import Tree

requestInfo = {
        'name': '',
        'time': '',
        'location': ''
}
haveGreeted = False

# Given the collection of parse trees returned by CYKParse, this function
# returns the one corresponding to the complete sentence.
def getSentenceParse(T):
    sentenceTrees = { k: v for k,v in T.items() if k.startswith('S/0') or k.startswith('Greeting/0')}
    completeSentenceTree = max(sentenceTrees.keys())
    #print('getSentenceParse', completeSentenceTree)
    return T[completeSentenceTree]

# Processes the leaves of the parse tree to pull out the user's request.
def updateRequestInfo(Tr):
    global requestInfo
    lookingForLocation = False
    lookingForName = False
    lookingForTime1 = False
    lookingForTime2 = False
    
    for leaf in Tr.getLeaves():
        #print(leaf)
        if leaf[0] == 'WQuestion' and leaf[1] == 'will':
            lookingForTime1 = True
        if lookingForTime1 and leaf[0] == 'Adverb':
            requestInfo['time1'] = leaf[1]
            lookingForTime1 = False
            continue
        if leaf[0] == 'Preposition' and leaf[1] == 'than':
            lookingForTime2 = True
        if lookingForTime2 and leaf[0] == 'Adverb':
            requestInfo['time2'] = leaf[1]
            lookingForTime2 = False
            continue
        if leaf[0] == 'Adjective':
            requestInfo['compare'] = leaf[1]

        if leaf[0] == 'Adverb':
            requestInfo['time'] = leaf[1]
            requestInfo['time1'] = ''
        if lookingForLocation and leaf[0] == 'Name':
            requestInfo['location'] = leaf[1]
        if leaf[0] == 'Preposition' and leaf[1] == 'in':
            lookingForLocation = True
        else:
            lookingForLocation = False
        if leaf[0] == 'Noun' and leaf[1] == 'name':
            lookingForName = True
        if lookingForName and leaf[0] == 'Name':
            requestInfo['name'] = leaf[1]
    #print(requestInfo)
# This function contains the data known by our simple chatbot
def getTemperature(location, time):
    if location == 'Irvine':
        if time == 'now':
            return '68'
        elif time == 'today':
            return '68'
        elif time == 'tomorrow':
            return '70'
        elif time == 'yesterday':
            return '66'
        else:
            return 'unknown'
    elif location == 'Tustin':
        if time == 'now':
            return '58'
        elif time == 'today':
            return '58'
        elif time == 'tomorrow':
            return '60'
        elif time == 'yesterday':
            return '56'
        else:
            return 'unknown'
    elif location == 'Pasadena':
        if time == 'now':
            return '48'
        elif time == 'today':
            return '48'
        elif time == 'tomorrow':
            return '50'
        elif time == 'yesterday':
            return '46'
        else:
            return 'unknown'
    else:
        return 'unknown'

# Format a reply to the user, based on what the user wrote.
def reply():
    global requestInfo
    global haveGreeted
    if not haveGreeted and requestInfo['name'] != '':
        print("Hello", requestInfo['name'] + '.')
        haveGreeted = True
        return
    time = 'now' # the default
    if requestInfo['time1'] != '':
        if requestInfo['compare'] == 'hotter':
            temp1 = getTemperature(requestInfo['location'],requestInfo['time1'])
            temp2 = getTemperature(requestInfo['location'],requestInfo['time2'])
            salutation = ''
            if requestInfo['name'] != '':
                salutation = 'dear ' + requestInfo['name'] + ', '
            if temp1 > temp2 :
                salutation += requestInfo['time1'] + ' is hotter than ' + requestInfo['time2'] + ' in ' + requestInfo['location']
                print(salutation)
                return
            elif temp1 < temp2:
                salutation += requestInfo['time2'] + ' is hotter than ' + requestInfo['time1'] + ' in ' + requestInfo['location']
                print(salutation)
                return
            elif temp2 == temp1:
                salutation += requestInfo['time2'] + ' and ' + requestInfo['time1'] + ' have the same temperature in ' + requestInfo['location']
                print(salutation)
                return
            else:
                return

    elif requestInfo['time'] != '':
        time = requestInfo['time']
    salutation = ''
    if requestInfo['name'] != '':
        salutation = requestInfo['name'] + ', '
    print(salutation + 'the temperature in ' + requestInfo['location'] + ' ' +
        time + ' is ' + getTemperature(requestInfo['location'], time) + '.')

# A simple hard-coded proof of concept.
def main():
    global requestInfo
    T, P = CYKParse.CYKParse(['hi', 'my', 'name', 'is', 'Peter'], CYKParse.getGrammarWeatherC1F())
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['what', 'is', 'the', 'temperature', 'in', 'Irvine', 'now'], CYKParse.getGrammarWeatherC1F())
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['what', 'was', 'the', 'temperature', 'in', 'Pasadena', 'yesterday'], CYKParse.getGrammarWeatherC1F())
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['what', 'was', 'the', 'temperature', 'in', 'Tustin', 'yesterday'], CYKParse.getGrammarWeatherC1F())
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['will', 'yesterday', 'be', 'hotter', 'than', 'now', 'in', 'Irvine'], CYKParse.getGrammarWeatherC1F())
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['will', 'yesterday', 'be', 'hotter', 'than', 'tomorrow', 'in', 'Pasadena'], CYKParse.getGrammarWeatherC1F())
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

main()