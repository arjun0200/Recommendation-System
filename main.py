from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np

df_popular = pickle.load(open("popular.pkl", "rb"))
books = pickle.load(open("books.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
similarity_scores = pickle.load(open("similarity_scores.pkl", "rb"))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(df_popular['Book-Title'].values),
                           author=list(df_popular['Book-Author'].values),
                           image=list(df_popular['Image-URL-M'].values),
                           votes=list(df_popular['Num_rating'].values),
                           rating=list(df_popular['Num_rating_avg'].values)
                           )


@app.route('/recommend')
def recommend_gui():
    return render_template('recommend.html')


# arjun
@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)

    return render_template('recommend.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
