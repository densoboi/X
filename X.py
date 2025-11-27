import tweepy
import requests
import time

# X API setup
client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAOio5gEAAAAAEzwCsA%2B74hk81TVueBsSNW%2Bwa%2Fo%3D7GyzbyCZHwJHSpwu90eqQjkoyRdqDLBSATAHVCpnEJw35AzXp4')
discord_webhook = 'https://discord.com/api/webhooks/1443599784324890655/ps20oZhs-k7O5Qs7g5HLpaArSokeSzE2ftVZS4rLi8CKF2thpeGrH1_tgZUe_lR2vIQ6'
user_id = client.get_user(username='exampleuser').data.id

last_tweet_id = None
while True:
    tweets = client.get_users_tweets(user_id, max_results=5, since_id=last_tweet_id)
    for tweet in reversed(tweets.data):  # Newest first
        payload = {'content': f"New tweet: {tweet.text}\nhttps://x.com/exampleuser/status/{tweet.id}"}
        requests.post(discord_webhook, json=payload)
        last_tweet_id = tweet.id
    time.sleep(60)  # Poll every minute
