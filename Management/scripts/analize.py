import os
import sys
from collections import Counter
from Module.TwitterAPIWrapper import TwitterAPI

try:
    from CustomConfig import *
except Exception as e:
    print(e)
    # Credentials
    username = 'TWITTER_USERNAME'
    costumer_key = 'TWITTER_COSTUMER_API_KEY'
    costumer_key_secret = 'TWITTER_COSTUMER_API_KEY_SECRET'
    access_token = 'TWITTER_ACCESS_TOKEN'
    access_token_secret = 'TWITTER_ACCESS_TOKEN_SECRET'

# Usage example
if __name__ == '__main__':
    api = TwitterAPI(
        username = username,
        costumer_key = costumer_key,
        costumer_key_secret = costumer_key_secret,
        access_token = access_token,
        access_token_secret = access_token_secret,
    )

    divider = '----------------'
    count_filter = 10
    limit = 200

    # Get most used hashtags by topic
    print(divider)
    topics = ['ai', 'art', 'stablediffusion', 'stable diffusion', 'anime', 'cosplay', 'fanart']
    print(f'\n[+] Searching topics: {", ".join(topics)}\n')

    ''' TOP HASHTAGS BY TOPIC '''
    print(divider)
    # Get the trending hashtags for each topic
    trending_hashtags = api.get_trending_hashtags(topics, count=limit, result_type='mixed')
    # Print the trending hashtags for each topic
    for topic, hashtags in trending_hashtags.items():
        print(f"Trending hashtags for {topic}:")
        for hashtag, count in hashtags:
            if count > count_filter:
                print(f"{hashtag}: {count}")
        print()


    ''' TOP HASHTAGS IN TOPICS '''
    print(divider)
    # Get the top 100 tweets for each query and extract the hashtags
    hashtags = []
    for query in topics:
        tweets = api.search_tweets(query, count=limit, result_type='mixed')
        for tweet in tweets:
            hashtags.extend(api.extract_hashtags(tweet))
    # Count the occurrences of each hashtag
    hashtag_counts = Counter(hashtags)
    # Print the most common hashtags
    print("Most common hashtags:")
    for hashtag, count in hashtag_counts.most_common():
        if count > count_filter:
            print(f"{hashtag}: {count}")

    ''' PEAK TWEET TIMES '''
    print(divider)
    sorted_tweet_reach, peak_time_counter = api.analyze_tweets(count=limit)

    # Print the top 5 tweets by reach
    print("Top 5 tweets by reach:\n")
    for tweet_id, reach, hour in sorted_tweet_reach[:5]:
        tweet_url = f"https://twitter.com/{api.twitter_username}/status/{tweet_id}"
        print(f"Tweet URL: {tweet_url}, Reach: {reach}, Hour: {hour}:00")

    # Print the peak posting time
    peak_time, _ = peak_time_counter.most_common(1)[0]
    print(f"\nPeak posting time: {peak_time}:00")

    print(divider)
