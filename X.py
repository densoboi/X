import os
import tweepy
import requests
import time

print("Starting script...")
bearer_token = os.getenv('BEARER_TOKEN')
if not bearer_token:
    print("ERROR: No BEARER_TOKEN env var!")
    exit(1)
discord_webhook = os.getenv('DISCORD_WEBHOOK')
if not discord_webhook:
    print("ERROR: No DISCORD_WEBHOOK env var!")
    exit(1)

client = tweepy.Client(bearer_token=bearer_token)
username = 'LouSahFur'  # Your target
user = client.get_user(username=username)
if not user.data:
    print("ERROR: Invalid username!")
    exit(1)
user_id = user.data.id
print(f"Monitoring user ID: {user_id} for @{username}")

last_tweet_id = None
poll_count = 0
sleep_interval = 300  # Start at 5 mins (adjust to 900 for 15 mins if needed)
while True:
    poll_count += 1
    print(f"\n--- Poll #{poll_count} at {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
    try:
        tweets = client.get_users_tweets(user_id, max_results=5, since_id=last_tweet_id)
        print(f"Fetched {len(tweets.data) if tweets.data else 0} tweets.")
        if tweets.data:
            for tweet in reversed(tweets.data):  # Newest first
                print(f"Fetched tweet {tweet.id}: {tweet.text[:50]}...")
                payload = {
                    'content': f"New tweet from @{username}: {tweet.text}\nhttps://x.com/{username}/status/{tweet.id}"
                }
                response = requests.post(discord_webhook, json=payload)
                print(f"Discord post for {tweet.id}: Status {response.status_code} | Response: {response.text[:100]}...")
                if response.status_code == 204:
                    print(f"✅ Successfully posted {tweet.id}")
                else:
                    print(f"❌ Discord failed for {tweet.id}")
                last_tweet_id = tweet.id
        else:
            print("No new tweets found.")
        print(f"Next poll in {sleep_interval}s...")
        time.sleep(sleep_interval)
    except tweepy.TooManyRequests as e:
        print(f"⚠️ Rate limited (429): {e}. Backing off {sleep_interval * 2}s before retry.")
        sleep_interval = min(sleep_interval * 2, 3600)  # Double sleep, cap at 1 hour
        time.sleep(sleep_interval)
        sleep_interval = 300  # Reset after backoff
    except Exception as e:
        print(f"❌ Poll error: {type(e).__name__}: {e}")
        time.sleep(sleep_interval)
