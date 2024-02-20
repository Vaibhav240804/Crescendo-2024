from flask import Flask, jsonify
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk

app = Flask(__name__)

reviewList = [
    {
        "rating": "5.0 out of 5 stars",
        "star": 5.0,
        "body": "Great Product, Value for Money, Original product, great quality.",
        "fullDate": "Reviewed in India on 27 January 2024",
        "date": "27 January 2024"
    },
    {
        "rating": "4.0 out of 5 stars",
        "star": 4.0,
        "body": "Good quality.",
        "fullDate": "Reviewed in India on 8 February 2024",
        "date": "8 February 2024"
    },
    {
        "rating": "3.0 out of 5 stars",
        "star": 3.0,
        "body": "Average product, nothing special.",
        "fullDate": "Reviewed in India on 15 March 2024",
        "date": "15 March 2024"
    }
]

# Analyze reviews and find related sentences for top words
def analyze_reviews(reviewList):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    if len(reviewList)==0:
        return "List is Empty"
    # Combine review bodies into one string
    review_text = ' '.join([review['body'] for review in reviewList])

    # Tokenize the combined text into sentences
    review_sentences = sent_tokenize(review_text)

    # Lemmatize each sentence and remove stop words
    lemmatized_sentences = []
    for sentence in review_sentences:
        lemmatized_words = [lemmatizer.lemmatize(word) for word in sentence.split() if word.lower() not in stop_words]
        lemmatized_sentences.append(' '.join(lemmatized_words))

    # Vectorize the lemmatized sentences
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    X = vectorizer.fit_transform(lemmatized_sentences)

    # Apply NMF to find topics
    num_topics = 5
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

    # Get the overall top words
    overall_top_words = sorted(word_freq, key=word_freq.get, reverse=True)[:5]

    # Find related sentences for each top word
    related_sentences = {}
    for word in overall_top_words:
        related_sentences[word] = []

    for sentence in lemmatized_sentences:
        for word in overall_top_words:
            if word in sentence:
                related_sentences[word].append(sentence)

    return related_sentences

# Define Flask endpoint
@app.route('/related_sentences', methods=['GET'])
def get_related_sentences():
    related_sentences = analyze_reviews(reviewList)
    return jsonify(related_sentences)

if __name__ == '__main__':
    app.run(debug=True)
