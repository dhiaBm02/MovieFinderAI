import pandas as pd

def search_overview(title) -> list:
    global df
    movie_index = df[df['Title'] == title].index[0]
    movie_overview = df.iloc[movie_index,2]

    return movie_overview

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    df = pd.read_csv('mymoviedb.csv')


    print(search_overview("Encanto"))