import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum()]
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

def convert_post_time(post_time):
    try:
        days_ago = int(post_time.split(' ')[0])
        return days_ago
    except ValueError:
        return None

def recommend_jobs(skills_input, experience_input, location_input, data):
    # Preprocess user input
    skills_input = preprocess_text(' '.join(skills_input))

    # Filter based on user input
    filtered_jobs = data[data["Skills"].apply(lambda x: all(skill in x for skill in skills_input))]

    # Optionally, filter based on experience
    if experience_input:
        filtered_jobs = filtered_jobs[filtered_jobs["Experience_Required"] >= float(experience_input)]

    # Optionally, filter based on location
    if location_input:
        filtered_jobs = filtered_jobs[filtered_jobs["Locations"].str.contains(location_input, case=False, na=False)]

    # Convert "Post_Time" to numeric days ago
    filtered_jobs["Post_Time_Num"] = filtered_jobs["Post_Time"].apply(convert_post_time)

    # Sort by "Post_Time_Num" in descending order and get the top 5 jobs
    filtered_jobs = filtered_jobs.sort_values(by="Post_Time_Num", ascending=False).head(5)

    return filtered_jobs[["Job_Titles", "Company_Names", "Package_Details", "Locations", "Post_Url", "Post_Time"]]
