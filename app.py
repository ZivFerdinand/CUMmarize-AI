import tkinter as tk
import nltk
from textblob import TextBlob
from newspaper import Article

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])

# def home():
#     return render_template("index.html")

def gfg():
    if request.method == "POST":
       urlLink = request.form.get("url")
       nltk.download('punkt')
       article = Article(urlLink)
       article.download()
       article.parse()
       article.nlp()
       return "This is your summary <br></br>" + article.summary
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)