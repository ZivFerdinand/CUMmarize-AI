import nltk
from newspaper import Article
from nltk_summarization import nltk_summarizer, readingTime
import time

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def home():
    return render_template('index.html')

@app.route('/text', methods =["GET", "POST"])
def text():
    start = time.time()
    if request.method == "POST" and request.form.get("button") == "url":
        urlLink = request.form.get("url")
        nltk.download('punkt')
        article = Article(urlLink)
        article.download()
        article.parse()
        article.nlp()
        return "Title : " + article.title + "<br>" + "Authors : " + str(article.authors) + "<br>" + "Publication Date : " + str(article.publish_date) + "<br> </br>" + "Summary : <br>" + article.summary
    elif request.method == 'POST' and request.form.get("button") == "rawtext":
        rawtext = request.form['rawtext']
        final_reading_time = readingTime(rawtext)
        final_summary = nltk_summarizer(rawtext)
        summary_reading_time = readingTime(final_summary)
        end = time.time()
        final_time = end-start
        return render_template('result.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)
    return render_template("text.html")

if __name__ == "__main__":
    app.run(debug=True)

# import whisper

# model = whisper.load_model("medium")
# result = model.transcribe("C:\\Users\\bcamaster\\OneDrive\\Documents\\Code\\Code Cawu 3\\CUMmarize-AI\\18.mp4")

# print(result["text"])