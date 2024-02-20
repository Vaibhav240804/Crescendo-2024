from flask import Flask
from flask import request
from rake_nltk import Rake
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake


# Sentimental Analysis
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from flask import Flask, request, jsonify
import numpy as np
# Sentimental Analysis
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)




app = Flask(__name__)

# helper function to lemmatize the text
def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    tokenized = word_tokenize(text)
    lemmatized = [lemmatizer.lemmatize(word) for word in tokenized]
    lemmatized_text = ' '.join(lemmatized)
    return lemmatized_text

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/kextract',methods=['POST'])
def kextract():
    text = request.form['text']
    r = Rake()
    try:
        # lemmatize the text
        try:
            lemmatized_text = lemmatize_text(text)
        except Exception as e:
            return str(e)
        print(lemmatized_text)        
        r.extract_keywords_from_text(lemmatized_text)
        keywords = r.get_ranked_phrases_with_scores()
        # return json response with keywords and their scores
        return {'keywords':keywords}
    except Exception as e:
        return str(e)
    
# Sentimental Analysis    
def polarity_scores_roberta(example):
    encoded_text = tokenizer(example, return_tensors="pt")
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    scores = scores.astype(np.float64)

    return {
        "roberta_neg": scores[0],
        "roberta_neu": scores[1],
        "roberta_pos": scores[2],
    }

# Sentimental Analysis
@app.route("/sentiment", methods=["POST"])
def analyze_sentiment():
    data = request.get_json()
    if not data or not data.get("text"):
        return jsonify({"error": "Missing 'text' field in request body"}), 400

    text = data["text"]
    try:
        scores = polarity_scores_roberta(text)
        return jsonify(scores)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/about')
def about():
    return 'This is the about page.'

if __name__ == '__main__':
    app.run(debug=True)
