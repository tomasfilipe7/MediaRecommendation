import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import Levenshtein
import sys

path = "Datasets"


def get_genres(listed_in):
    genres = listed_in.split(", ")
    return genres


def get_cast(cast):
    if str(cast) != "nan":
        _cast = cast.split(", ")
        return _cast
    return ["NaN"]


def proc_data(dataframe):
    dataframe["cast"] = dataframe["cast"].apply(get_cast)
    dataframe["listed_in"] = dataframe["listed_in"].apply(get_genres)
    return dataframe


def normalize_data(data):
    if isinstance(data, list):
        return [str.lower(d.replace(" ", "")) for d in data]
    else:
        return str.lower(str(data).replace(" ", ""))


def get_LevenshteinDistance(string_1, string_2):
    return Levenshtein.distance(string_1, string_2)


def make_soup(features):
    return ' '.join(features['cast']) + ' ' + features['director'] + ' ' + features['description'] + ' ' + ' '.join(
        features['listed_in'])


netflix_titles_df = pd.read_csv(path + "/netflix_titles.csv")
features = ["type", "cast", "director", "description", "listed_in"]
netflix_titles_df = proc_data(netflix_titles_df)
for feature in features:
    netflix_titles_df[feature] = netflix_titles_df[feature].apply(normalize_data)
netflix_titles_df["title_clean"] = netflix_titles_df["title"].apply(normalize_data)
netflix_titles_df["soup"] = netflix_titles_df.apply(make_soup, axis=1)

count_vectorizer = CountVectorizer(stop_words="english")
count_matrix = count_vectorizer.fit_transform(netflix_titles_df["soup"])
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

netflix_titles_df = netflix_titles_df.reset_index()
indices = pd.Series(netflix_titles_df.index, index=netflix_titles_df["title_clean"]).drop_duplicates()


def get_recommendations(title, cosine_sim=cosine_sim2):
    _title = str.lower(title).replace(" ", "")
    if _title not in indices:
        distance_v = netflix_titles_df["title_clean"].apply(lambda x: Levenshtein.distance(_title, x))
        distance_list = list(enumerate(distance_v))
        closest_index = sorted(distance_list, key=lambda x: x[1])[0]
        closest_title = netflix_titles_df["title"].iloc[closest_index[0]]
        choice = input("Could not find {}. Did you mean {}? (S/n): ".format(title, closest_title))
        if choice != "n":
            return get_recommendations(closest_title)
        else:
            return
        return
    idx = indices[_title]
    similarity_scores = list(enumerate(cosine_sim[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:11]
    # (a, b) where a is id of movie, b is similarity_scores
    movies_indices = [ind[0] for ind in similarity_scores]
    movies = netflix_titles_df["title"].iloc[movies_indices]
    return movies


def main():
    if len(sys.argv) < 2:
        movie = input("Write a series or movies to get recommendation: ")
    else:
        movie = ""
        for i in range(1, len(sys.argv)):
            movie += sys.argv[i] + " "
    recomendations = get_recommendations(movie)
    if recomendations is not None:
        print("If you liked {}, you might also like: ".format(movie))
        for recomendation in recomendations:
            print(recomendation)
    return


if __name__ == '__main__':
    main()

