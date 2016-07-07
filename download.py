import json, nltk.data, re, time, urllib

CORPUS_SIZE = 500
SENTENCE_DETECTOR = nltk.data.load("tokenizers/punkt/english.pickle")

def cleanString(str):
  str = re.sub(r"http\S+", " ", str)
  str = re.sub(r"<.*?>", " ", str)
  str = re.sub(r"&.*?;", " ", str)
  str = str.encode("ascii", "ignore")
  return str

def getAppData(appID):
  url = "http://store.steampowered.com/api/appdetails?appids=" + str(appID)
  response = urllib.urlopen(url)
  try:
    data = json.loads(response.read())
    if (not data[str(appID)]["success"] or data[str(appID)]["data"]["type"] != "game"):
      return None
    return data[str(appID)]
  except:
    return None

def getApps():
  url = "http://api.steampowered.com/ISteamApps/GetAppList/v2/"
  response = urllib.urlopen(url)
  try:
    data = json.loads(response.read())
    apps = data["applist"]["apps"]
    return apps
  except:
    return None

def getDescriptionFromAppData(appData):
  description = cleanString(appData["data"]["detailed_description"])
  sentences = SENTENCE_DETECTOR.tokenize(description.strip())
  if (len(sentences) > 0):
    sentences = sentences[0:(min(3, len(sentences)))]
    sentences = [x for x in sentences if len(x.split(" ")) > 5 and not x.split(" ")[0].isupper() and x.find("\r") == -1]
    combinedSentence = " ".join(sentences)
    if (len(combinedSentence) == 0 or not combinedSentence[0].isalpha() or len(combinedSentence.split(" ")) < 5):
      return None
    return combinedSentence
  return None

def getTitleFromAppData(appData):
  return cleanString(appData["data"]["name"])

def main():
  apps = getApps()[-CORPUS_SIZE:]

  for app in apps:
    appID = app["appid"]
    appData = getAppData(appID)
    if (not appData):
      continue
    with open("description.txt", "a") as descriptionFile:
      description = getDescriptionFromAppData(appData)
      if (description):
        descriptionFile.write(description + " ")
    with open("title.txt", "a") as titleFile:
      title = getTitleFromAppData(appData)
      if (title):
        titleFile.write(title + " ")
    time.sleep(2)
main()