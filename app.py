import tkinter as tk
import nltk
from textblob import TextBlob
from newspaper import Article
from nltk_summarization import nltk_summarizer
import time
import spacy
nlp = spacy.load('en_core_web_sm')

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def home():
    return render_template('index.html')

def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        final_summary = nltk_summarizer(rawtext)
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

def analyze():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		final_summary = nltk_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('result.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)

def readingTime(mytext):
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime

if __name__ == "__main__":
    app.run(debug=True)

# import whisper

# model = whisper.load_model("medium")
# result = model.transcribe("C:\\Users\\bcamaster\\OneDrive\\Documents\\Code\\Code Cawu 3\\CUMmarize-AI\\18.mp4")

# print(result["text"])