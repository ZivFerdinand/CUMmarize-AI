import tkinter as tk
import nltk
from textblob import TextBlob
from newspaper import Article

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/text', methods =["GET", "POST"])
def text():
    if request.method == "POST":
       urlLink = request.form.get("url")
       nltk.download('punkt')
       article = Article(urlLink)
       article.download()
       article.parse()
       article.nlp()
       return "Title : " + article.title + "<br>" + "Authors : " + str(article.authors) + "<br>" + "Publication Date : " + str(article.publish_date) + "<br> </br>" + "Summary : <br>" + article.summary
    return render_template("text.html")



if __name__ == "__main__":
    app.run(debug=True)

# import whisper

# model = whisper.load_model("medium")
# result = model.transcribe("C:\\Users\\bcamaster\\OneDrive\\Documents\\Code\\Code Cawu 3\\CUMmarize-AI\\18.mp4")

# print(result["text"])