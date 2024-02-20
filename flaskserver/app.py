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
    try:
        # lemmitize the text
        tokenized = word_tokenize(text)
        lemmatized = [lemmatizer.lemmatize(word) for word in tokenized]
        lemmatized_text = ' '.join(lemmatized)
        print(lemmatized_text)
        # extract keywords from sentence
        
        r.extract_keywords_from_text(lemmatized_text)
        keywords = r.get_ranked_phrases_with_scores()
        # return json response with keywords and their scores
        return {'keywords':keywords}
    except Exception as e:
        return str(e)
    

@app.route('/about')
def about():
    return 'This is the about page.'

if __name__ == '__main__':
    app.run(debug=True)
