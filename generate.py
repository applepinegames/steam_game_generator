import markovify, sys

def generate(numSentences):
  with open("description.txt") as f:
    text = f.read()
  textModel = markovify.Text(text)
  bestSentences = []
  while (True):
    sentence = textModel.make_short_sentence(140).capitalize()
    wordCount = len(sentence.split(" "))
    if (sentence.find(" is a ") != -1 and wordCount > 5):
      bestSentences.append(sentence)
      if (len(bestSentences) == numSentences):
        break;
  return bestSentences

def amazon_lambda_handler(event, context):
  return generate(5)

if __name__ == "__main__":
  print generate(1)[0]