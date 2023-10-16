from sklearn.datasets import fetch_20newsgroups
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
import matplotlib.pyplot as plt

nltk.download('stopwords')
nltk.download('punkt')

newsgroups_train = fetch_20newsgroups(subset='train')
newsgroups_test = fetch_20newsgroups(subset ='test')


def preprocess_texts(texts : list[str]) -> list[str]:
    '''
    Remove all stopwords, remove non-letter words, lowercase.
    '''
    filtered = []
    for text in texts:
        temp = []
        for word in nltk.tokenize.word_tokenize(text):
            if word.lower() not in stopwords.words('english') and word.isalpha():
                temp.append(word.lower())

        filtered.append(" ".join(temp))
    return filtered

def stem_texts(texts : list[str]):
    '''
    Stem all words in texts.\n\nAccepts already tokenized texts.
    '''
    stemmed = []
    stemmer = nltk.SnowballStemmer("english")

    for text in texts:
        temp = []
        for word in nltk.tokenize.word_tokenize(text):
            temp.append(stemmer.stem(word))

        stemmed.append(" ".join(temp))
    return stemmed


newsgroups_train['preprocessed_data'] = preprocess_texts(newsgroups_train.data)
newsgroups_test['preprocessed_data'] = preprocess_texts(newsgroups_test.data)

newsgroups_train['stemmed_data'] = stem_texts(newsgroups_train['preprocessed_data'])
newsgroups_test['stemmed_data'] = stem_texts(newsgroups_test['preprocessed_data'])


def vectorize_data(vectorizer, train_data, test_data):
    '''
    Fits vectorizer and vectorizes data.

    Returns: Vectorized train data, vectorized test data.
    '''
    vec_train = vectorizer.fit_transform(train_data)
    vec_test = vectorizer.transform(test_data)
    return vec_train, vec_test


'''
Count Vectorizer
'''

# raw texts
raw_text_count_train, raw_text_count_test = vectorize_data(
    CountVectorizer(),
    newsgroups_train.data,
    newsgroups_test.data)

# preprocessed texts excluding stemming
preprocessed_count_train, preprocessed_count_test = vectorize_data(
    CountVectorizer(),
    newsgroups_train['preprocessed_data'],
    newsgroups_test['preprocessed_data'])

# preprocessed texts including stemming
stemmed_count_train, stemmed_count_test = vectorize_data(
    CountVectorizer(),
    newsgroups_train['stemmed_data'],
    newsgroups_test['stemmed_data'])

# preprocessed texts considering bigrams as well
stemmed_bigram_count_train, stemmed_bigram_count_test = vectorize_data(
    CountVectorizer(ngram_range=(1,2)),
    newsgroups_train['stemmed_data'],
    newsgroups_test['stemmed_data'])

'''
Tf-idf Vectorizer
'''

# raw texts
raw_text_tfidf_train, raw_text_tfidf_test = vectorize_data(
    TfidfVectorizer(),
    newsgroups_train.data,
    newsgroups_test.data)

# preprocessed texts excluding stemming
preprocessed_tfidf_train, preprocessed_tfidf_test = vectorize_data(
    TfidfVectorizer(),
    newsgroups_train['preprocessed_data'],
    newsgroups_test['preprocessed_data'])

# preprocessed texts including stemming
stemmed_tfidf_train, stemmed_tfidf_test = vectorize_data(
    TfidfVectorizer(),
    newsgroups_train['stemmed_data'],
    newsgroups_test['stemmed_data'])

# preprocessed texts considering bigrams as well
stemmed_bigram_tfidf_train, stemmed_bigram_tfidf_test = vectorize_data(
    TfidfVectorizer(ngram_range=(1,2)),
    newsgroups_train['stemmed_data'],
    newsgroups_test['stemmed_data'])


def get_predictions_of_model_on_data(model_class, train_data, test_data, train_target):
    '''
    Fit a model with vectorized data and get predictions.
    '''
    model = model_class.fit(train_data, train_target)
    return model.predict(test_data)

# Train each model on each type of preprocessing and vectorizer, 
# let the model classify the test data and save the predictions in a `results_dict`

results_dict = {}
for classifier, name in [(MultinomialNB(), "Naive Bayes"), (SVC(), "SVC"), (LogisticRegression(), "Regression"), (RandomForestClassifier(), "Random Forest")]:
    print("Training", name)
    temp = {}

    # raw texts
    temp["raw texts count"] = get_predictions_of_model_on_data(classifier,
                                                 raw_text_count_train,
                                                 raw_text_count_test,
                                                 newsgroups_train.target)

    temp["raw texts tfidf"] = get_predictions_of_model_on_data(classifier,
                                                 raw_text_tfidf_train,
                                                 raw_text_tfidf_test,
                                                 newsgroups_train.target)

    # preprocessed texts excluding stemming
    temp["preprocessed texts count"] = get_predictions_of_model_on_data(classifier,
                                                 preprocessed_count_train,
                                                 preprocessed_count_test,
                                                 newsgroups_train.target)

    temp["preprocessed texts tfidf"] = get_predictions_of_model_on_data(classifier,
                                                 preprocessed_tfidf_train,
                                                 preprocessed_tfidf_test,
                                                 newsgroups_train.target)

    # preprocessed texts including stemming
    temp["stemmed texts count"] = get_predictions_of_model_on_data(classifier,
                                                 stemmed_count_train,
                                                 stemmed_count_test,
                                                 newsgroups_train.target)

    temp["stemmed texts tfidf"] = get_predictions_of_model_on_data(classifier,
                                                 stemmed_tfidf_train,
                                                 stemmed_tfidf_test,
                                                 newsgroups_train.target)

    # preprocessed texts considering bigrams as well
    temp["stemmed bigram texts count"] = get_predictions_of_model_on_data(classifier,
                                                 stemmed_bigram_count_train,
                                                 stemmed_bigram_count_test,
                                                 newsgroups_train.target)

    temp["stemmed bigram texts tfidf"] = get_predictions_of_model_on_data(classifier,
                                                 stemmed_bigram_tfidf_train,
                                                 stemmed_bigram_tfidf_test,
                                                 newsgroups_train.target)

    results_dict[name] = temp

# Evaluate using multiple metrics

for method in results_dict:
    print(method)
    print("\naccuracy:")
    for preprocessing in results_dict[method]:
        print(preprocessing, accuracy_score(newsgroups_test.target, results_dict[method][preprocessing]))

    print("\nf1_score:")
    for preprocessing in results_dict[method]:
        print(preprocessing, f1_score(newsgroups_test.target, results_dict[method][preprocessing], average="weighted"))

    print("\nprecision:")
    for preprocessing in results_dict[method]:
        print(preprocessing, precision_score(newsgroups_test.target, results_dict[method][preprocessing], average="weighted"))

    print("\nrecall:")
    for preprocessing in results_dict[method]:
        print(preprocessing, recall_score(newsgroups_test.target, results_dict[method][preprocessing], average="weighted"))

# retrain and evaluate the best achieving model

best_model_predictions = get_predictions_of_model_on_data(LogisticRegression(),
                                          stemmed_bigram_tfidf_train,
                                          stemmed_bigram_tfidf_test,
                                          newsgroups_train.target)

print("accuracy of the model:", accuracy_score(newsgroups_test.target, best_model_predictions))

print("average='micro', labels='None':", f1_score(newsgroups_test.target, best_model_predictions, average='micro', labels='None'))
print("average='micro':", f1_score(newsgroups_test.target, best_model_predictions, average='micro'))

print("average='macro', labels='None':", f1_score(newsgroups_test.target, best_model_predictions, average='macro', labels='None'))
print("average='macro':", f1_score(newsgroups_test.target, best_model_predictions, average='macro'))

print("average='weighted', labels='None':", f1_score(newsgroups_test.target, best_model_predictions, average='weighted', labels='None'))
print("average='weighted':", f1_score(newsgroups_test.target, best_model_predictions, average='weighted'))

print("average='weighted', labels=[1,2,3,4,5]:", f1_score(newsgroups_test.target, best_model_predictions, average='weighted', labels=[1,2,3,4,5]))


conf_matrix = confusion_matrix(newsgroups_test.target, best_model_predictions)

fig, ax = plt.subplots(figsize=(7.5, 7.5))
ax.matshow(conf_matrix, cmap=plt.cm.Blues, alpha=0.5)
for i in range(conf_matrix.shape[0]):
    for j in range(conf_matrix.shape[1]):
        ax.text(x=j, y=i,s=conf_matrix[i, j], va='center', ha='center')

plt.xlabel('Predictions', fontsize=18)
plt.ylabel('True', fontsize=18)
plt.title('Confusion Matrix', fontsize=18)
plt.show()

