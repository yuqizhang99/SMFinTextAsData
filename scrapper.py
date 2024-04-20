import os
import argparse
from datetime import datetime
from tqdm import tqdm
import snscrape.modules.twitter as sntwitter
import json

parser = argparse.ArgumentParser()
parser.add_argument("--until", type=str, default='2023-06-31', help="Until date for scraping tweets")
args = parser.parse_args()
until = args.until

if 'tweets.jsonl' in os.listdir('./data'):
    with open("./data/tweets.jsonl") as f:
        while True:
            line = f.readline()
            if not line:
                break
            date = json.loads(line)['date']
        print("Last tweet date: ",date)
        since = int(datetime.strptime(date,'%Y-%m-%d %H:%M:%S').timestamp())
else:
    since = int(datetime.strptime('2022-07-01 00:00:00','%Y-%m-%d %H:%M:%S').timestamp())

keywords = ['$MSFT', '$GOOG', '$NVDA', '$META', '$TSLA', '$ADBE', '$IBM', '$PLTR', '$MBLY', '$DT', '$PATH', '$S', '$AUR', '$DARK.L', '$PRESIGHT.AE', '$AI', '$NWTN', '$UPST', '$ODD', '$BAYANAT.AE', '$RXRX', '$PRO', '$SOUN', '$EXAI', '$NNOX', '$CRNC', '$BBAI', '$STEM', '$LGCL', '$INOD', '$AISP', '$STIX', '$AIXI', '$APX.AX', '$AUID', '$BTH.AX', '$TSP', '$LTRN', '$KSCP', '$AIRE', '$DUOT', '$BFRG', '$PRST', '$SPPL', '$JTAI', '$FRGT']

with open("./data/tweets.jsonl",'a+',encoding='utf-8') as t:
    print(' OR '.join(keywords[:10])+' '+f'since:{since} until:{until}')
    for tweet in tqdm(sntwitter.TwitterSearchScraper(' OR '.join(keywords[:10])+' '+f'since:{since} until:{until}').get_items()):
        row = {
        "url":tweet.url,
        "date":tweet.date.strftime("%Y-%m-%d %H:%m:%S"),
        "content":tweet.content,
        "id":tweet.id,
        "userId": tweet.user.id,
        "replyCount":tweet.replyCount,
        "retweetCount":tweet.retweetCount,
        "likeCount":tweet.likeCount,
        "quoteCount":tweet.quoteCount,
        "viewCount":tweet.viewCount,
        "lang":tweet.lang,
        "source":tweet.source,
        "sourceUrl":tweet.sourceUrl,
        "sourceLabel":tweet.sourceLabel,
        "retweetedTweetId":tweet.retweetedTweet.id if tweet.retweetedTweet else None,
        "quotedId":tweet.quotedTweet.id if tweet.quotedTweet else None,
        "inReplyToTweetId":tweet.inReplyToTweetId,
        "inReplyToUserId":tweet.inReplyToUser.id if tweet.inReplyToUser else None,
        "mentionedUsersId":[user.id for user in tweet.mentionedUsers] if tweet.mentionedUsers else None,
        "conversationId":tweet.conversationId,
        "hashtags":tweet.hashtags,
        "place":tweet.place
        }
        line = json.dumps(row,ensure_ascii=False,default=str)
        t.write(line)
        t.write("\n")