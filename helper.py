from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter
extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        # selects the user
        df_user = df[df['users'] == selected_user]
        # number of messages
        num_messages = df_user.shape[0]
        # number of words
        words = [word for message in df_user['message'] for word in message.split()]
        # number of photos, videos and gifs
        num_media_messages_user = df_user[df['message'].str.contains('image omitted|video omitted|sticker omitted')].shape[0]
        # number of links
        links = [link for message in df_user['message'] for link in extract.find_urls(message)]

        # def num_media_messages(df):
        #     return df[df['message'].str.contains('image omitted|video omitted|sticker omitted')].shape[0]

        # num_media_messages_user = num_media_messages(df_user)
    else:
        num_messages = df.shape[0]
        words = [word for message in df['message'] for word in message.split()]
        num_media_messages_user = df[df['message'].str.contains('image omitted|video omitted|sticker omitted')].shape[0]
        links = [link for message in df['message'] for link in extract.find_urls(message)]

    return num_messages, len(words), num_media_messages_user, len(links)

def fetch_most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'users':'name', 'count': 'percent'})
    return x, df

def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df_user = df[df['users'] == selected_user]
        temp = df_user[~df_user['message'].str.contains(r'\bimage\b|\bvideo\b|\bsticker\b|\bomitted\b')]
    else:
        temp = df[~df['message'].str.contains(r'\bimage\b|\bvideo\b|\bsticker\b|\bomitted\b')]

    def remove_stop_words(message):
        y =[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=300, height=300, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df_user = df[df['users'] == selected_user]
        temp = df_user[~df_user['message'].str.contains(r'\bimage\b|\bvideo\b|\bsticker\b|\bomitted\b')]
    else:
        temp = df[~df['message'].str.contains(r'\bimage\b|\bvideo\b|\bsticker\b|\bomitted\b')]

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])
    return most_common_df

def emoji_counter(selected_user, df):
    if selected_user != 'Overall':
        # Selects the user
        df_user = df[df['users'] == selected_user]

        emojis = []
        for message in df_user['message']:
            emojis.extend(emoji.demojize(message).split())
    else:
        # If 'Overall' is selected, consider all users
        emojis = []
        for message in df['message']:
            emojis.extend(emoji.demojize(message).split())

    # Remove non-emoji words
    emojis = [word for word in emojis if word.startswith(':') and word.endswith(':')]

    # Convert shortcode representations to actual emojis
    emojis = [emoji.emojize(e) for e in emojis]

    # Create a DataFrame with emoji counts
    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.items(), columns=['Emoji', 'Count']).sort_values(by='Count', ascending=False)

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        # Selects the user
        df_user = df[df['users'] == selected_user]
        timeline = df_user.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    else:
        timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        # Selects the user
        df_user = df[df['users'] == selected_user]
        daily_timeline = df_user.groupby('only_date').count()['message'].reset_index()
    else:
        daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity(selected_user, df):
    if selected_user != 'Overall':
        # Selects the user
        df_user = df[df['users'] == selected_user]
        return df_user['day_name'].value_counts()
    else:
        return df['day_name'].value_counts()

def month_activity(selected_user, df):
    if selected_user != 'Overall':
        # Selects the user
        df_user = df[df['users'] == selected_user]
        return df_user['month'].value_counts()
    else:
        return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        # Selects the user
        df_user = df[df['users'] == selected_user]
    else:
        df_user = df  # Use the entire DataFrame for 'Overall'

    user_heatmap = df_user.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
