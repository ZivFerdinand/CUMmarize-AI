import nltk, time, whisper, os, shutil
from newspaper              import Article
from flask_wtf              import FlaskForm
from werkzeug.utils         import secure_filename
from wtforms                import FileField, SubmitField
from wtforms.validators     import InputRequired
from flask                  import Flask, render_template, request
from nltk_summarization     import nltk_summarizer, readingTime

def folder_clearance():
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

            final_reading_time = readingTime(article.text)
            final_summary = nltk_summarizer(article.text)
            summary_reading_time = readingTime(article.summary)
            if final_summary == "":
                final_summary = "Your link can't be summarized!"
            end = time.time()
            final_time = end-start
        except:
            return render_template('text.html', error_msg="Invalid Link Provided!")
        else:
            return render_template('result.html',
                ctext=article.text,
                final_summary=article.summary,
                final_time=final_time,
                final_reading_time=final_reading_time,
                summary_reading_time=summary_reading_time
                )
    elif request.method == 'POST' and request.form.get("button") == "rawtext":
        try:
            rawtext = request.form['rawtext']
            final_reading_time = readingTime(rawtext)
            final_summary = nltk_summarizer(rawtext)
            summary_reading_time = readingTime(final_summary)
            if final_summary == "":
                final_summary = "Your text can't be summarized!"
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
    try:
        folder_clearance()
    except:
        os.mkdir('static/files')
        folder_clearance()
    
    form = UploadFileForm()
    if form.validate_on_submit():
        start = time.time()
        file = form.file.data # First grab the file
        save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
        file.save(save_path) # Then save the file
        
        model = whisper.load_model("base")
        result = model.transcribe(save_path)
        # return result["text"]
        final_reading_time = readingTime(result["text"])
        final_summary = nltk_summarizer(result["text"])
        summary_reading_time = readingTime(final_summary)
        if final_summary == "":
            final_summary = "Your video can't be summarized!"
        end = time.time()
        final_time = end-start
        return render_template('result.html',
                ctext=result["text"],
                final_summary=final_summary,
                final_time=final_time,
                final_reading_time=final_reading_time,
                summary_reading_time=summary_reading_time
            )
    return render_template('audio.html', form=form)

@app.route('/video', methods=['GET',"POST"])
def video():  
    try:
        folder_clearance()
    except:
        os.mkdir('static/files')
        folder_clearance()
    
    form = UploadFileForm()
    if form.validate_on_submit():
        start = time.time()
        file = form.file.data # First grab the file
        save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
        file.save(save_path) # Then save the file
        
        model = whisper.load_model("base")
        result = model.transcribe(save_path)
        # return result["text"]
        final_reading_time = readingTime(result["text"])
        final_summary = nltk_summarizer(result["text"])
        summary_reading_time = readingTime(final_summary)
        if final_summary == "":
            final_summary = "Your paragraph can't be summarized!"
        end = time.time()
        final_time = end-start
        return render_template('result.html',
                ctext=result["text"],
                final_summary=final_summary,
                final_time=final_time,
                final_reading_time=final_reading_time,
                summary_reading_time=summary_reading_time
            )
    return render_template('video.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)


