import nltk, time, whisper, os, shutil
from newspaper              import Article
from flask_wtf              import FlaskForm
from werkzeug.utils         import secure_filename
from wtforms                import FileField, SubmitField
from wtforms.validators     import InputRequired
from flask                  import Flask, render_template, request
from nltk_summarization     import nltk_summarizer, readingTime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods =["GET", "POST"])
def home():
    return render_template('index.html')

@app.route('/text', methods =["GET", "POST"])
def text():
    start = time.time()
    if request.method == "POST" and request.form.get("button") == "url":
        try:
            urlLink = request.form.get("url")
            nltk.download('punkt')
            article = Article(urlLink)
            article.download()
            article.parse()
            article.nlp()
        except:
            return render_template('text.html', error_msg="Invalid Link Provided!")
        else:
            return "Title : " + article.title + "<br>" + "Authors : " + str(article.authors) + "<br>" + "Publication Date : " + str(article.publish_date) + "<br> </br>" + "Summary : <br>" + article.summary
    elif request.method == 'POST' and request.form.get("button") == "rawtext":
        try:
            rawtext = request.form['rawtext']
            final_reading_time = readingTime(rawtext)
            final_summary = nltk_summarizer(rawtext)
            summary_reading_time = readingTime(final_summary)
            end = time.time()
            final_time = end-start
        except:
            return render_template('text.html', error_msg_2="Invalid Text Provided!")
        else:
            return render_template('result.html',
                ctext=rawtext,
                final_summary=final_summary,
                final_time=final_time,
                final_reading_time=final_reading_time,
                summary_reading_time=summary_reading_time
                )
    return render_template("text.html")

@app.route('/audio', methods=['GET',"POST"])
def audio():  
    folder = 'static/files'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
        file.save(save_path) # Then save the file
        
        model = whisper.load_model("base")
        result = model.transcribe(save_path)
        return result["text"]
    return render_template('audio.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)