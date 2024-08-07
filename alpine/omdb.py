import requests
import json

apiKey = '4dccc310'

title = input('Enter movie or series name to search: ')
response = requests.get(f'http://www.omdbapi.com/?t={title}&apikey={apiKey}')
response.raise_for_status()
jsonified = json.loads(response.text)
# print(jsonified['Year'])
print(jsonified)