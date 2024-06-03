import matplotlib.pyplot as plt
import pandas as pd  # pandas is used for data manipulation and analysis
import tensorflow_hub as hub
from sklearn.decomposition import PCA  # For performing Principal Component Analysis (PCA)
from sklearn.neighbors import NearestNeighbors


def encode_data(texts):
    model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    return model(texts)


def load_data():
    df = pd.read_csv('mymoviedb.csv')
    df.head()
    # keep only needed columns
    df = df[["Title", "Overview", "Poster_Url"]]
    df.head()
    return df


def recommend(text,nn,movies):
    # Generate the embedding for the input 'text' using the 'embed' function
    emb = encode_data([text])

    # Find the 10 nearest neighbors based on the computed embeddings using the NearestNeighbors model 'nn'
    neighbors = nn.kneighbors(emb, return_distance=False)[0]

    # Print the titles of the recommended movies based on the nearest neighbors

    recommended_movies = [movies['Title'].iloc[i] for i in neighbors]
    return recommended_movies


def before_serevr():
    movies = load_data()

    titles = list(movies['Overview'])

    embeddings = encode_data(titles)

    pca = PCA(n_components=2)
    data_pc2 = pca.fit_transform(embeddings)

    plt.figure(figsize=(11, 6))
    plt.title("Embedding space")
    plt.scatter(data_pc2[:, 0], data_pc2[:, 1])
    plt.show()

    nn = NearestNeighbors(n_neighbors=10)

    nn.fit(embeddings)
    return nn,movies
