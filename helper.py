import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter


extract=URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    # fetch number of messages
    num_messages = df.shape[0]

    # fetch total number of words
    words = []
    for message in df['messages']:
        words.extend(message.split())

    # fetch media messages
    num_media=df[df['messages']=='<Media omitted>\n'].shape[0]

    # fetch links shared
    links = []

    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words),num_media,len(links)

def most_busy_users(df):
    x = df['users'].value_counts().head()
    df=round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x,df

def create_word_cloud(selected_user,df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    df=df[df['messages']!='<Media omitted>\n']

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['messages'].str.cat(sep=" "))
    return  df_wc

def most_common_words(selected_user,df):
    temp=df[df['users']!='group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words=[]
    for message in temp['messages']:
        words.extend(message.split())
    commonwords=pd.DataFrame(Counter(words).most_common(20))
    return commonwords

def timeline_of_messages(selected_user,df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    # reset_index converts the items into dataframe format
    time = []
    for i in range(timeline.shape[0]):
        time.append(str(timeline['month'][i]) + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    date_df = df.groupby(['date_only']).count()['messages'].reset_index().rename(columns={'date_only': 'date'})
    return date_df

def activity_day(selected_user,df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    return df['dayname'].value_counts()

def activity_month(selected_user,df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    heatmap_data= df.pivot_table(index='dayname', columns='period',values='messages',aggfunc='count').fillna(0)
    return  heatmap_data