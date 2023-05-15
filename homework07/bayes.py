from collections import Counter, defaultdict

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize


class NaiveBayesClassifier:
    def __init__(self, alpha=0.05):
        self.word_probabilities = defaultdict(Counter)
        self.class_probabilities = {}
        self.alpha = alpha
        self.labels = set()
        self.words = Counter()

    def fit(self, X, y):
        lemmatizer = WordNetLemmatizer()
        class_counts = Counter(y)
        total_count = len(y)
        self.labels = set(y)
        self.class_probabilities = {lbl: count / total_count for lbl, count in class_counts.items()}
        for doc, label in zip(X, y):
            for word in wordpunct_tokenize(doc):
                stemmed_word = lemmatizer.lemmatize(word)
                self.words[stemmed_word] += 1
                self.word_probabilities[label][stemmed_word] += 1
        count_labels = {lbl: sum(word_counts.values()) for lbl, word_counts in self.word_probabilities.items()}
        for word in self.words:
            for label in self.labels:
                self.word_probabilities[label][word] = (self.word_probabilities[label][word] + self.alpha) / (
                    count_labels[label] + self.alpha * len(self.words)
                )

    def predict(self, X):
        predictions = []
        lemmatizer = WordNetLemmatizer()
        for doc in X:
            label_scores = self.class_probabilities.copy()
            for word in wordpunct_tokenize(doc):
                word_lemma = lemmatizer.lemmatize(word)
                for label, word_probs in self.word_probabilities.items():
                    if word_probs[word_lemma] != 0:
                        label_scores[label] *= word_probs[word_lemma]
            predicted_label = max(label_scores, key=label_scores.get)
            predictions.append(predicted_label)
        return predictions

    def score(self, X_test, y_test):
        num_correct = 0
        num_total = len(y_test)
        predicted_labels = self.predict(X_test)
        for predicted_label, true_label in zip(predicted_labels, y_test):
            if predicted_label == true_label:
                num_correct += 1
        accuracy = num_correct / num_total
        return accuracy