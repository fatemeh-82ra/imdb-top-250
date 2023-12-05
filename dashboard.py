# import streamlit as st
# import pandas as pd
# import mysql.connector
# import altair as alt
# import networkx as nx
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
#
# connect = mysql.connector.connect(
#     host="127.0.0.1",
#     user="newuser",
#     password="12345678",
#     database="imdb"
# )
# cursor = connect.cursor()
#
# # first
# start_year = st.text_input('Start Year')
# end_year = st.text_input('End Year')
# movies_query = "SELECT * FROM movie WHERE Year >= %s AND Year <= %s"
# cursor.execute(movies_query, (start_year, end_year))
# results = cursor.fetchall()
# column_names = [out[0] for out in cursor.description]
# data = pd.DataFrame(results, columns=column_names)
# st.table(data)
#
# # second
# min_time = st.text_input('Minimum Time')
# max_time = st.text_input('Maximum Time')
# query = "SELECT * FROM movie WHERE runtime >= %s AND runtime <= %s"
# cursor.execute(query, (min_time, max_time))
# results = cursor.fetchall()
# column_names = [out[0] for out in cursor.description]
# data1 = pd.DataFrame(results, columns=column_names)
# st.table(data1)
#
# # third
# actors_query = "SELECT DISTINCT name FROM person"
# cursor.execute(actors_query)
# actors = [result[0] for result in cursor.fetchall()]
# selected_actors = st.text_input('Enter Actor Name(s) (comma-separated)', key='actors')
# selected_actors = [actor.strip() for actor in selected_actors.split(',')]
# selected_actors = [actor for actor in selected_actors if actor]
# query = """
#     SELECT m.title, m.year, m.runtime, m.parental_guide, m.gross_us_canada
#     FROM movie AS m
#     JOIN cast AS c ON m.id = c.movie_id
#     JOIN person AS p ON c.person_id = p.id
#     WHERE p.name IN ({})
# """.format(', '.join(['%s'] * len(selected_actors)))
# if selected_actors:
#     cursor.execute(query, tuple(selected_actors))
#     results = cursor.fetchall()
#     column_names = [out[0] for out in cursor.description]
#     data2 = pd.DataFrame(results, columns=column_names)
#     st.table(data2)
#
# # forth
# genres_query = "SELECT DISTINCT genre FROM genre_movie"
# cursor.execute(genres_query)
# genres = [result[0] for result in cursor.fetchall()]
# selected_genre = st.selectbox('Select Genre', genres)
# query = """
#     SELECT m.title, m.year, m.runtime, m.parental_guide, m.gross_us_canada
#     FROM movie AS m
#     JOIN genre_movie AS g ON m.id = g.movie_id
#     WHERE g.genre = %s
#     AND m.id NOT IN (
#         SELECT movie_id
#         FROM genre_movie
#         GROUP BY movie_id
#         HAVING COUNT(*) > 1
#     )
# """
# cursor.execute(query, (selected_genre,))
# results = cursor.fetchall()
# column_names = [out[0] for out in cursor.description]
# data3 = pd.DataFrame(results, columns=column_names)
# st.table(data3)
#
# # fifth
# query = """
#     SELECT m.title, m.gross_us_canada
#     FROM movie AS m
#     ORDER BY m.gross_us_canada DESC
#     LIMIT 10
# """
# cursor.execute(query)
# results = cursor.fetchall()
# column_names = [out[0] for out in cursor.description]
# data = pd.DataFrame(results, columns=column_names)
# chart = alt.Chart(data).mark_bar().encode(
#     x=alt.X('title', sort=alt.EncodingSortField(order='descending')),
#     y='gross_us_canada',
#     tooltip=['title', 'gross_us_canada']
# ).properties(
#     title='Top 10 Highest Sell Movies',
#     # width=alt.Step(1)
# )
# st.altair_chart(chart, use_container_width=True)
#
# # sixth
# query = """
#     SELECT p.name AS actor, COUNT(*) AS movie_count
#     FROM person AS p
#     JOIN cast AS c ON p.id = c.person_id
#     GROUP BY p.name
#     ORDER BY movie_count DESC
#     LIMIT 5
# """
# cursor.execute(query)
# results = cursor.fetchall()
# column_names = [desc[0] for desc in cursor.description]
# data = pd.DataFrame(results, columns=column_names)
# chart = alt.Chart(data).mark_bar().encode(
#     x=alt.X('actor', sort=alt.EncodingSortField(order='descending')),
#     y='movie_count'
# ).properties(
#     title='Top 5 Most Frequent Actors',
#     width=alt.Step(40)
# )
# st.altair_chart(chart, use_container_width=True)
#
# # seventh
# query = """
#     SELECT genre, COUNT(*) AS count
#     FROM genre_movie
#     GROUP BY genre
#
# """
# cursor.execute(query)
# results = cursor.fetchall()
# column_names = [out[0] for out in cursor.description]
# data = pd.DataFrame(results, columns=column_names)
# chart = alt.Chart(data).mark_arc().encode(
#     alt.Color('genre:N', legend=alt.Legend(title='Genre')),
#     tooltip=['genre_name:N', 'count:Q'],
#     size='count:Q',
#     theta='count:Q'
# ).properties(
#     title='Genre'
#     # width=500,
#     # height=400
# )
# st.altair_chart(chart, use_container_width=True)
#
# # eighth
# query = """
#     SELECT parental_guide, COUNT(*) AS count
#     FROM movie
#     GROUP BY parental_guide
# """
# cursor.execute(query)
# results = cursor.fetchall()
# column_names = [out[0] for out in cursor.description]
# data = pd.DataFrame(results, columns=column_names)
# chart = alt.Chart(data).mark_arc().encode(
#     alt.Color('parental_guide:N', legend=alt.Legend(title='parental guide')),
#     tooltip=['parental_guide:N', 'count:Q'],
#     size='count:Q',
#     theta='count:Q'
# ).properties(
#     title='parental guide'
#     # width=500,
#     # height=400
# )
# st.altair_chart(chart, use_container_width=True)
#
# # ninth
# query = """
# SELECT g.Genre, m.parental_guide, COUNT(*) AS count
# FROM movie m
#          JOIN genre_movie g ON m.id = g.Movie_id
# GROUP BY g.Genre, m.parental_guide
# """
# cursor.execute(query)
# results = cursor.fetchall()
# column_names = [out[0] for out in cursor.description]
# data = pd.DataFrame(results, columns=column_names)
# grouped_data = data.groupby(['Genre', 'parental_guide']).sum().reset_index()
# chart_data = pd.pivot_table(grouped_data, values='count', index='Genre', columns='parental_guide', fill_value=0)
# st.bar_chart(chart_data)
#
# # tenth
# user_genre = st.text_input("Enter the genre:")
#
# cursor.execute("""
# SELECT m.title, m.gross_us_canada
# FROM movie AS m
#          JOIN genre_movie AS g ON m.id = g.movie_id
# WHERE g.genre = %s
# ORDER BY m.gross_us_canada DESC
# LIMIT 10
# """, (user_genre,))
# results = cursor.fetchall()
# data = {
#     'Title': [result[0] for result in results],
#     'Gross Sales': [result[1] for result in results]
# }
# df = pd.DataFrame(data)
# chart = alt.Chart(df).mark_bar().encode(
#     x=alt.X('Title', sort=alt.EncodingSortField(order='descending')),
#     y='Gross Sales'
# )
# chart = chart.properties(
#     # width=alt.Step(80),
#     title=f"Top selling Movies in the {user_genre} genre"
# )
# st.altair_chart(chart, use_container_width=True)
#
#
# # eleventh
# def get_similar_movies(movie_title):
#     cursor.execute("""
#         SELECT movie.id, person.id
#         FROM movie
#          JOIN crew ON movie.id = crew.movie_id
#          JOIN person ON crew.person_id = person.id
#         WHERE movie.title = %s AND crew.role = 'Director'
#     """, (movie_title,))
#     movie_data = cursor.fetchone()
#     if movie_data:
#         movie_id, director_id = movie_data
#         cursor.execute("""
#             SELECT movie.title
#             FROM movie
#              JOIN crew ON movie.id = crew.movie_id
#             WHERE crew.person_id = %s AND crew.role = 'Director' AND movie.id != %s
#         """, (director_id, movie_id))
#         similar_movies = cursor.fetchall()
#         if similar_movies:
#             return similar_movies
#     cursor.execute("""
#         SELECT movie.title
#         FROM movie
#          JOIN genre_movie ON movie.id = genre_movie.movie_id
#         WHERE genre_movie.genre IN (
#             SELECT genre_movie.genre
#             FROM movie
#              JOIN genre_movie ON movie.id = genre_movie.movie_id
#             WHERE movie.title = %s
#         ) AND movie.title != %s
#         GROUP BY movie.title
#         HAVING COUNT(DISTINCT genre_movie.genre) = 2
#     """, (movie_title, movie_title))
#     similar_movies = cursor.fetchall()
#     if similar_movies:
#         return similar_movies
#     return None
#
#
# def main():
#     st.title("Movie Recommendation System")
#     movie_title = st.text_input("Enter a movie title:")
#     if st.button("Get Recommendations"):
#         similar_movies = get_similar_movies(movie_title)
#         if similar_movies:
#             st.success("Recommended Movies:")
#             for movie in similar_movies:
#                 st.write(movie[0])
#         else:
#             st.warning("No recommendations found.")
#
#
# if __name__ == '__main__':
#     main()
#
# # twelfth
# cursor.execute("SELECT DISTINCT genre FROM genre_movie")
# genres = cursor.fetchall()
#
# for genre in genres:
#     st.header(f"Genre: {genre[0]}")
#     cursor.execute("""
#         SELECT s.storyline
#         FROM storyline AS s
#          JOIN movie AS m ON s.movie_id = m.id
#          JOIN genre_movie AS g ON m.id = g.movie_id
#         WHERE g.genre = %s
#     """, (genre[0],))
#     rows = cursor.fetchall()
#     storylines = [row[0] for row in rows]
#     all_storylines = " ".join(storylines)
#     wordcloud = WordCloud(width=300, height=200).generate(all_storylines)
#     st.image(wordcloud.to_image())
#
# # thirteenth
# query = '''
#            SELECT p1.id AS actor1_id, p1.name AS actor1_name, p2.id AS actor2_id, p2.name AS actor2_name, COUNT(*) AS num_movies
#            FROM person p1
#            JOIN cast c1 ON p1.id = c1.person_id
#            JOIN cast c2 ON c1.movie_id = c2.movie_id AND c1.person_id != c2.person_id
#            JOIN person p2 ON c2.person_id = p2.id
#            GROUP BY p1.id, p1.name, p2.id, p2.name
#        '''
# cursor.execute(query)
# resultttttt = cursor.fetchall()
# graph = nx.Graph()
# for row in resultttttt:
#     actor1_id = row[0]
#     actor1_name = row[1]
#     actor2_id = row[2]
#     actor2_name = row[3]
#     num_movies = row[4]
#     graph.add_node(actor1_id, name=actor1_name)
#     graph.add_node(actor2_id, name=actor2_name)
#     graph.add_edge(actor1_id, actor2_id, weight=num_movies)
# pos = nx.fruchterman_reingold_layout(graph, k=0.13)
# fig, ax = plt.subplots()
# nx.draw_networkx(graph, pos=pos, with_labels=True, ax=ax, node_size=10, font_size=3, width=0.5)
# st.pyplot(fig)
# cursor.close()
# connect.close()
