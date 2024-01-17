import streamlit as st
import matplotlib.pyplot as plt
import preprocessor, helper
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates


st.sidebar.title("Whatsapp Chat Analyser")
# this is displayed on sidebar as title

uploaded_file = st.sidebar.file_uploader("Choose a file")
# this chooses the file
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df =preprocessor.preprocess(data)

    # st.dataframe(df)

    # fetch unique records or users

    user_list = df['users'].unique().tolist()
    # user_list.remove('NEU Housing Spring 2022')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("Show analysis of:", user_list)

    if st.sidebar.button("Generate Analysis"):
        num_messages, words, num_media_messages_user, links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)


        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Images")
            st.title(num_media_messages_user)

        with col4:
            st.header("Total Links")
            st.title(links)

        # Monthly number of messages

        # timeline = helper.monthly_timeline(selected_user, df)
        # fig, ax = plt.subplots()
        # ax.plot(timeline['time'], timeline['message'])
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)

        timeline = helper.monthly_timeline(selected_user, df)
        time = timeline['time']
        messages = timeline['message']

        fig, ax = plt.subplots()
        ax.plot(time, messages, color='green')

        # Set the x-axis ticks to every alternate element
        plt.xticks(range(0, len(time), 2), time[::2], rotation='vertical')

        st.pyplot(fig)

        #  Daily Timeline

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        time = daily_timeline['only_date']
        messages = daily_timeline['message']

        fig, ax = plt.subplots()
        ax.plot(time, messages, color='black')

        # Set the x-axis ticks to every alternate element
        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        # Activity map

        st.title("Activity map")

        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy Month")
            busy_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color ='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        st.title("Weekly Activity map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)




        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.fetch_most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.title('Number of messages')
                ax.bar(x.index, x.values, color = 'orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.title('Percentage of messages')
                st.dataframe(new_df)


        st.title("Word Cloud")

        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

    # Most common words

        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df['Word'], most_common_df['Frequency'])
        st.title("Most used words")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # emoji analysis
        # emoji analysis
        emoji_df = helper.emoji_counter(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.title("Count")
            st.dataframe(emoji_df)

        with col2:
            st.title("Pie Chart")
            # Limit the number of emojis displayed
            max_display = 10  # Set the maximum number of emojis to display
            if len(emoji_df) > max_display:
                # Display only the top N emojis
                top_emojis = pd.concat([emoji_df.head(max_display), pd.DataFrame(
                    {'Emoji': ['Others'], 'Count': [emoji_df.iloc[max_display:]['Count'].sum()]})], ignore_index=True)
            else:
                top_emojis = emoji_df

            fig, ax = plt.subplots()
            ax.pie(top_emojis['Count'], labels=top_emojis['Emoji'], autopct='%0.1f%%')
            st.pyplot(fig)


