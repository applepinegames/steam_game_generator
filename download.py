import json, nltk.data, re, time, urllib

CORPUS_SIZE = 500
SENTENCE_DETECTOR = nltk.data.load('tokenizers/punkt/english.pickle')

def clean_string(s):
  s = re.sub(r'http\S+', ' ', s)
  s = re.sub(r'<.*?>', ' ', s)
  s = re.sub(r'&.*?;', ' ', s)
  s = s.encode('ascii', 'ignore')
  return s

def get_app_data(app_id):
  url = 'http://store.steampowered.com/api/appdetails?appids=' + str(app_id)
  response = urllib.urlopen(url)
  try:
    data = json.loads(response.read())
    if not data[str(app_id)]['success'] or data[str(app_id)]['data']['type'] != 'game':
      return None
    return data[str(app_id)]
  except:
    return None

def get_apps():
  url = 'http://api.steampowered.com/ISteamApps/GetAppList/v2/'
  response = urllib.urlopen(url)
  try:
    data = json.loads(response.read())
    apps = data['applist']['apps']
    return apps
  except:
    return None

def get_description_from_app_data(app_data):
  description = clean_string(app_data['data']['detailed_description'])
  sentences = SENTENCE_DETECTOR.tokenize(description.strip())
  if len(sentences) > 0:
    sentences = sentences[0:(min(3, len(sentences)))]
    sentences = [x for x in sentences if len(x.split(' ')) > 5 and not x.split(' ')[0].isupper() and x.find('\r') == -1]
    combined_sentence = ' '.join(sentences)
    if len(combined_sentence) == 0 or not combined_sentence[0].isalpha() or len(combined_sentence.split(' ')) < 5:
      return None
    return combined_sentence
  return None

def get_title_from_app_data(app_data):
  return clean_string(app_data['data']['name'])

def main():
  apps = get_apps()[-CORPUS_SIZE:]

  for app in apps:
    app_id = app['appid']
    app_data = get_app_data(app_id)
    if not app_data:
      continue
    with open('description.txt', 'a') as description_file:
      description = get_description_from_app_data(app_data)
      if (description):
        description_file.write(description + ' ')
    with open('title.txt', 'a') as title_file:
      title = get_title_from_app_data(app_data)
      if (title):
        title_file.write(title + ' ')
    time.sleep(2)

if __name__ == "__main__":
  main()
