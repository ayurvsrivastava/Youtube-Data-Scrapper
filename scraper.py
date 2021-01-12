#Imports from Needed Libraries
from requests_html import HTMLSession 
from bs4 import BeautifulSoup as bs

# Creates HTML Session through Requests Library
requestSession = HTMLSession()

# Function to get data from Video
def videoDataScraper(videoUrl, convertInteger):

    #Create HTML File for Video
    createHtml  = requestSession.get(videoUrl)

    #Javscript Function to Render Data into HTML
    createHtml.html.render(sleep = 1)

    #Use Beautiful Soup library to create beatiful soup opject
    beautifulSoup = bs(createHtml.html.html, "html.parser")

    #Intialize Result Storage
    scrappedData = {}

    #Store data into scrappedData
    scrappedData["Title"] = beautifulSoup.find("h1").text.strip()

    #Converts Number of Views to Integer if True
    if convertInteger:
        numberOfView = beautifulSoup.find("span", attrs = {"class": "view-count"}).text
        numberOfView = numberOfView.replace(',','')
        numberOfView = numberOfView.replace(' views','')
        scrappedData["Number_of_Views"] = int(numberOfView)
    else: 
        scrappedData["Number_of_Views"] = beautifulSoup.find("span", attrs={"class": "view-count"}).text

    scrappedData["Video_Description"] = beautifulSoup.find("yt-formatted-string", {"class": "content"}).text
    scrappedData["Date_Published"] = beautifulSoup.find("div", {"id": "date"}).text[1:]
    scrappedData["Video_Length"] = beautifulSoup.find("span", {"class": "ytp-time-duration"}).text

    #Convert Number of Likes/Dislikes into Integer if True
    if convertInteger:
        numberOfLikes = beautifulSoup.find_all("yt-formatted-string", {"id": "text", "class": "ytd-toggle-button-renderer"})[0].text
        numberOfLikes = numberOfLikes.replace('K','000')
        scrappedData["Number_of_Likes"] = int(numberOfLikes)
        numberOfDislikes = beautifulSoup.find_all("yt-formatted-string", {"id": "text", "class": "ytd-toggle-button-renderer"})[1].text
        numberOfDislikes = numberOfDislikes.replace('K','000')
        scrappedData["Number_of_Disikes"] = int(numberOfDislikes)
    else:
        scrappedData["Number_of_Likes"] = beautifulSoup.find_all("yt-formatted-string", {"id": "text", "class": "ytd-toggle-button-renderer"})[0].text
        scrappedData["Number_of_Disikes"] = beautifulSoup.find_all("yt-formatted-string", {"id": "text", "class": "ytd-toggle-button-renderer"})[1].text
    
    scrappedData["Channel_Name"] = beautifulSoup.find("yt-formatted-string", {"class": "ytd-channel-name"}).text

    return scrappedData

#Ask User Input for Youtube Video
videoUrl = input("Please Input Youtube Video Url including the https:// portion: ")

#Ask for Integer Conversion (default is False)
correctInput = False
convertInteger = False

while correctInput == False:

    convertToInt = input("Would you like to convert the Number of Views, Likes, and Dislikes into integers? Input Y/N ")

    #Check Input
    if convertToInt == 'Y' or convertToInt == 'y':
        convertInteger = True
        correctInput = True
    elif convertToInt == 'N' or convertToInt == 'n':
        convertInteger = False
        correctInput = True
    else: 
        print (" Please Input a Valid Answer ")

#Gather Data from Video
scrappedData = videoDataScraper( videoUrl, convertInteger)

#Print Data As A String
for column in scrappedData:
    print (column + ": " + str(scrappedData[column]))


