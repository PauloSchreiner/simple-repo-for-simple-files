#Paulo Schreiner, June 2019
#The code is probably confusing. I lack patience to comment it all

import webbrowser
import time
from random import choice
import argparse
from datetime import datetime
import re

argparse = argparse.ArgumentParser(description='Set a timer to open urls in your default browser.')
argparse.add_argument('-w','--when',nargs='?',type=str,default=None,help='When to open the url. Enter the hour (0 to 23), followed by any non-digit (except space) and the minutes.')
argparse.add_argument('-l','--minslater',nargs='?',type=int,default=1,help='Minutes to wait to open the url. Default: 1.')
argparse.add_argument('-u','--url',nargs='?',type=str,default='',help='Enter a specific url to open.')
argparse.add_argument('-a','--addurl',nargs='?',type=str,default='',help='Add an url to urlsFile.txt. To add multiple urls, set to "multiple".')
argparse.add_argument('-o','--open',nargs='?',type=(lambda x:(str(x).lower() == 'true')),default=True,help='To open a random url from urlsFile.txt or not. Default: True.')
argparse.add_argument('-r','--remove',nargs='?',type=(lambda x:(str(x).lower() == 'true')),default=False,help='to remove opened url from urlsFile.txt or not. Default: False.')
args = argparse.parse_args()

urlsFileName = 'urlsFile.txt'

#Calculate seconds passed since 00:00
nowList = str(datetime.now().time()).split(':')
def SecNow(): return int(nowList[0])*3600 + int(nowList[1])*60 + round(float(nowList[2]))

#Print start time
timeNow = str(datetime.now().time()).split(':')
print(timeNow[0]+':'+timeNow[1])

#If given url is not in a url format or an empty string, format it to be so.
urlRegex = '(https://)*www[.].+[.]com.*'
def toUrlFormat(url):
    if (not re.search(urlRegex, url)) and url != '':
        url = 'https://www.{}.com'.format(url)
    return url

toUrlFormat(args.url)

#Accept multiple urls and add to urlsFile.txt
if args.addurl == 'multiple':
    urlsList = []
    print('Enter the urls. To stop, enter "stop".')
    while True:
        inpUrl = input('Url to append: ')
        if inpUrl == 'stop':
            break
        urlsList.append(toUrlFormat(inpUrl))
    with open(urlsFileName,'a') as urlsFile:
        for url in urlsList:
            if url:
                urlsFile.write(url+'\n')
    print('Urls added successfully!')
else: #Append args.addurl to urlsFile.txt
    if args.addurl:
        args.addurl = toUrlFormat(args.addurl)
        with open(urlsFileName,'a') as urlsFile:
            urlsFile.write(args.addurl+'\n')
            print('Url added successfully!')

#Only sleep and open url if args.open == True
if args.open == True:
    #If args.when exists, sleep for the amount os seconds until given time
    if args.when: 
        when_list = re.findall('\d+', args.when)
        when = ((int(when_list[0])*60)+int(when_list[1]))*60
        toSleep = when-SecNow()
        if toSleep < -30000: #To accept 12h formatted time. Not precise, it is preferable to aways use 24hs
            toSleep += 43200
        elif toSleep < 0:
            toSleep = 0
            print("Time doesn't run backwards.")
        print('Sleeping for {} minute(s).'.format(round(toSleep/60)))
        time.sleep(toSleep)
    #If args.when does not exist, appeal to args.later (that has default of 1 minute)
    else:
        print('Sleeping for {} minute(s).'.format(args.minslater))
        time.sleep(args.minslater*60)
    #If args.url exists, let the string content be equal to it.
    if args.url:
        content = args.url
    else:
        with open(urlsFileName,'r') as urlsFile:
            fileContents = urlsFile.read().split('\n')
            content = random.choice(fileContents)
    try:
        print('Opening url.')
        time.sleep(0.3)
        webbrowser.open(content)
    except Exception as e:
        print('An error occured while opening the url.\nError message:',e)
    if args.remove:
        with open(urlsFileName,'r+') as urlsFile:
            data = urlsFile.read()
            urlsFile.seek(0)
            result = data.replace(content,'').strip() + '\n'
            urlsFile.write(result)
            urlsFile.truncate()
            print('Url removed from {} successfully!'.format(urlsFileName))

'''
if the webbrowser module is not opening your default browser, replace webbrowser.open(content) with:

browser = 'chrome' #change accordingly
pathToBrowser = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" #change accordingly
webbrowser.register(browser,None,webbrowser.BackgroundBrowser(pathToBrowser))
webbrowser.get(browser).open(content) 
'''
