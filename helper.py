from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import  pandas as pd

def fetch_stats(selected_user, df):
    extractor = URLExtract()
    links = []

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['messages']:
        words.extend(message.split())

    num_media = df[df['messages'] == '<Media omitted>\n'].shape[0]
    for message in df['messages']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media, len(links)


def fetch_activeuser(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


def create_cloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc


def commonwords(selected_user, df):
    temp = df[df['messages'] != '<media omitted\n>']
    temp = df[df['user'] != 'group_notification']
    f = open('hinglis_stop.txt')
    stop_words = f.read()
    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)


    commwords = pd.DataFrame(Counter(words).most_common(20))
    return commwords

