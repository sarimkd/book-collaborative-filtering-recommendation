import streamlit as st
import pickle
import numpy as np

# Set page title
st.set_page_config(page_title="Book Recommender")

# Load pre-processed data from pickle files
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('final_pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Define the main function of the app
def main():
    st.title('Book Recommendation System')  # Set the title of the app

    # Create a sidebar with page options
    page = st.sidebar.selectbox('Choose Recommendation System', ['Top Rated', 'Collaborative Filtering'])

    # Based on the selected page, display the appropriate content
    if page == 'Top Rated':
        show_home_page()  # Display popular books
    elif page == 'Collaborative Filtering':
        show_recommend_page()  # Display book recommendations

    # Developer Information
    linkedin = "https://www.linkedin.com/in/sarimkhanskd"
    github = "https://github.com/sarimkd"
    st.sidebar.write("Developed by [Sarim Khan](%s)" % linkedin, "| [GitHub](%s)" % github)
    st.sidebar.write("Email : sarimkhanskd@gmail.com")

# Define a function to display the "Top Rated" page
def show_home_page():
    st.subheader('Recommended Books by Rating')  # Display a header for the popular books section
    
    # Iterate through popular books and display their information
    for idx, row in popular_df.iterrows():
        col1, col2 = st.columns(2)
        with col1:
            st.image(row['Image-URL-M'], width=130)
        with col2:
            st.write(f"**Title:** {row['Book-Title']}")
            st.write(f"**Author:** {row['Book-Author']}")
            st.write(f"**Votes:** {row['num_ratings']}")
            st.write(f"**Rating:** {row['avg_ratings']}")
            st.write('')

# Define a function to display the "Collaborative Filtering" page
def show_recommend_page():
    st.subheader('Recommended Books by Collaborative Filtering')  # Display a header for the book recommendation section

    user_input = st.selectbox('Select a book title:', pt.index)
    
    # When the "Recommend" button is clicked
    if st.button('Recommend'):
        index = np.where(pt.index == user_input)[0][0]  # Find the index of the input book
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        # Display recommended books and their information
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            col1, col2 = st.columns(2)
            with col1:
                st.image(temp_df['Image-URL-M'].values[0], width=130)
            with col2:
                st.write(f"**Title:** {temp_df['Book-Title'].values[0]}")
                st.write(f"**Author:** {temp_df['Book-Author'].values[0]}")
            

# Check if the script is being run directly and call the main function
if __name__ == '__main__':
    main()