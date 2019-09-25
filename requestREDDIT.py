import requests
from io import BytesIO
from PIL import Image, ImageTk
import tkinter
from bs4 import BeautifulSoup
import json
import pprint

class requestREDDIT:

    #Get the initial memes
    initUrl = "https://www.reddit.com/r/dankmemes"
    response = requests.get(initUrl, headers = {'User-agent': 'memeGetter'})
    result = BeautifulSoup(response.text, "html.parser")
    nextCursor = result.find('script', attrs={"id": "data"}).string
    nextCursor = nextCursor[len("window.___r = "):-len('; window.___prefetches = ["https://www.redditstatic.com/desktop2x/CommentsPage.de9277da3ad416d48d12.js","https://www.redditstatic.com/desktop2x/Frontpage.7bd472251f4aea026105.js"];')]
    jsonResponse = json.loads(nextCursor)
    nextCursor = jsonResponse['listings']['postOrder']['ids']["dankmemes--[sort:'hot']"][0]

    initUrl = "https://gateway.reddit.com/desktopapi/v1/subreddits/dankmemes?after=%s" % nextCursor
    response = requests.get(initUrl, headers={'User-agent': 'memeGetter'})
    jsonResponse = response.json()
    amountOfMemes = int(len(jsonResponse['postIds'])) - 1
    nextCursor = jsonResponse['postIds'][amountOfMemes]

    def displayNextImage(self, id: str, imageLabel: tkinter.Label):
        if int(self.jsonResponse['posts'][id]['media']['width']) >= 960:
            image = requests.get(self.jsonResponse['posts'][id]['media']['resolutions'][4]['url'])
        else:
            image = requests.get(self.jsonResponse['posts'][id]['media']['content'])
        i = Image.open(BytesIO(image.content))
        img = ImageTk.PhotoImage(i)
        imageLabel.config(image=img)
        imageLabel.image = img
        imageLabel.pack()

    def checkIfLast(self):
        if self.amountOfMemes == 0:
            self.initUrl = "https://gateway.reddit.com/desktopapi/v1/subreddits/dankmemes?after=%s" % self.nextCursor
            self.response = requests.get(self.initUrl, headers={'User-agent': 'memeGetter'})
            self.jsonResponse = self.response.json()
            self.amountOfMemes = int(len(self.jsonResponse['postIds'])) - 1
            self.nextCursor = self.jsonResponse['postIds'][self.amountOfMemes]

    def callback(self, voteLabel: tkinter.Label, imageLabel: tkinter.Label, titleLabel: tkinter.Label):
        print("Another reddit meme please")
        intId = (int(len(self.jsonResponse['postIds'])) - 1) - self.amountOfMemes

        #Check if its not a picture, and before if it its sponsored
        if self.jsonResponse['posts'][self.jsonResponse['postIds'][intId]]['isSponsored'] == True:
            self.amountOfMemes = self.amountOfMemes - 1
            self.checkIfLast()
            return self.callback(voteLabel, imageLabel, titleLabel)
        elif str(self.jsonResponse['posts'][self.jsonResponse['postIds'][intId]]['media']['type']) != "image":
            self.amountOfMemes = self.amountOfMemes - 1
            self.checkIfLast()
            return self.callback(voteLabel, imageLabel, titleLabel)

        #Check if it has the nessecary amount of upvotes
        elif int(self.jsonResponse['posts'][self.jsonResponse['postIds'][intId]]['score']) <= 500:
            self.amountOfMemes = self.amountOfMemes - 1
            self.checkIfLast()
            return self.callback(voteLabel, imageLabel, titleLabel)

        #Otherwise go ahead!!
        else:
            identifier = self.jsonResponse['posts'][self.jsonResponse['postIds'][intId]]['id']
            votes = "Amount of upvotes: " + str(self.jsonResponse['posts'][identifier]['score'])
            voteLabel.config(text=votes)
            title = self.jsonResponse['posts'][self.jsonResponse['postIds'][intId]]['title'].encode('utf-8')
            titleLabel.config(text=title)
            self.amountOfMemes = self.amountOfMemes - 1
            self.displayNextImage(identifier, imageLabel)
            self.checkIfLast()
