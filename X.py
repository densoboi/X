import os
import tweepy
import requests
import time

print("Starting script...")
bearer_token = os.getenv('AAAAAAAAAAAAAAAAAAAAAOio5gEAAAAA5FAa3ewskh%2BoOniZjhu80Nr3Qug%3DgVFjwVMdjg80Bi7UgAQT1zNWbWm8jN5fdd9tlwHThMwphghYcF')
if not bearer_token:
    print("ERROR: No BEARER_TOKEN env var!")
    exit(1)
discord_webhook = os.getenv('https://discord.com/api/webhooks/1443599784324890655/ps20oZhs-k7O5Qs7g5HLpaArSokeSzE2ftVZS4rLi8CKF2thpeGrH1_tgZUe_lR2vIQ6')
if not discord_webhook:
    print("ERROR: No DISCORD_WEBHOOK env var!")
    exit(1)

client = tweepy.Client(bearer_token=bearer_token)
# Get user ID (hardcode or env var for now)
username = 'BaronDestructo'  # Change to your target
user = client.get_user(username=username)
if not user.data:
    print("ERROR: Invalid username!")
    exit(1)
user_id = user.data.id
print(f"Monitoring user ID: {user_id}")

last_tweet_id = None
while True:
    try:
        tweets = client.get_users_tweets(user_id, max_results=5, since_id=last_tweet_id)
        if tweets.data:
            for tweet in reversed(tweets.data):  # Process newest first
                payload = {
                    'content': f"New tweet: {tweet.text}\nhttps://x.com/{username}/status/{tweet.id}"
                }
                response = requests.post(discord_webhook, json=payload)
                print(f"Posted tweet {tweet.id}: {response.status_code}")
                last_tweet_id = tweet.id
        else:
            print("No new tweets found.")
        time.sleep(60)  # Poll every minute
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)
