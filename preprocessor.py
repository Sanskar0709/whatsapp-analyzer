import re
import pandas as pd


def preprocess(data):
    pattern = ('\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\\s?[ap]m\s-\s')

    messages = re.split(pattern, data)[1:]

    dates = re.findall('\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\u202f?[ap]m\s-\s', data)
    df = pd.DataFrame({'user_messages': messages, 'date': dates})
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M %p - ')

    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['messages'] = messages
    df.drop(columns=['user_messages'], inplace=True)
    df['month'] = df['date'].dt.month_name()
    df['year'] = df['date'].dt.year
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['day'] = df['date'].dt.day
    return df
