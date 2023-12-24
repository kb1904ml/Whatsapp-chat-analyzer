
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import string
import re
import emoji
extract=URLExtract()
from textblob import TextBlob
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df= df[df['user'] == selected_user]

    #1. fetch number of messages
    total_messages=df.shape[0]
    #2. number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    #3. fetch no. of media messages shared
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return total_messages, len(words), num_media_messages, len(links)

# func will only work in group chat analysis
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})

    return x,df


def remove_stop_words(message):
    f = open(r"C:\Users\user\Downloads\stop_hinglish.txt", encoding='utf-8')
    stop_words = f.read()
    y = []
    for word in message.lower().split():
        if word not in stop_words:
            y.append(word)
    return " ".join(y)
def remove_punctuation(message):
    x = re.sub('[%s]'% re.escape(string.punctuation), '', message)
    return x
def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp['message'] = temp['message'].apply(remove_stop_words)
    temp['message'] = temp['message'].apply(remove_punctuation)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc
def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp['message'] = temp['message'].apply(remove_stop_words)
    temp['message'] = temp['message'].apply(remove_punctuation)
    words = []

    for message in temp['message']:
        words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    month_timeline = []
    for i in range(timeline.shape[0]):
        month_timeline.append(timeline['month'][i]+"-"+str(timeline['year'][i]))

    timeline['time'] = month_timeline
    return timeline
def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()
def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
# sentimental analysis
def analyze_sentiment(message):
    analysis = TextBlob(message)

    # Classify the polarity of the message
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'


def analyze_sentiments(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    sentiments = []
    for message in df['message']:
        sentiment = analyze_sentiment(message)
        sentiments.append(sentiment)
    sentiment_df = pd.DataFrame({'Sentiment': sentiments})
    return sentiment_df



    # Classify the polarity of the message











