from flask import Flask, jsonify, request
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake
import pandas as pd
from pytrends.request import TrendReq
import statsmodels.api as sm


# --------- sva ------------
valid_timeframes = [
    "now 1-d",
    "now 1-H",
    "now 4-H",
    "now 1-d",
    "now 7-d",
    "today 1-m",
    "today 3-m",
    "today 12-m",
    "today 5-y"
]
data = pd.read_csv('db.csv')

# ------------------------

# Sentimental Analysis
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from flask import jsonify
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

@app.route('/kextract', methods=['POST'])
def kextract():
    text = request.form['text']
    r = Rake()
    try:
        lemmatized_text = lemmatize_text(text)
        r.extract_keywords_from_text(lemmatized_text)
        keywords_with_scores = r.get_ranked_phrases_with_scores()
        keywords_list = [{"word": keyword, "score": score} for score, keyword in keywords_with_scores]
        return jsonify(keywords_list)
    except Exception as e:
        return jsonify({"error": str(e)})

# Sentimental Analysis    
def polarity_scores_roberta(example):
    encoded_text = tokenizer(example, return_tensors="pt")
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    scores = scores.astype(np.float64)

    return {
        "sentiment": {
        "negative":  scores[0],
        "neutral": scores[1],
        "positive": scores[2]
        },
    }

# Sentimental Analysis
@app.route("/sentiment", methods=["POST"])
def analyze_sentiment():
    data = request.form['text']
    text = data
    try:
        scores = polarity_scores_roberta(text)
        return jsonify(scores)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/about')
def about():
    return 'This is the about page.'


# ----------------------- sva ----------------------------

@app.route('/sva', methods=['GET'])
def interest_over_time():
    timeframe_choice = request.args.get('timeframe_choice', type=int)

    if not 1 <= timeframe_choice <= len(valid_timeframes):
        return jsonify({'error': 'Invalid timeframe choice. Please enter a valid number.'}), 400

    timeframe = valid_timeframes[timeframe_choice - 1]

    pytrends = TrendReq(hl='en-US', tz=360)

    product_name = data['name'][0]
    kw_list = [product_name]
    geo = "IN"

    pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=geo)
    interest_over_time_df = pytrends.interest_over_time().reset_index()

    interest_over_time_df['date'] = interest_over_time_df['date'].astype(str)

    result = {
        'interest_over_time': interest_over_time_df[['date', product_name]].to_dict(orient='records')
    }
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)

# for now done 