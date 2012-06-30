import re
import nltk

from pymongo.connection import Connection
connection = Connection("localhost")
db = connection.foo

def get_all_words(allComments):
        allWords = [];
        for (words, sentiments) in allComments:
                allWords.extend(words);
        return allWords;

def get_word_features(allWords):
        word_frequency = nltk.FreqDist(allWords);
        features = word_frequency.keys();
        return features;

def extract_features(commentData):
	commentDataIterate = set(commentData)
	features = {};
	for word in word_features:
		features["contains (%s)" % word] = (word in commentDataIterate);
	return features;

"""pos_comments = [('I love this car', 'positive'),
	      ('This view is amazing', 'positive'),
	      ('I feel great this morning', 'positive'),
	      ('I am so excited about the concert', 'positive'),
	      ('He is my best friend', 'positive')];

neg_comments = [('I do not like this car', 'negative'),
	      ('This view is horrible', 'negative'),
	      ('I feel tired this morning', 'negative'),
	      ('I am not looking forward to the concert', 'negative'),
	      ('He is my enemy', 'negative')];"""

pos_comments = [];
neg_comments = [];

for comment in db.testdata.find({"emotion":"positive"}).limit(300):
	pos_comments.append((comment["comment"], comment["emotion"]));

for comment in db.testdata.find({"emotion":"negative"}).limit(300):
	neg_comments.append((comment["comment"], comment["emotion"]));

allComments = [];

for (words, emotion) in pos_comments + neg_comments:
	words_split = [word.lower() for word in words.split() if len(word) >= 3];
	allComments.append((words_split, emotion));

word_features = get_all_words(allComments);

training_set = nltk.classify.apply_features(extract_features, allComments);

classifier = nltk.NaiveBayesClassifier.train(training_set);

print classifier.show_most_informative_features(20);

comment = "This movie is very annoying";

print classifier.classify(extract_features(comment.lower().split()));
