#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import pandas as pd


# In[2]:


f=open(r"C:\Users\user\Downloads\WhatsApp Chat with M2 mechanical .txt",encoding='utf-8')


# In[3]:


data=f.read()


# In[4]:


print(data)


# In[5]:


print(type(data))


# In[6]:


# convert data from string form to dataframe
# date and time in one column and msg in other column
pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'


# In[7]:


messages=re.split(pattern,data)[1:]
print(messages)
                


# In[8]:


dates=re.findall(pattern,data)
dates


# In[9]:


df = pd.DataFrame({'user_message': messages, 'message_date': dates})
 # convert message_date type
df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')

df.rename(columns={'message_date': 'date'}, inplace=True)


# In[10]:


df.head()


# In[11]:


df.shape


# In[12]:


# separate users and messages
users = []
messages = []
for message in df['user_message']:
    entry = re.split('([\w\W]+?):\s', message)
    if entry[1:]:  # user name
        users.append(entry[1])
        messages.append(" ".join(entry[2:]))
    else:
        users.append('group_notification')
        messages.append(entry[0])
df['user'] = users
df['message'] = messages
df.drop(columns=['user_message'], inplace=True)


# In[13]:


df.head()


# In[14]:


df['year']=df['date'].dt.year


# In[15]:


df.head()


# In[16]:


df['month'] = df['date'].dt.month_name()


# In[17]:


df['month_num'] = df['date'].dt.month


# In[18]:


df['day']=df['date'].dt.day


# In[19]:


df['day_name'] = df['date'].dt.day_name()


# In[20]:


df['hour']=df['date'].dt.hour


# In[21]:


df['minute']=df['date'].dt.minute


# In[22]:


df.head()


# In[23]:


df[df['user']=='Kumkum'].shape


# In[24]:


#finding total number of words 
words=[]
for message in df['message']:
    words.extend(message.split())
    


# In[25]:


len(words)


# In[26]:


#Number of media shared
df[df['message']=='<Media omitted>\n'].shape[0]


# In[27]:


get_ipython().system('pip install urlextract')


# In[28]:


#Number of links shared
from urlextract import URLExtract
extract=URLExtract()
links=[]
for message in df['message']:
    links.extend(extract.find_urls(message))


# In[29]:


len(links)


# In[30]:


df['user'].value_counts().head()


# In[31]:


#finding the busiest users in the group
import matplotlib.pyplot as plt
x=df['user'].value_counts().head()
user_names=x.index
msg_count=x.values
plt.bar(user_names,msg_count)
plt.xticks(rotation='vertical')
plt.show()


# In[32]:


new_df = round(((df['user'].value_counts() / df.shape[0]) * 100), 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})

new_df.head()


# In[33]:


#Display top words in a chat
get_ipython().system('pip install wordcloud')


# In[34]:


import string


# In[35]:


def remove_stop_words(message):
  f = open(r"C:\Users\user\Downloads\stop_hinglish.txt",encoding='utf-8')
  stop_words = f.read()
  y = []
  for word in message.lower().split():
      if word not in stop_words:
          y.append(word)
  return " ".join(y)
def remove_punctuation(message):
  x = re.sub('[%s]'% re.escape(string.punctuation), '', message)
  return x


# In[36]:


#Data Cleaning
temp = df[df['user'] != 'group_notification'] #remove group notification
temp = temp[temp['message'] != '<Media omitted>\n'] #remove media message
temp['message'] = temp['message'].apply(remove_stop_words) #remove stopwords
temp['message'] = temp['message'].apply(remove_punctuation) #remove punctuations


# In[37]:


#Draw the wordCloud
from wordcloud import WordCloud
plt.figure(figsize=(20, 10))
wc = WordCloud(width=1000,height=750,min_font_size=10,background_color='white')
cloud = wc.generate(temp['message'].str.cat(sep=" "))
plt.imshow(cloud)


# In[38]:


#finding 20 most common words
temp = df[df['user'] != 'group_notification'] #remove group notification
temp = temp[temp['message'] != '<Media omitted>\n'] #remove media message
temp['message'] = temp['message'].apply(remove_stop_words) #remove stopwords
temp['message'] = temp['message'].apply(remove_punctuation) #remove punctuations
words = []
for message in temp['message']:
  words.extend(message.split())
from collections import Counter
most_common_df = pd.DataFrame(Counter(words).most_common(20))
most_common_df


# In[39]:


get_ipython().system('pip install emoji')


# In[40]:


#Emoji Analysis
import emoji

emojis = []
for message in df['message']:
  emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))


# In[41]:


#time based analysis
#monthly chats timeline
timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
month_timeline = []

for i in range(timeline.shape[0]):
  month_timeline.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

timeline['time'] = month_timeline

#draw plot
plt.figure(figsize=(12,6))
plt.plot(timeline['time'], timeline['message'])
plt.xticks(rotation='vertical')
plt.show()


# In[42]:


#day based activity map
busy_day = df['day_name'].value_counts()
plt.figure(figsize=(12, 6))
plt.bar(busy_day.index, busy_day.values, color='purple')
plt.title("Busy Day")
plt.xticks(rotation='vertical')
plt.show()


# In[43]:


#monthly based activity map
busy_month = df['month'].value_counts()
plt.figure(figsize=(12, 6))
plt.bar(busy_month.index, busy_month.values, color='orange')
plt.title("Busy Month")
plt.xticks(rotation='vertical')
plt.show()


# In[44]:


pip install textblob


# In[47]:


from textblob import TextBlob

def analyze_sentiment(message):
    analysis = TextBlob(message)
    
    # Classify the polarity of the message
    if analysis.sentiment.polarity >0:
        return 'Positive'
    elif analysis.sentiment.polarity==0:
        return 'Neutral'
    else:
        return 'Negative'
    messages = df.readlines()

# Perform sentiment analysis on each message
sentiments = [analyze_sentiment(message) for message in messages]

# Print the sentiments
for i, sentiment in enumerate(sentiments):
    print(f'Message {i + 1}: {sentiment}')


# In[48]:


# Plot sentiment distribution
sentiment_counts = {'Positive': 0, 'Neutral': 0, 'Negative': 0}

for sentiment in sentiments:
    sentiment_counts[sentiment] += 1

labels = list(sentiment_counts.keys())
values = list(sentiment_counts.values())

plt.bar(labels, values, color=['purple', 'orange', 'pink'])
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.title('Sentiment Distribution')
plt.show()


# In[49]:


from textblob import TextBlob

testimonial = TextBlob("The food was best!")
print(testimonial.sentiment)

