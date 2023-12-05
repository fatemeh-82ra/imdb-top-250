import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start_time = time.time()
count = 10
session = requests.Session()
retry = Retry(connect=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
headers = {
    "Accept-Encoding": "*",
    "Connection": "keep-alive",
    'Accept-Language': 'en-US,en;q=0.5',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
}
response = session.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
series_containers = soup.find_all('div', class_='sc-b51a3d33-0 hKhnaG cli-children')
series_data = []

for container in series_containers:
    count -= 1
    series_name = container.find('div',
                                 class_='ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b51a3d33-7 huNpFl cli-title').text.strip()
    series_name = series_name[series_name.index('.') + 1:].strip()
    years = container.find('span', class_='sc-b51a3d33-6 faLXbD cli-title-metadata-item').text.strip()
    parental_guide = container.find_all('span')
    if len(parental_guide) == 8:
        parental_guide = parental_guide[2].text.strip()
    else:
        parental_guide = ''
    times = container.find_all_next('span', class_='sc-b51a3d33-6 faLXbD cli-title-metadata-item')[
        1].text.strip()
    hours, minutes = times.split('h') if 'h' in times else (0, times)
    hours = int(hours)
    minutes = int(minutes[:-1].strip()) if minutes else 0
    total_minutes = hours * 60 + minutes
    link_element = container.find('div',
                                  class_='ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b51a3d33-7 huNpFl cli-title').a[
        'href']
    movies_id = []
    movie_id = [re.search(r'/title/tt(\d+)/', link_element).group(1)]
    complete_url = f"https://www.imdb.com{link_element}"
    driver = webdriver.Edge()
    driver.get(complete_url)
    try:
        story = driver.find_element(By.XPATH, '//div[@data-testid="storyline-header"]')
        driver.execute_script('arguments[0].scrollIntoView(true)', story)

        wait = WebDriverWait(driver, 15)
        elements = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="ipc-html-content ipc-html-content--base sc-9eebdf80-1 iUikZB"]')))

        if len(elements) > 0:
            elements = elements[0].text
        else:
            print("No elements found")
            elements = np.nan

    except Exception as e:
        print("Error occurred:", str(e))
        elements = ''

    finally:
        driver.quit()
    reply = session.get(complete_url, headers=headers)
    soup1 = BeautifulSoup(reply.text, 'html.parser')
    box = soup1.find_all('div', class_='sc-e226b0e3-10 jcOwsU')
    for things in box:
        genres = things.find_all('a', class_='ipc-chip ipc-chip--on-baseAlt')
        genres = [link.span.text for link in genres]
        director = things.find('a',
                               class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')
        director_href = director['href']
        director = director.text.strip()
        director_id_match = re.search(r'/name/nm(\d+)/', director_href)
        director_id = [director_id_match.group(1)]
        writers = things.find_all('ul',
                                  class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt')[
            1]
        writer_ids = []
        for writer in writers:
            writer_href = writer.a['href']
            writer_id_match = re.search(r'/name/nm(\d+)/', writer_href)
            writer_id = writer_id_match.group(1)
            writer_ids.append(writer_id)
        writers = [writer.a.text for writer in writers]
        stars = things.find_all('ul',
                                class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt')[
            2]
        star_ids = []
        for star in stars:
            star_href = star.a['href']
            star_id_match = re.search(r'/name/nm(\d+)/', star_href)
            star_id = star_id_match.group(1)
            star_ids.append(star_id)
        stars = [star.a.text for star in stars]
        gross_us_canada = soup1.find_all('li', {'data-testid': 'title-boxoffice-grossdomestic'})
        if gross_us_canada:
            gross_us_canada = gross_us_canada[0].find('span',
                                                      class_='ipc-metadata-list-item__list-content-item').text.strip()
        else:
            gross_us_canada = np.nan
    if not box:
        box = soup1.find_all('div', class_='sc-e226b0e3-10 bALQos')
        for things in box:
            genres = things.find_all('a', class_='ipc-chip ipc-chip--on-baseAlt')
            genres = [link.span.text for link in genres]
            director = things.find('a',
                                   class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')
            director_href = director['href']
            director = director.text.strip()
            director_id_match = re.search(r'/name/nm(\d+)/', director_href)
            director_id = [director_id_match.group(1)]
            writers = things.find_all('ul',
                                      class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt')[
                1]
            writer_ids = []
            for writer in writers:
                writer_href = writer.a['href']
                writer_id_match = re.search(r'/name/nm(\d+)/', writer_href)
                writer_id = writer_id_match.group(1)
                writer_ids.append(writer_id)
            writers = [writer.a.text for writer in writers]
            stars = things.find_all('ul',
                                    class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt')[
                2]
            star_ids = []
            for star in stars:
                star_href = star.a['href']
                star_id_match = re.search(r'/name/nm(\d+)/', star_href)
                star_id = star_id_match.group(1)
                star_ids.append(star_id)
            stars = [star.a.text for star in stars]
            gross_us_canada = soup1.find_all('li', {'data-testid': 'title-boxoffice-grossdomestic'})
            if gross_us_canada:
                gross_us_canada = gross_us_canada[0].find('span',
                                                          class_='ipc-metadata-list-item__list-content-item').text.strip()
            else:
                gross_us_canada = np.nan
    series_data.append(
        (
            movie_id, series_name, years, parental_guide, total_minutes, genres, director_id, director, writer_ids,
            writers, star_ids, stars, gross_us_canada, elements))
    # if count <= 0:
    #     break

df = pd.DataFrame(series_data,
                  columns=['movie_id', 'title', 'year', 'parental_guide', 'runtime', 'genre', 'director_id', 'director',
                           'writer_ids', 'writer', 'star_ids', 'star',
                           'gross_us_canada', 'storyline'])
end_time = time.time()
execution_time = end_time - start_time
execution_time_minutes = execution_time / 60
print(f"Execution time: {execution_time_minutes} minutes")
df.to_csv('top_250_movies_test.csv', index=False, encoding='utf-8-sig')
