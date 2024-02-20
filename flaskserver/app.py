from flask import Flask, jsonify, request
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake
import pandas as pd
from pytrends.request import TrendReq
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk


# import statsmodels.api as sm

# ---------------------------------------
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
# ---------------------------------------


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

# Sentimental Analysis
from transformers import AutoTokenizer, pipeline
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from flask import jsonify
import numpy as np
import pymongo

# Aspect Based Sentiment Analysis

tokenizer_for_deberta = AutoTokenizer.from_pretrained("yangheng/deberta-v3-large-absa-v1.1")
deberta_model = AutoModelForSequenceClassification.from_pretrained("yangheng/deberta-v3-large-absa-v1.1")
classifier_deberta = pipeline("text-classification", model=deberta_model, tokenizer=tokenizer_for_deberta)

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


# Aspect Based Sentiment Analysis
@app.route('/absa', methods=['POST'])
def absa():
    review = request.form['text']
    try:
        aspects = request.form['aspects']
        aspects = aspects.split(',')
    except Exception as e:
        print(str(e))
        aspects = ['performance','durability','pricing','sensitivity']
    try:
        res = []
        for aspect in aspects:
            element = classifier_deberta(review, text_pair=aspect)
            label = element[0]['label']
            score = element[0]['score']
            res.append({'aspect': aspect, 'label': label, 'score': score})
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)})


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
    email = request.form['email']
    url = request.form['url']
    try:
        scores = polarity_scores_roberta(text)
        res = jsonify(scores)
        client = pymongo.MongoClient("mongodb+srv://sonarsiddhesh105:K5NuO27RwuV2R986@cluster0.0aedb3y.mongodb.net/?retryWrites=true&w=majority")
        db = client['test']
        collect = db['cres_users']
        filter_query = { "email": email }
        update_query = { "$set": { "products.$[product].sentiment": res } }  # Update the reviews field of the matched product

  # Use arrayFilters to match the specific product within the products array
        array_filters = [{ "product.url": url }]

        update_result = collect.update_one(filter_query, update_query, array_filters=array_filters)
        print("Documents matched:", update_result.matched_count)
        print("Documents modified:", update_result.modified_count)
        return jsonify(scores)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/about')
def about():
    return 'This is the about page.'


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


lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

reviews_df = pd.read_csv("flaskserver/reviews.csv")

reviews_df['sentences'] = reviews_df['text'].apply(sent_tokenize)

def lemmatize_sentence(sentence):
    lemmatized_words = [lemmatizer.lemmatize(word) for word in sentence.split() if word.lower() not in stop_words]
    return ' '.join(lemmatized_words)

reviews_df['text_lemmatized'] = reviews_df['text'].apply(lemmatize_sentence)

vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
X = vectorizer.fit_transform(reviews_df['text_lemmatized'])

num_topics = 5  # You can adjust this number based on your preference
nmf_model = NMF(n_components=num_topics, random_state=42)
nmf_topic_matrix = nmf_model.fit_transform(X)

feature_names = vectorizer.get_feature_names_out()
word_freq = {}
for topic_idx, topic in enumerate(nmf_model.components_):
    for word_idx, word_count in enumerate(topic):
        word = feature_names[word_idx]
        if word in word_freq:
            word_freq[word] += word_count
        else:
            word_freq[word] = word_count

overall_top_words = sorted(word_freq, key=word_freq.get, reverse=True)[:5]

related_sentences = {}
for word in overall_top_words:
    related_sentences[word] = []

for _, row in reviews_df.iterrows():
    review_sentences = row['sentences']
    for sentence in review_sentences:
        for word in overall_top_words:
            if word in sentence:
                related_sentences[word].append(sentence)

@app.route('/related_sentences', methods=['GET'])
def get_related_sentences():
    return jsonify(related_sentences)


if __name__ == '__main__':
    app.run(debug=True)

# for now done 