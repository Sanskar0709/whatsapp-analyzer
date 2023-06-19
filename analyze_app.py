import streamlit as st
import matplotlib.pyplot as plt
import preprocessor,helper

st.sidebar.title("whatsapp chat analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    # st.text(data)
    df=preprocessor.preprocess(data)

    st.dataframe(df)

    #fetch unique user

    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Members",user_list)

    if st.sidebar.button("Start Analyzing"):

        num_messages,words,num_media , num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total messages')
            st.title(num_messages)
        with col2:
            st.header('Total words')
            st.title(words)
        with col3:
            st.header("Media messages")
            st.title(num_media)
        with col4:
            st.header("LINKS shared")
            st.title(num_links)
        #finding the busiest user
        if selected_user =="Overall":
            st.title('Most active users')
            x, newdf = helper.fetch_activeuser(df)
            figure, ax = plt.subplots()

            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(figure)
            with col2:
                st.dataframe(newdf)
        #world cloud
        st.title("world cloud")
        df_wc = helper.create_cloud(selected_user, df)
        fig, ax =plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #commonwords
        commwords = helper.commonwords(selected_user,df)
        st.dataframe(commwords)





