import rdflib

def search_overview(title) -> list:
    global g
    query = """
    PREFIX : <https://www.themoviedb.org/kaggle-export/> 
    SELECT ?overview
    WHERE {
        ?movie a :Movie;
            :overview ?overview;
            :title ?movie_title.
        FILTER(CONTAINS(UCASE(?movie_title), UCASE("%s")))
    }""" % title.upper()

    query_result = g.query(query)

    result = [row[0] for row in query_result]

    return result


def search_title(title) -> list:
    global g
    query = """
    PREFIX : <https://www.themoviedb.org/kaggle-export/> 
    SELECT ?movie_title
    WHERE {
        ?movie a :Movie;
            :title ?movie_title.
        FILTER(CONTAINS(UCASE(?movie_title), UCASE("%s")))
    }""" % title.upper()

    query_result = g.query(query)

    result = [row[0] for row in query_result]

    return result


def actor_search(actor_name) -> list:
    global g
    query = """
    PREFIX : <https://www.themoviedb.org/kaggle-export/> 
    SELECT ?movie_title
    WHERE {
        ?movie a :Movie;
            :overview ?overview;
            :title ?movie_title.
        FILTER(CONTAINS(UCASE(?overview), UCASE("%s")))
    }""" % actor_name.upper()

    query_result = g.query(query)
    result = [row[0] for row in query_result]
    return result


if __name__ == '__main__':
    g = rdflib.Graph()
    g.parse("IAI_Team4_MovieFinder/TMDB.ttl", format='turtle')

    # zuerst durch web application title oder actor erhalten
    # hier wahrscheinlich while schleife und anfragen bearbeiten

    title = "avengers"
    actor = "julius caesar"

    actor_result = actor_search(actor)
    actor_result_strings = [title.toPython() for title in actor_result]
    print(actor_result_strings)

    title_result = search_title(title)
    title_result_strings = [title.toPython() for title in title_result]
    print(title_result_strings)

    overview_result = search_overview(title)
    overview_result_strings = [overview.toPython() for overview in overview_result]
    print(overview_result_strings)


