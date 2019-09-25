import requests
from io import BytesIO
from PIL import Image,ImageTk
import tkinter


class request9GAG:

    # Get the initial memes
    response = requests.get("http://9gag.com")
    jsonResponse = response.text
    position = jsonResponse.find('"position":1,"url":"https:\\/\\/9gag.com\\/gag\\/')
    position = position + len('"position":1,"url":"https:\\/\\/9gag.com\\/gag\\/')
    nextCursor = jsonResponse[position:position + 7]
    initUrl = "https://9gag.com/v1/group-posts/group/default/type/hot?%s" % nextCursor
    response = requests.get(initUrl)
    jsonResponse = response.json()
    amountOfMemes = int(len(jsonResponse['data']['posts'])) - 1
    nextCursor = jsonResponse['data']['nextCursor']

    def displayNextImage(self, string: str, imageLabel: tkinter.Label):
        print(string)
        image = requests.get("https://img-9gag-fun.9cache.com/photo/%s_460s.jpg" % string)
        i = Image.open(BytesIO(image.content))
        img = ImageTk.PhotoImage(i)
        imageLabel.config(image=img)
        imageLabel.image = img
        imageLabel.pack()

    def checkIfLast(self):
        if self.amountOfMemes == 0:
            self.initUrl = "https://9gag.com/v1/group-posts/group/default/type/hot?%s" % self.nextCursor
            self.response = requests.get(self.initUrl)
            self.jsonResponse = self.response.json()
            self.amountOfMemes = int(len(self.jsonResponse['data']['posts'])) - 1
            self.nextCursor = self.jsonResponse['data']['nextCursor']

    def callback(self, voteLabel: tkinter.Label, imageLabel: tkinter.Label, titleLabel: tkinter.Label):
        print("Another 9GAG meme please")

        if self.jsonResponse['data']['posts'][self.amountOfMemes]['type'] != "Photo":
            self.amountOfMemes = self.amountOfMemes - 1
            self.checkIfLast()
            return self.callback(voteLabel, imageLabel, titleLabel)
        elif int(self.jsonResponse['data']['posts'][self.amountOfMemes]['upVoteCount']) <= 5000:
            self.amountOfMemes = self.amountOfMemes - 1
            self.checkIfLast()
            return self.callback(voteLabel, imageLabel, titleLabel)
        else:
            identifier = self.jsonResponse['data']['posts'][self.amountOfMemes]['id']
            votes = "Amount of upvotes: " + str(self.jsonResponse['data']['posts'][self.amountOfMemes]['upVoteCount'])
            voteLabel.config(text=votes)
            titleLabel.config(text=self.jsonResponse['data']['posts'][self.amountOfMemes]['title'])
            self.amountOfMemes = self.amountOfMemes - 1
            self.displayNextImage(identifier, imageLabel)
            self.checkIfLast()

    def pleaseWork(self):
        print("success")