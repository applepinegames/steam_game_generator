import markovify, nltk, sys

with open("description.txt") as f:
    text = f.read()

textModel = markovify.Text(text)

bestSentence = None
while (True):
  sentence = textModel.make_sentence().capitalize()
  wordCount = len(sentence.split(" "))
  if (sentence.find(" is a ") != -1 and wordCount > 5):
    bestSentence = sentence
    break;

print bestSentence