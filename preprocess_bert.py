import pandas as pd
import argparse
import re
import string
from functools import partial
import harvesttext

keyword_dict = {
    "科大讯飞": ['科大讯飞', 'SZ002230', '002230.SZ', '002230'],
    "工业富联": ['工业富联', 'SH601138', '601138.SH', '601138'],
    "中科曙光": ['中科曙光', 'SH603019', '603019.SH', '603019'],
    "浪潮信息": ['浪潮信息', 'SZ000977', '000977.SZ', '000977'],
    "昆仑万维": ['昆仑万维', 'SZ300418', '300418.SZ', '300418'],
}

def preprocess(row,firm_name,ht):
    text = row["text"]
    text = ht.clean_text(text,remove_url=True,email=True,weibo_at=True,emoji=False,weibo_topic=False,markdown_hyperlink=True,\
        deduplicate_space=True,remove_tags=True,t2s=True)
    text = text.lower()
    #clean url thoroughly
    text = re.sub(r'http[0-9a-z\.\/:?]+', ' ', text)
    #clean mentioned users
    for mentioned_user in row['mentioned_users']:
        text = text.replace(f'//@{mentioned_user}', '')
        text = text.replace(f'@{mentioned_user}', '')
        text = text.replace(f'回复@{mentioned_user}:', '')
    #combine multiple spaces into one
    text = re.sub(r'\s+', ' ', text)
    # replace keywords with X
    for keyword in keyword_dict[firm_name]:
        text = text.replace(keyword.lower(), 'X')
    # split text into sentences
    sentences = ht.cut_sentences(text)
    row["sentences"] = sentences
    return row

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--firm_name', type=str)
    firm_name = argparser.parse_args().firm_name

    df = pd.read_csv(f"./data/{firm_name}20220701-20230630_cleaned.csv")
    partial_preprocess = partial(preprocess, firm_name=firm_name,ht=harvesttext.HarvestText())
    df['bert_sentences'] = df.apply(partial_preprocess, axis=1)["sentences"]
    df.to_csv(f"./data/{firm_name}20220701-20230630_cleaned_bert.csv", index=False)