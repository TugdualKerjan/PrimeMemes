import tkinter as tk
from request9GAG import request9GAG
#from requestREDDIT import requestREDDIT
#from requestIFUNNY import requestIFUNNY

request9gagmemes = request9GAG()
#requestredditmemes = requestREDDIT()
#requestifunnymemes = requestIFUNNY()

def more9gagmemes():
    request9gagmemes.callback(voteLabel, imageLabel, titleLabel)

#def moreredditmemes():
#    requestredditmemes.callback(voteLabel, imageLabel, titleLabel)

#def moreifunnymemes():
#    requestifunnymemes.callback(voteLabel, imageLabel, titleLabel)


###Display the window for the memes
window = tk.Tk()
window.title("Beta quality memes")
window.pack_propagate(0)
window.geometry("960x1080")

voteLabel = tk.Label(window, text="Votes will appear here")
titleLabel = tk.Label(window, text="Title will appear here")
imageLabel = tk.Label(window, relief="sunken")
b = tk.Button(window, text="More quality memes from 9GAG", command=more9gagmemes, width=960,cursor="mouse")
#b1 = tk.Button(window, text="More quality memes from Reddit", command=moreredditmemes, width=960,cursor="mouse")
#b2 = tk.Button(window, text="More quality memes from iFunny", command=moreifunnymemes, width=960,cursor="mouse")

b.pack()
#b1.pack()
#b2.pack()
voteLabel.pack()
titleLabel.pack()
imageLabel.pack()

tk.mainloop()