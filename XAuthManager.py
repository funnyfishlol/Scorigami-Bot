import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

x_client = tweepy.Client(
    consumer_key = os.getenv("X_API_CONSUMER_KEY"),
    consumer_secret = os.getenv("X_API_CONSUMER_SECRET"),
    access_token = os.getenv("X_API_ACCESS_TOKEN"),
    access_token_secret = os.getenv("X_API_ACCESS_SECRET"),
)