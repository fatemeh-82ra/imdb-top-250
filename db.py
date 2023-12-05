import mysql.connector
import csv
import re

mysqlserver = mysql.connector.connect(
    host="127.0.0.1",
    user="newuser",
    password="12345678",
    database="IMDB"
)
cursor = mysqlserver.cursor()
# creating movie table
cursor.execute(
    "CREATE TABLE movie (id VARCHAR(8) PRIMARY KEY , Title VARCHAR(128), Year INT, Runtime INT, parental_guide VARCHAR(8), Gross_Us_Canada INT)"
)

# creating person table
cursor.execute(
    "CREATE TABLE person (id VARCHAR(8) PRIMARY KEY, Name VARCHAR(32))"
)

# creating cast table
create_table_3 = '''
CREATE TABLE cast (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Movie_id VARCHAR(8),
    Person_id VARCHAR(8),
    FOREIGN KEY (Movie_id) REFERENCES movie(id),
    FOREIGN KEY (Person_id) REFERENCES person(id)
)AUTO_INCREMENT = 1
'''
cursor.execute(create_table_3)

# creating crew table
create_table_4 = '''
CREATE TABLE crew (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Movie_id VARCHAR(8),
    Person_id VARCHAR(8),
    Role VARCHAR(8),
    FOREIGN KEY (Movie_id) REFERENCES movie(id),
    FOREIGN KEY (Person_id) REFERENCES person(id)
)AUTO_INCREMENT = 1
# '''
cursor.execute(create_table_4)

# creating genre table
create_table_5 = '''
CREATE TABLE genre_movie (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Movie_id VARCHAR(8),
    Genre VARCHAR(16),
    FOREIGN KEY (Movie_id) REFERENCES movie(id)
)AUTO_INCREMENT = 1
'''
cursor.execute(create_table_5)

# creating storyline table
create_table_6 = '''
    CREATE TABLE storyline (
        Movie_id VARCHAR(8),
        storyline TEXT,
        FOREIGN KEY (Movie_id) REFERENCES movie(id)
    )
'''
cursor.execute(create_table_6)

# movie
query_1 = """
INSERT INTO movie (id, Title, Year, Runtime, Parental_Guide, Gross_Us_Canada)
VALUES (%s, %s, %s, %s, %s, %s)
"""
movies_data = []
with open('top_250_movies.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        movie_data = {
            'id': re.sub(r'\D', '', row['movie_id']),
            'title': row['title'],
            'year': int(row['year']),
            'runtime': int(row['runtime']),
            'parental_guide': row['parental_guide'],
            'gross_us_canada': row['gross_us_canada']
        }
        movies_data.append(movie_data)
for movie_data in movies_data:
    if movie_data['parental_guide'] in [None, '', 'Not Rated']:
        movie_data['parental_guide'] = 'Unrated'

    gross_us_canada = movie_data['gross_us_canada']
    if gross_us_canada is None or gross_us_canada.strip() == '':
        gross_us_canada = None
    else:
        gross_us_canada = gross_us_canada.replace('$', '').replace(',', '')

    cursor.execute(query_1, (
        movie_data['id'],
        movie_data['title'],
        movie_data['year'],
        movie_data['runtime'],
        movie_data['parental_guide'],
        gross_us_canada
    ))

# person
with open('top_250_movies.csv', 'r', encoding='utf-8-sig') as file:
    csv_data = csv.reader(file)
    next(csv_data)
    for row in csv_data:
        writer_ids = eval(row[8])
        star_ids = eval(row[10])
        director_id = re.sub(r'\D', '', row[6])

        for writer_id, writer_name in zip(writer_ids, eval(row[9])):
            select_query = "SELECT id FROM person WHERE id = %s"
            cursor.execute(select_query, (writer_id,))
            existing_writer = cursor.fetchone()

            if not existing_writer:
                insert_query = "INSERT INTO person (id, Name) VALUES (%s, %s)"
                writer_data = (writer_id, writer_name)
                cursor.execute(insert_query, writer_data)

        for star_id, star_name in zip(star_ids, eval(row[11])):
            select_query = "SELECT id FROM person WHERE id = %s"
            cursor.execute(select_query, (star_id,))
            existing_star = cursor.fetchone()

            if not existing_star:
                insert_query = "INSERT INTO person (id, Name) VALUES (%s, %s)"
                star_data = (star_id, star_name)
                cursor.execute(insert_query, star_data)

        select_query = "SELECT id FROM person WHERE id = %s"
        cursor.execute(select_query, (director_id,))
        existing_director = cursor.fetchone()

        if not existing_director:
            insert_query = "INSERT INTO person (id, Name) VALUES (%s, %s)"
            director_name = row[7]
            director_data = (director_id, director_name)
            cursor.execute(insert_query, director_data)

# cast
with open('top_250_movies.csv', 'r', encoding='utf-8-sig') as file:
    csv_data = csv.reader(file)
    next(csv_data)
    for row in csv_data:
        movie_id = re.sub(r'\D', '', row[0])
        star_ids = eval(row[10])
        for star_id in star_ids:
            insert_query = "INSERT INTO cast (Movie_id, Person_id) VALUES (%s, %s)"
            cast_data = (movie_id, star_id)
            cursor.execute(insert_query, cast_data)

# crew
with open('top_250_movies.csv', 'r', encoding='utf-8-sig') as file:
    csv_data = csv.reader(file)
    next(csv_data)
    for row in csv_data:
        movie_id = re.sub(r'\D', '', row[0])
        director_id = re.sub(r'\D', '', row[6])

        insert_query = "INSERT INTO crew (Movie_id, Person_id, Role) VALUES (%s, %s, %s)"
        director_data = (movie_id, director_id, "Director")
        cursor.execute(insert_query, director_data)

        writer_ids = eval(row[8])
        writer_names = eval(row[9])
        for writer_id, writer_name in zip(writer_ids, writer_names):
            insert_query = "INSERT INTO crew (Movie_id, Person_id, Role) VALUES (%s, %s, %s)"
            writer_data = (movie_id, writer_id, "Writer")
            cursor.execute(insert_query, writer_data)

# genre
with open('top_250_movies.csv', 'r', encoding='utf-8-sig') as file:
    csv_data = csv.reader(file)
    next(csv_data)
    for row in csv_data:
        movie_id = re.sub(r'\D', '', row[0])
        genres = row[5].replace("[", "").replace("'", "").replace("]", "").split(',')

        for genre in genres:
            insert_query = "INSERT INTO genre_movie (Movie_id, Genre) VALUES (%s, %s)"
            genre_data = (movie_id, genre.strip())
            cursor.execute(insert_query, genre_data)
# storyline
with open('top_250_movies.csv', 'r', encoding='utf-8-sig') as file:
    csv_data = csv.reader(file)
    next(csv_data)
    for row in csv_data:
        movie_id = re.sub(r'\D', '', row[0])
        storyline = row[13]
        insert_query = "INSERT INTO storyline (Movie_id, storyline) VALUES (%s, %s)"
        story_data = (movie_id, storyline.strip())
        cursor.execute(insert_query, story_data)
mysqlserver.commit()
cursor.close()
mysqlserver.close()
