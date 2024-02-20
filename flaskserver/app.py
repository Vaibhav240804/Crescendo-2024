from flask import Flask
from flask import request
from rake_nltk import Rake
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/kextract',methods=['POST'])
def kextract():
    text = request.form['text']
    lemmatizer = WordNetLemmatizer()
    r = Rake()
    r.extract_keywords_from_sentences(word_tokenize(text))
    

@app.route('/about')
def about():
    return 'This is the about page.'

if __name__ == '__main__':
    app.run(debug=True)
