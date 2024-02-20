from flask import Flask
from flask import request
from rake_nltk import Rake

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/kextract',methods=['POST'])
def kextract():
    text = request.form['text']
    r = Rake()
    try:
        r.extract_keywords_from_text(text)
        return {'keywords':r.get_ranked_phrases()}
    except:
        return {'keywords':[]}
    

@app.route('/about')
def about():
    return 'This is the about page.'

if __name__ == '__main__':
    app.run(debug=True)
