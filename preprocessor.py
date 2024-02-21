import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user-message': messages, 'message-date': dates})
    # convert message data type
    df['message-date'] = pd.to_datetime(df['message-date'], format='%d/%m/%y, %H:%M - ')
    df.rename(columns={'message-date': 'date'}, inplace=True)

    # seperate users and messages
    users = []
    messages = []

    for message in df['user-message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group-notification')
            messages.append(entry[0])
    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user-message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['date_only'] = df['date'].dt.date
    df['dayname'] = df['date'].dt.day_name()

    period=[]
    for hour in df[['dayname','hour']]['hour']:
        if hour==23:
            period.append(str(hour)+"-"+str('00'))
        elif hour==0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
    df['period']=period

    return df