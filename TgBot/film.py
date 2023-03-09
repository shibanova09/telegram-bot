from imdb import Cinemagoer
import pyodbc

def fill(year, country, genre):
    res, directors, genres = [], [], []
    year = year.split('-')
    conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                          "Server=DESKTOP-M089Q5L\SQLSERVER;"
                          "Database=Films;"
                          "Trusted_Connection=yes;")
    cursor = conn.cursor()
    id_cursor = cursor.execute(f"select top 1 name_rus from all_movies where (movie_year between {year[0]} and {year[1]} and countries='[{country}]' and genres='[{genre}]') order by newid()")
    for row in id_cursor:
        res.append(str(row))
    id_str = str(res[0])
    id_str = id_str[2:-4]
    ia = Cinemagoer()
    movie = ia.search_movie(id_str)
    movie = ia.get_movie(str(movie[0].movieID))
    for director in movie['director']:
        directors.append(director['name'])
    for genre in movie['genres']:
        genres.append(genre)
    return f"{id_str}\nГод выхода:{movie['year']}\nРежиссер(ы):{directors}\nЖанр(ы):{genres}"