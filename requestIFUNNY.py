import requests
from io import BytesIO
from PIL import Image,ImageTk
import tkinter
from bs4 import BeautifulSoup


class requestIFUNNY:

    """ Get the initial memes
    response = requests.get("http://9gag.com")
    jsonResponse = response.text
    position = jsonResponse.find('"position":1,"url":"https:\\/\\/9gag.com\\/gag\\/')
    position = position + len('"position":1,"url":"https:\\/\\/9gag.com\\/gag\\/')
    nextCursor = jsonResponse[position:position + 7] """

    listOfMemes = []
    listOfVotes = []
    initUrl = "https://ifunny.co/feeds/featured/RQzAr9h76?batch=6&mode=list"
    response = requests.get(initUrl)
    result = BeautifulSoup(response.text, "html.parser")
    for link in result.find_all(attrs={"class": "media__image"}):
        listOfMemes.append(link['src'])
    amountOfMemes = len(listOfMemes) - 1

    for vote in result.find_all('span', attrs={"class": "actionlink__text"}):
        listOfVotes.append(vote.string)
    listOfVotes = listOfVotes[0::2]

    nextCursor = result.find('a', attrs={"class": "button button_huge button_curved button_deepblue feed__action"}).get('href')
    nextCursor = nextCursor[-9:]
    print(nextCursor)

    def displayNextImage(self, imageLabel: tkinter.Label):
        image = requests.get(self.listOfMemes[self.amountOfMemes])
        i = Image.open(BytesIO(image.content))
        img = ImageTk.PhotoImage(i)
        imageLabel.config(image=img)
        imageLabel.image = img
        imageLabel.pack()

    def checkIfLast(self):
        if self.amountOfMemes == 0:
            self.initUrl = "https://ifunny.co/feeds/featured/{0}?batch=6&mode=list".format(self.nextCursor)
            self.response = requests.get(self.initUrl)
            self.result = BeautifulSoup(self.response.text, "html.parser")
            self.listOfMemes.clear()
            for link in self.result.find_all(attrs={"class": "media__image"}):
                self.listOfMemes.append(link['src'])
            self.amountOfMemes = len(self.listOfMemes) - 1
            for vote in self.result.find_all('span', attrs={"class": "actionlink__text"}):
                self.listOfVotes.append(vote.string)
            self.listOfVotes = self.listOfVotes[0::2]
            self.nextCursor = self.result.find('a', attrs={"class": "button button_huge button_curved button_deepblue feed__action"}).get('href')
            self.nextCursor = self.nextCursor[-9:]
            print(self.nextCursor)

    def callback(self, voteLabel: tkinter.Label, imageLabel: tkinter.Label, titleLabel: tkinter.Label):
        print("Another iFunny meme please")
        votes = self.listOfVotes[self.amountOfMemes]
        votes = votes.replace("K", "")
        voteInt = int(float(votes)) * 1000
        """
        #Check if its not a picture
        
        if self.jsonResponse['data']['posts'][self.amountOfMemes]['type'] != "Photo":
            self.amountOfMemes = self.amountOfMemes - 1
            self.checkIfLast()
            return self.callback(voteLabel, imageLabel, titleLabel)
        #Check if it has the nessecary amount of upvotes"""
        print(voteInt)
        if voteInt <= 50000:
            print(voteInt)
            self.amountOfMemes = self.amountOfMemes - 1
            self.checkIfLast()
            return self.callback(voteLabel, imageLabel, titleLabel)

        #Otherwise go ahead!!
        else:

            #votes has something to do with actionlink__text
            voteLabel.config(text=self.listOfVotes[self.amountOfMemes])
            titleLabel.config(text="No titles on iFunny!")
            self.amountOfMemes = self.amountOfMemes - 1
            self.displayNextImage(imageLabel)
            self.checkIfLast()
