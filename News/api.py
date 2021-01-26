import requests

response = requests.get("https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key=AxJegn8UbsHdFMNGJYedGyrkdqgf8G4h")
print(response.json())
