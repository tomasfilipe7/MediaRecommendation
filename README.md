# MediaRecommendation
Use of the application: <br/>
-
<b>python3 main.py [movie or series name] </b><br />
or <br />
<b>python3 main.py</b> <br />
and a prompt will appear:  <br />
"Write a series or movies to get recommendation:" <b>[insert movie or series name]</b><br />

Requirements: <br/>
-
pandas==1.4.1 </br>
scikit-learn==1.0.2 </br>
python-Levenshtein==0.12.2 </br>
</br>
To install those requirements, just run: <b> pip install -r requirements.txt </b>

About the application: <br/>
-
This application will return a list of 10 movies or series based on the metadata of a movie or tv show given by the user <br/>
This recommendation list is calculated via the cosine similarity between the metadata of multiple attributes of each movie/tv show. <br/>
If the media title a user is trying to enter is not present in the database, a prompt will show up, suggesting the most similar entry on the database <br/>
This similarity is computed via the Levenshtein distance. <br/>

Dataset: <br/>
-
This application uses a dataset of the movies and series on Netflix platform, provided by https://www.kaggle.com/shivamb/netflix-shows
