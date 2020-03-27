import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import statistics
import requests
import click
from secrets import *

# https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python


class Twitter:
    def __init__(self):
        """
        Returns the tweepy api object

        # TODO Move the keys to env variables

        Args:

        Returns:
            Tweepy object
        """
        self.consumer_key = CONSUMER_KEY
        self.consumer_secret = CONSUMER_SECRET
        self.access_token = ACCESS_TOKEN
        self.access_token_secret = ACCESS_TOKEN_SECRET

    def connect(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        return api


def fetch_geo_code(location):
    geo_code_url = (
        f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={OPEN_CAGE_KEY}"
    )
    response = requests.get(geo_code_url).json()
    lat = response["results"][0]["geometry"]["lat"]
    lng = response["results"][0]["geometry"]["lng"]
    return lat, lng


def analyse(search_term):
    api = Twitter().connect()
    search_results = api.search(q=search_term, count=1000,result_type="mixed")
    # also checkout https://github.com/sloria/TextBlob
    sid_obj = SentimentIntensityAnalyzer()
    result = {}
    scores = []

    for tweet in search_results:
        scores.append(
            [
                sid_obj.polarity_scores(tweet.text).get("compound"),
                tweet.text,
                tweet.favorite_count + tweet.retweet_count
            ]
        )
    if len(scores) > 1:
        mean_scores = statistics.mean([score[0] for score in scores])
        result["mean_score"] = mean_scores
        scores.sort(key=lambda a: a[0])
        # TODO Word cloud, time-series graph,popular positive/negative tweets, +ve -ve tweets by popular users
        result["top_positive_tweets"] = scores[-5:]
        result["top_negative_tweets"] = scores[:5]
        scores.sort(key=lambda a: a[2],reverse=True)
        result["top_tweets"] = scores[:5]
    return result


def main(location=None, search_term=None):
    respose = {"status": True}
    search_string = "-filter:retweets"

    if not search_term:
        search_term = "Corona"

    if not location:
        search_string = f"{search_term} {search_string}"
    else:
        lat, lng = fetch_geo_code(location)
        search_string = f"{search_term} geocode:{lat},{lng},50km {search_string}"
    print(search_string)
    results = analyse(search_string)
    if not "mean_score" in results:
        return respose
    sentiment = "Neutral"
    mean_score = results["mean_score"]
    if mean_score < -0.05:
        sentiment = "Negative"
    elif mean_score > 0.05:
        sentiment = "Positive"
    results["sentiment"] = sentiment
    respose["results"] = results
    return respose
