import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # st.dataframe(df)
    st.title("Detailed Analysis of your Chats")
    st.markdown("====" * 22)

    # fetch unique users data

    user_list = df['users'].unique().tolist()
    user_list.remove('group-notification')
    user_list.sort()
    user_list.insert(0, "All Users")

    selected_user = st.sidebar.selectbox("Show analysis wrt:", user_list)

    if st.sidebar.button("Show Analysis"):
        col1, col2, col3, col4 = st.columns(4)

        num_messages, words, media, links = helper.fetch_stats(selected_user, df)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media ")
            st.title(media)

        with col4:
            st.header("Total Links ")
            st.title(links)
        st.markdown("====" * 22)

        # timeline (monthly- col1, daily-col2)

        new_df = helper.timeline_of_messages(selected_user, df)
        date_df = helper.daily_timeline(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.title("Monthly Timeline")
            fig, ax = plt.subplots()
            ax.plot(new_df['time'], new_df['messages'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.title("Daily Timeline")
            fig, ax = plt.subplots()
            ax.plot(date_df['date'], date_df['messages'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        st.markdown("====" * 22)

        # Activity by day and month
        days = helper.activity_day(selected_user, df)
        months = helper.activity_month(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:

            st.title("Activity By Day")
            fig, ax = plt.subplots()
            ax.bar(days.index, days.values, color="purple")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.title("Activity By Month")
            fig, ax = plt.subplots()
            ax.bar(months.index, months.values, color='orange')
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        st.markdown("====" * 22)

        # heatmap (day vs timeperiod)
        st.title("Activity Heatmap")
        heatmap_data = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heatmap_data)
        st.pyplot(fig)

        st.markdown("====" * 22)

        # finding busiest people in the group(only for group chat)
        if selected_user == 'All Users':
            st.title('Most Active Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='green')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
            st.markdown("====" * 22)

        # WordCloud (col1) and Most common words (col2)

        df_wc = helper.create_word_cloud(selected_user, df)
        com_word = helper.most_common_words(selected_user, df)
        col1, col2 = st.columns(2)
        # word cloud
        with col1:
            st.title("Words Used")
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

        # most common words
        with col2:
            fig, ax = plt.subplots()
            ax.barh(com_word[0], com_word[1])
            plt.xticks(rotation="vertical")
            st.title("Most common words")
            st.pyplot(fig)
