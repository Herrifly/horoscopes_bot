import requests
from bs4 import BeautifulSoup
import sqlite3
import time

def search_info():
    conn = sqlite3.connect('db/database_zodiak.db', check_same_thread=False)
    cursor = conn.cursor()

    list_zodiak = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra',
                   'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
    list_dates = ['yesterday', 'today', 'tomorrow', 'week', 'month', 'year']

    for i in list_zodiak:
        for j in list_dates:
            responce = requests.get(url="https://horo.mail.ru/prediction/" + i + '/' + j + '/')
            while responce.status_code != 200:
                time.sleep(0.5)
                responce = requests.get(url="https://horo.mail.ru/prediction/" + i + '/' + j + '/')
            soup = BeautifulSoup(responce.text, 'lxml')
            info = soup.find_all('p')
            text_zodiak = info[0].text + '\n' + info[1].text
            cursor.execute(f'UPDATE "horoscopes"  SET {j} = ? WHERE "zodiak" = ? ',
                           (text_zodiak, i))
            conn.commit()

search_info()
# schedule.every().day.at("00:00").do(search_info)
#
#
# while True:
#     schedule.run_pending()