import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns



st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    st.dataframe(df)
    # Sentiment analysis for each message
    #df['Sentiment'] = df['message'].apply.helper.analyze_sentiment()
    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    #creating a button to show analysis
    if st.sidebar.button("Show Analysis"):
        total_messages,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(total_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links shared")
            st.title(num_links)
        #Monthly timeline
        st.title("Monthly Chat Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        # weekly activity
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        # monthly activity
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud (Top Frequent words)
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title('Most commmon words')
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # emoji analysis
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        if emoji_df.shape[0] > 0:
            col1, col2 = st.columns(2)
            with col1:
              st.dataframe(emoji_df)
            with col2:
              fig, ax = plt.subplots()
              ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
              st.pyplot(fig)
        else:
            st.write("No Emojis Send by this user")

        #sentimental analysis

        # Plot sentiment distribution
        st.title("Sentiment Distribution:")
        sentiment_df = helper.analyze_sentiments(selected_user,df)
        colors = {'Positive': 'purple', 'Neutral': 'orange', 'Negative': 'pink'}

        if sentiment_df.shape[0] > 0:
            fig, ax = plt.subplots()
            sentiment_df['Sentiment'].value_counts().plot(kind='bar',color='green', ax=ax)
            st.pyplot(fig)
        else:
            st.write("No Sentiments for Emoji")




            






