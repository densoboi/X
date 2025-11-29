import os
import tweepy
import requests
import time

print("Starting script...")
print(f"Python version: {os.sys.version}")  # Extra debug
print(f"Number of env vars loaded: {len(os.environ)}")  # Should be 10+

# List ALL env var keys (sorted for ease)
print("=== ALL ENVIRONMENT VARIABLES (KEYS ONLY) ===")
for key in sorted(os.environ.keys()):
    print(f"- {key}")

# Specific var checks with partial values (for security)
bearer_token = os.getenv('BEARER_TOKEN')
print("\n=== SPECIFIC VARS DEBUG ===")
print(f"BEARER_TOKEN exists? {bearer_token is not None}")
if bearer_token:
    print(f"BEARER_TOKEN preview: {bearer_token[:20]}... (length: {len(bearer_token)})")
else:
    print("BEARER_TOKEN: MISSING")

discord_webhook = os.getenv('DISCORD_WEBHOOK')
print(f"DISCORD_WEBHOOK exists? {discord_webhook is not None}")
if discord_webhook:
    print(f"DISCORD_WEBHOOK preview: {discord_webhook[:30]}... (length: {len(discord_webhook)})")
else:
    print("DISCORD_WEBHOOK: MISSING")

# If vars are good, proceed (comment out below for full run)
if bearer_token and discord_webhook:
    print("SUCCESS: Vars loaded! Running X client...")
    client = tweepy.Client(bearer_token=bearer_token)
    username = 'LouSahFur'
    try:
        user = client.get_user(username=username)
        if user.data:
            user_id = user.data.id
            print(f"User ID: {user_id} – API works!")
        else:
            print("API call failed – token issue?")
    except Exception as api_err:
        print(f"API Error: {api_err}")
else:
    print("Halting due to missing vars.")
    exit(1)

# Uncomment below for full loop once fixed
# last_tweet_id = None
# while True:
#     ... (your loop code)
