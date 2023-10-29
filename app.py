import streamlit as st
from data_ingestion import load_data, preprocess_data
from data_transformation import recommend_jobs

def main():
    st.title("Job Recommendation App")
    st.sidebar.header("Filters")

    skills_input = st.sidebar.text_input("Enter your skills (comma-separated):").lower().split(',')
    experience_input = st.sidebar.text_input("Enter your experience (optional):")
    location_input = st.sidebar.text_input("Enter your preferred location (optional):")

    df = load_data()
    df = preprocess_data(df)

    recommended_jobs = recommend_jobs(skills_input, experience_input, location_input, df)

    if st.button("Recommend Jobs"):
        st.table(recommended_jobs)

if __name__ == '__main__':
    main()
