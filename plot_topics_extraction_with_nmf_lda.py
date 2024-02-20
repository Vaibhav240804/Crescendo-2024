import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

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
print(overall_top_words)
related_sentences = {}
for word in overall_top_words:
    related_sentences[word] = []

for _, row in reviews_df.iterrows():
    review_sentences = row['sentences']
    for sentence in review_sentences:
        for word in overall_top_words:
            if word in sentence:
                related_sentences[word].append(sentence)

print(related_sentences)

for word, sentences in related_sentences.items():
    print(word)
    for sentence in sentences:
        print(sentence)
    print()
