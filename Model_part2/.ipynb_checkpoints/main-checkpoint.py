import numpy as np
import pandas as pd
import spacy
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import tensorflow as tf


nlp = spacy.load("en_core_web_md")


def load_data(filter_data: bool = False, normalize: bool = False) -> tuple:
    filepath = "../data/movie_genres.csv"
    df = pd.read_csv(filepath, quotechar='"')

    action_movie_ids = df[df['Genre'] == 'Action']['MovieID']
    df['IsAction'] = df['MovieID'].isin(action_movie_ids)
    df.drop_duplicates(subset='MovieID', inplace=True)
    df.drop(columns=['Genre', 'MovieID'], inplace=True)

    X, y = df['Description'].to_numpy(), df['IsAction'].to_numpy()

    if filter_data:
        X = np.stack([filter_sentence(desc) for desc in X], axis=0)
    else:
        X = np.stack([nlp(desc).vector for desc in X], axis=0)

    if normalize:
        X = (X - np.mean(X, axis=0)) / (np.std(X, axis=0) + 1e-10)

    return X, y


def filter_sentence(sentence: str) -> np.ndarray:
    sentence = sentence.lower()
    doc = nlp(sentence)
    filtered_tokens = [token for token in doc
                       if token.is_alpha and not token.is_stop]
    mean_vector = np.mean([token.vector for token in filtered_tokens], axis=0)

    return mean_vector


def train_mlp(X_train, X_test, y_train, y_test):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(2, activation='softmax')
    ])
    model.compile(loss='categorical_crossentropy', optimizer='adam',
                  metrics=['accuracy'])

    y_train, y_test = tf.one_hot(y_train, depth=2), tf.one_hot(y_test, depth=2)

    model.fit(X_train, y_train, epochs=10, batch_size=32,
              validation_data=(X_test, y_test), verbose=0)
    pred = model.predict(X_test)

    pred = np.argmax(pred, axis=-1)
    y_test = np.argmax(y_test.numpy(), axis=-1)
    cm = confusion_matrix(y_test, pred)
    acc = accuracy_score(y_test, pred)

    print(f"Accuracy: {acc}\nConfusion Matrix:\n{cm}")


if __name__ == '__main__':
    for filter_data in [False,  True]:
        for normalize in [False, True]:
            X, y = load_data(filter_data=filter_data, normalize=normalize)

            data = train_test_split(X, y, test_size=0.2, random_state=0)

            print(f"Results for {filter_data=}, {normalize=}:")
            train_mlp(*data)


