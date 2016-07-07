import json, re, time, urllib

CORPUS_SIZE = 500

def cleanString(str):
  str = str.replace("<br>", " ")
  str = re.sub(r"http\S+", " ", str)
  str = re.sub(r"<.*?>", " ", str)
  str = re.sub(r"&.*?;", " ", str)
  str = str.encode("ascii", "ignore")
  return str

def getAppData(appID):
  url = "http://store.steampowered.com/api/appdetails?appids=" + str(appID)
  response = urllib.urlopen(url)
  data = json.loads(response.read())
  if (not data[str(appID)]["success"]):
    return None
  return data[str(appID)]

def getApps():
  url = "http://api.steampowered.com/ISteamApps/GetAppList/v2/"
  response = urllib.urlopen(url)
  data = json.loads(response.read())
  apps = data["applist"]["apps"]
  return apps

def getDescriptionFromAppData(appData):
  description = cleanString(appData["data"]["detailed_description"])
  secondPeriodInstance = description.find(".", description.find(".")+1)
  if (secondPeriodInstance == -1):
    return description
  return description[0:secondPeriodInstance]

def getTitleFromAppData(appData):
  return cleanString(appData["data"]["name"])

def main():
  apps = getApps()[0:CORPUS_SIZE:]

  for app in apps:
    appID = app["appid"]
    appData = getAppData(appID)
    if (not appData):
      continue
    with open("description.txt", "a") as descriptionFile:
      description = getDescriptionFromAppData(appData)
      descriptionFile.write(description + " ")
    with open("title.txt", "a") as titleFile:
      title = getTitleFromAppData(appData)
      titleFile.write(title + " ")
    time.sleep(2)
main()