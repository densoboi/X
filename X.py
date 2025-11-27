import tweepy
import requests
import time

# X API setup
client = tweepy.Client(bearer_token='YOUR_BEARER_TOKEN')
discord_webhook = 'YOUR_DISCORD_WEBHOOK_URL'
user_id = client.get_user(username='exampleuser').data.id

last_tweet_id = None
while True:
    tweets = client.get_users_tweets(user_id, max_results=5, since_id=last_tweet_id)
    for tweet in reversed(tweets.data):  # Newest first
        payload = {'content': f"New tweet: {tweet.text}\nhttps://x.com/exampleuser/status/{tweet.id}"}
        requests.post(discord_webhook, json=payload)
        last_tweet_id = tweet.id
    time.sleep(60)  # Poll every minute
