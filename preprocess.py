import pandas as pd
import argparse
import re
import string
from functools import partial

keyword_dict = {
    "科大讯飞": ['科大讯飞', 'SZ002230', '002230.SZ', '002230'],
    "工业富联": ['工业富联', 'SH601138', '601138.SH', '601138'],
    "中科曙光": ['中科曙光', 'SH603019', '603019.SH', '603019'],
    "浪潮信息": ['浪潮信息', 'SZ000977', '000977.SZ', '000977'],
    "昆仑万维": ['昆仑万维', 'SZ300418', '300418.SZ', '300418'],
}

def getLabels(text):
    labels = []
    if '工业富联' in text or '601138' in text:
        labels.append('工业富联')
    if '科大讯飞' in text or '002230' in text:
        labels.append('科大讯飞')
    if '中科曙光' in text or '603019' in text:
        labels.append('中科曙光')
    if '浪潮信息' in text or '000977' in text:
        labels.append('浪潮信息')
    if '昆仑万维' in text or '300418' in text:
        labels.append('昆仑万维')
    return labels

def getTopics(topics):
    if pd.isna(topics):
        return []
    else:
        return topics.split(',')
    
def getMentionedUsers(users):
    if pd.isna(users):
        return []
    else:
        return users.split(',')

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--firm_name', type=str)
    firm_name = argparser.parse_args().firm_name

    df = pd.read_csv(f"./data/{firm_name}20220701-20230630.csv")
    df = df.rename(columns={'用户昵称': 'username', '微博正文': 'text', '头条文章url': 'toutiao_url', '发布位置': 'location', '艾特用户': 'mentioned_users', '话题': 'topics', '转发数': 'repost_count', '评论数': 'comment_count', '点赞数': 'like_count', '发布时间': 'create_time', '发布工具': 'publish_platform', '微博图片url': 'weibo_image_url', '微博视频url': 'weibo_video_url'})
    df["topics"] = df["topics"].apply(getTopics)
    df["mentioned_users"] = df["mentioned_users"].apply(getMentionedUsers)
    df["labels"] = df["text"].apply(getLabels)
    df.to_csv(f"./data/{firm_name}20220701-20230630_cleaned.csv", index=False)