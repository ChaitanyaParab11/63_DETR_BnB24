import streamlit as st
import pickle
import pandas as pd


def recommend(text):
    # resume_index = data[data['description'] == text].index[0]

    # Assuming `data` is your DataFrame and `text` is the description you're searching for
    filtered_data = data[data['description'] == text]

    if not filtered_data.empty:
        resume_index = filtered_data.index[0]
        # Proceed with operations using resume_index
    else:
        # Handle the case where the description does not match any rows
        print("No matching description found.")
        resume_index = None  # or any other fallback action

    distances = similarity[resume_index]
    resume_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x: x[1])[1:7]

    recommended_resume = []
    # recommended_videos_posters = []

    for i in resume_list:
        recommended_resume.append(data.iloc[i[0]].resume_id)


    # return recommended_videos, recommended_videos_posters
    return recommended_resume


data_dict = pickle.load(open('data_dict.pkl', 'rb'))
data = pd.DataFrame(data_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Resume Analyzer')

title = "Enter Job Description"
user_input = st.text_area(title, height=300)


if st.button('Recommend'):
    resume = recommend(user_input)

    if resume:  # This checks if the list is not empty
        st.write(resume[0])
    else:
        st.write('No data available')

