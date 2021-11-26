from io import StringIO
import pickle
import streamlit as st
import requests
import pandas as pd
import pathlib
from pathlib import Path
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import io
import base64
import csv
from csv import writer

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

header_html = "<center><img src='data:image/png;base64,{}' style='width:230px;height:200px;'></center>".format(
    img_to_bytes("anime.png")
)
st.markdown(
    header_html, unsafe_allow_html=True,
)

def recommend(anime):
    index =animes[animes['title'] == anime].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_anime_names = []
    recommended_anime_genre = []
    recommended_anime_posters = []
    for i in distances[1:6]:
        
        response = requests.get(animes.iloc[i[0]].image_url)
        m = response.status_code
        if m == 404:
            img = Image.open('picture4.png')
            recommended_anime_posters.append(img)
        else:
            img = Image.open(io.BytesIO(response.content))
            recommended_anime_posters.append(img)

        recommended_anime_names.append(animes.iloc[i[0]].title)
        recommended_anime_genre.append(animes.iloc[i[0]].genre)

    return recommended_anime_names, recommended_anime_posters, recommended_anime_genre


#df = pd.read_csv("AnimeList.csv")
st.markdown("<h1 style='text-align: center; color: #00ced1;'>Anime Recommender System - Genres</h1><br><br>", unsafe_allow_html=True)
user_input = st.text_input("Please insert your name first")
st.write(user_input)

#st.header('Anime Recommender System - Genres')
animes = pickle.load(open('animeGenre.pkl','rb'))
similarity = pickle.load(open('similarityGenre.pkl','rb'))

anime_list = animes['title'].values
selected_anime = st.selectbox("Type or select a anime from the dropdown",  anime_list)


if st.button('Show Recommendation'):
    recommended_anime_names,recommended_anime_posters,recommended_anime_genre = recommend(selected_anime)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_anime_posters[0])
        st.text(recommended_anime_names[0])
        st.text("Genre: " + recommended_anime_genre[0])

    with col2:
        st.image(recommended_anime_posters[1])
        st.text(recommended_anime_names[1])
        st.text("Genre: " + recommended_anime_genre[1])

    with col3:
        st.image(recommended_anime_posters[2])
        st.text(recommended_anime_names[2])
        st.text("Genre: " + recommended_anime_genre[2])

    with col4:
        st.image(recommended_anime_posters[3])
        st.text(recommended_anime_names[3])
        st.text("Genre: " + recommended_anime_genre[3])

    with col5:
        st.image(recommended_anime_posters[4])
        st.text(recommended_anime_names[4])
        st.text("Genre: " + recommended_anime_genre[4])

    #for i in recommended_anime_names:
        #st.write(i)

st.markdown("<br>", unsafe_allow_html=True)
rate = st.selectbox("How many anime you like from this recommendation?",("0", "1", "2", "3", "4", "5"))
if st.button('Enter value'):
    ratevalue  = int(rate)
    
    reset = Path('reset.txt').read_text()
    resetcount = int(reset)

    count = Path('count.txt').read_text()
    countvalue  = int(count)

    if resetcount == 5:
        accuracy = (countvalue/25)*100
        #st.write("Recommendation accuracy is " + str(accuracy) + "%")
        rate  = 0
        pathlib.Path('count.txt').write_text(str(rate))
        a = 0
        pathlib.Path('reset.txt').write_text(str(a))

    else:

        a = resetcount + 1
        rate = ratevalue + countvalue
        st.write(str(a) + ' round with ' + str(rate) + " correct anime recommendation")
        pathlib.Path('count.txt').write_text(str(rate))
        pathlib.Path('reset.txt').write_text(str(a))


reset = Path('reset.txt').read_text()
resetcount = int(reset)
count = Path('count.txt').read_text()
countvalue  = int(count)
if resetcount == 5:
        row = []
        rows = []
        accuracy = (countvalue/25)*100
        st.write("Recommendation accuracy is " + str(accuracy) + "%")
        rate  = 0
        pathlib.Path('count.txt').write_text(str(rate))
        a = 0
        pathlib.Path('reset.txt').write_text(str(a))
      
        filename = "data.csv"
        row.append(accuracy)
        rows.append(user_input)
        with open(filename, 'a', newline='') as csvfile: 
           
            writer_object = writer(csvfile)
            
            writer_object.writerow(rows)  
            writer_object.writerow(row)  
            csvfile.close()
  
      
   
