#This applicaiton was designed to send out a daily email to friends with a quote from the office
#By Broderick Lemke 2018

import requests
import random
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys
import datetime

numberOfAttempts = 0
successfulRetrieval = False


def getOfficeQuote():
    '''
    This function gets a random quote from a random season of the office
    '''

    #pick a random season of the office
    randSeason = random.randint(1,9)

    #Check the API to see what episodes are in season
    url = "https://the-office-api.herokuapp.com/season/" + str(randSeason) + "/format/connections"
    response = requests.get(url)
    
    #If the response does nocome back
    if response.status_code != 200:
        global numberOfAttempts
        ++numberOfAttempts
    else:
        #response came back, get the number of episodes
        seasonData = response.json()
        numberOfEpisodes = len(seasonData["data"])
        randomEpisode = random.randint(1,numberOfEpisodes)
        quoteUrl = "https://the-office-api.herokuapp.com/season/" + str(randSeason) + "/episode/" + str(randomEpisode)
        
        #Go get the quotes for this episode of this season
        quoteResponse = requests.get(quoteUrl)

        #Retrieval failes
        if quoteResponse.status_code !=200:
                ++numberOfAttempts
        else:
                episodeData = quoteResponse.json()
                quotes = episodeData["data"]["quotes"]
                episodeName = episodeData["data"]["name"]
                randomQuote = random.choice(quotes)

                #quote retrieved successfully, mark it as such
                global successfulRetrieval
                successfulRetrieval = True

                #Format quote from a list into a string
                quoteString = "Enjoy this quote from Season " + str(randSeason) + " Episode " + str(randomEpisode) + ": " + episodeName +  ".\n\n\n"
                for line in randomQuote:
                    quoteString += line + " \n "

                randomQuoteDict = {"Quote" : quoteString, "Season": randSeason, "Episode": randomEpisode}
                return randomQuoteDict


def sendEmail(quoteDict, toEmail):
    '''
    Function to create an email server and send out an email with the office quote 
    '''

    try:
        #Setup SMTP email server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        #retrieveLoginInfo
        with open(os.path.join(sys.path[0], 'login.txt')) as f:
            serverData = json.load(f)
        serverUsername = serverData["username"]
        serverPassword = serverData["pass"]

        server.login(serverUsername, serverPassword)

        #create email
        fromAddress = "dailyofficerquotes@gmail.com"
        toAddress = toEmail
        msg = MIMEMultipart()
        msg["FROM"] = fromAddress
        msg["To"] = toAddress
        
        todaysDate = str(datetime.datetime.today().month) + "/" + str(datetime.datetime.today().day) + "/" + str(datetime.datetime.today().year)
        msg["Subject"] = todaysDate + " - Your Daily Office Quote: From Season " + str(quoteDict["Season"]) + " Episode " + str(quoteDict["Episode"])

        #Attach the body of the email that's passed in as a parameter
        msg.attach(MIMEText(quoteDict["Quote"],'plain'))  

        text = msg.as_string()

        server.sendmail(fromAddress, toAddress, text)

        return 1
    except:
        #email failed to send, return a failure code
        return -1


### Execute the script
print("Retrieving a quote...")

while numberOfAttempts <= 3 and successfulRetrieval == False:
   #try to retrieve a quote
   dailyQuote = getOfficeQuote()
   if numberOfAttempts > 0:
       print("   Ooops, we didn't like that one, let's try again...")

if successfulRetrieval:
    print("Quote Retrieved... Sending....")

    #retrieve emails
    with open(os.path.join(sys.path[0], 'emails.txt')) as emailF:
        emailListDict = json.load(emailF)
    emailList = emailListDict["Emails"]

    #send the daily quote to each email in the email list
    for email in emailList:
        emailSentResponse = sendEmail(dailyQuote, email)
        if emailSentResponse == 1:
                print("Quote sent to " + email)
        else:
                print("Error sending quote to " + email)   
else:
    print("Error retrieving quote... sending bug message")
    errorDict = {"Quote" : "Something went wrong, no quote for you", "Season": 0, "Episode": 0}
    sendEmail(errorDict, "blemke4@gmail.com")