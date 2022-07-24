import CYKParse
import Tree
import requests
import time
from datetime import datetime
import json

requestInfo = {
    'name': '',
    'location': '',
    'num': '',
    'day': '',
    'hour': '',
    'wear': '',
}
haveGreeted = False


# generate weather api url
def getWeatherUrl(city):
    return "https://api.openweathermap.org/data/2.5/forecast?q="+city+"&units=imperial&appid=68d9091ad07e6dafa1f88720eec57fea"


# Given the collection of parse trees returned by CYKParse, this function
# returns the one corresponding to the complete sentence.
def getSentenceParse(T):
    sentenceTrees = {k: v for k, v in T.items() if k.startswith(
        'S/0') or k.startswith('Greeting/0')}
    completeSentenceTree = ''
    for key in sentenceTrees.keys():
        completeSentenceTree = key
    if completeSentenceTree == '':
        return None
    return T[completeSentenceTree]


# Processes the leaves of the parse tree to pull out the user's request.
def updateRequestInfo(Tr):
    global requestInfo
    lookingForLocation = False
    lookingForName = False

    for leaf in Tr.getLeaves():
        # print(leaf)
        if leaf[0] == 'Time':
            if 'hour' in leaf[1]:
                requestInfo['hour'] = leaf[1]
            elif 'day' in leaf[1]:
                requestInfo['day'] = leaf[1]

        if leaf[0] == 'Num':
            requestInfo['num'] = leaf[1]
        if leaf[0] == 'Adress':
            requestInfo['location'] = leaf[1]
        if leaf[0] == 'Name':
            requestInfo['name'] = leaf[1]
        if 'wear' in leaf[1]:
            requestInfo['wear'] = leaf[1]
    # print(requestInfo)


# Choosing what to wear
def get_clothes(weather):
    if weather.get('clouds').get('all') < 10:
        print('bot: It should be sunny, so a hat or sunglasses might be needed')
    if weather.get('rain') != None:
        if weather.get('rain').get('3h')*100 == 0:
            print("bot: It's not going to rain, so no umbrella is needed")
        elif weather.get('rain').get('3h')*100/3 < 2.5:
            print("bot: There'll be light rain, so consider a hood or umbrella")
        elif weather.get('rain').get('3h')*100/3 < 7.6:
            print("bot: There'll be moderate rain, so an umbrella is probably needed")
        elif weather.get('rain').get('3h')*100/3 < 50:
            print(
                "bot: There'll be heavy rain, so you'll need an umbrella and a waterproof top")
        elif weather.get('rain').get('3h')*100/3 > 50:
            print("bot: There'll be violent rain, so wear a life-jacket")
    if weather.get('main').get('temp') < 31.7:
        print("bot: It's going to be freezing, so take a heavy coat")
    elif weather.get('main').get('temp') < 49.7:
        print("bot: It's going to be cold, so a coat or thick jumper might be sensible")
    elif weather.get('main').get('temp') < 67.7:
        print("bot: It's not too cold, but you might consider taking a light jumper")
    elif weather.get('main').get('temp') < 85.7:
        print("bot: Shorts and T-shirt weather :)")
    if weather.get('wind').get('speed') > 30:
        print("bot: There'll be wind, so a jacket might be useful")
    elif weather.get('wind').get('speed') > 10:
        print("bot: There'll be a light breeze, so maybe long sleeves might be useful")
    else:
        print("bot: The air will be quite calm, so no need to worry about wind")


# This function contains the data known by our simple chatbot
def getTemperature(location, hour, day):
    time_now = time.time()
    time_forecast = time_now + int(hour)*60*60 + int(day)*24*60*60
    try:
        r = requests.get(getWeatherUrl(location))
        j = json.loads(r.text)
        for data in j.get('list'):
            if(data.get('dt') > time_forecast):
                return data
        for data in j.get('list'):
            last = data
        return last
    except:
        return None


# Format a reply to the user, based on what the user wrote.
def reply():
    global requestInfo
    global haveGreeted
    result = 'bot: '
    if not haveGreeted and requestInfo['name'] != '':
        print("Hello", requestInfo['name'] + '.')
        haveGreeted = True
        return
    if requestInfo['name'] != '':
        result += requestInfo['name'] + ','

    if requestInfo.get('location') != '' and (requestInfo.get('day') != '' or requestInfo.get('hour') != ''):
        if requestInfo.get('day') != '':
            requestInfo['hour'] = 0
            if '-' in requestInfo.get('day'):
                requestInfo['day'] = str(requestInfo.get('day')).split('-')[0]
            elif 'today' in requestInfo.get('day'):
                requestInfo['day'] = 0
            else:
                requestInfo['day'] = requestInfo.get('num')
        if requestInfo.get('hour') != '' and requestInfo.get('hour') != 0:
            requestInfo['day'] = 0
            requestInfo['hour'] = requestInfo.get('num')

        print('bot: Checking the weather for you...')
        # print(requestInfo)
        weather = getTemperature(requestInfo.get('location'),
                                 requestInfo.get('hour'), requestInfo.get('day'))

        if weather is None:
            result += 'Something seems wrong'
            requestInfo['day'] = ''
            requestInfo['num'] = ''
            requestInfo['hour'] = ''
            requestInfo['wear'] = ''
            print(result)
            return
        else:
            # print(weather)
            if requestInfo.get('wear') == '':
                if(int(requestInfo['day']) > 0):
                    result += 'at that time the temperature on ' + requestInfo.get('location') + ' is ' + str(weather.get('main').get(
                        'temp')) + ' Fahrenheit on mean,with ' + weather.get('weather')[0].get('description')+'.'
                    print(result)
                    print('bot: are you going to', requestInfo.get('location'), 'for',
                          requestInfo.get('day'), 'day?')
                    res = input(':')
                    if 'n' in res:
                        return
                    print('bot: do you need me to recommendate the clothes for you?')
                    res = input(':')
                    if 'n' in res:
                        return
                    get_clothes(weather)
                    requestInfo['day'] = ''
                    requestInfo['num'] = ''
                    requestInfo['hour'] = ''
                    requestInfo['wear'] = ''
                    return
                else:
                    result += 'the temperature on ' + requestInfo.get('location') + ' is ' + str(weather.get('main').get(
                        'temp')) + ' Fahrenheit on mean,with ' + weather.get('weather')[0].get('description')+'.'
                    print(result)
                    print('bot: How’s your feeling today?')
                    requestInfo['day'] = ''
                    requestInfo['num'] = ''
                    requestInfo['hour'] = ''
                    requestInfo['wear'] = ''
                    return
            else:
                result += 'i am no sure what you need to wear,but according to the weather following recommend may be useful'
                print(result)
                get_clothes(weather)
                print('bot: by the way,you look great all the day!')
                requestInfo['day'] = ''
                requestInfo['num'] = ''
                requestInfo['hour'] = ''
                requestInfo['wear'] = ''
    else:
        result += 'i dont know where you are'
        requestInfo['day'] = ''
        requestInfo['num'] = ''
        requestInfo['hour'] = ''
        requestInfo['wear'] = ''
        print(result)
# A simple hard-coded proof of concept.


def main():
    #getTemperature('Pasadena', 3, 0)
    global requestInfo
    while True:
        print()
        str_input = input('you: ')
        T, P = CYKParse.CYKParse(
            str_input.replace(',', '').lower().split(' '), CYKParse.getGrammarWeatherC1F())
        if T is None:
            print("bot: sorry i don't know what you mean, would you mink ask again?")
            continue
        sentenceTree = getSentenceParse(T)
        if sentenceTree is None:
            print("bot: sorry i don't know what you mean, would you mink ask again?")
            continue
        updateRequestInfo(sentenceTree)
        reply()


# hi my name is Peter

# today’s weather on bakersfield
# How’s the weather in Pasadena today
# In Pasadena, how’s the weather today

# future 5-day weather on Tustin
# How’s future 2-day weather on Pasadena
# How will the weather change in the future 5 days in Pasadena
# In Tustin, tell me the future 5 days weather

# Is it suitable that if I wear sunglasses today
# Is it okay if I wear sunglasses today
# will it be too much if I wear sunglasses today

# will it still be windy after 5 hours on Pasadena
# In Pasadena, how’s the weather be like after 4 hours

# What should I bring if I will go to Pasadena in 4 days
# What should I wear if I will go to Pasadena in 4 days

main()
