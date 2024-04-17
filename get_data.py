import csv
from datetime import datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup


class WeatherMaker:
    MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
              "october", "november", "december"]
    MONTHS_RU = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
                 'октября', 'ноября', 'декабря']

    def __init__(self):
        self.weather_report = []
        self.pages_weather_report = [["date", "temp"]]
        self.html = None
        self.path = Path('data.csv')
        self.url = 'https://yandex.ru/pogoda/month/{self.MONTHS[month]}?lat=56.829472&lon=60.532538&via=ms'

    def get_html(self, url):
        self.html = requests.get(url)

    def get_content(self):
        soup = BeautifulSoup(self.html.text, "html.parser")
        items = soup.find_all("div", class_="climate-calendar-day__detailed-container-center")
        items.encoding = "utf-8"
        for item in items:
            date = item.find("h6", class_="climate-calendar-day__detailed-day").get_text().split(',')[0].split(" ")

            for i, val in enumerate(self.MONTHS_RU):
                if val in date:
                    date[1] = str(i + 1)
                    self.weather_report.append([
                        datetime.strptime(" ".join(date) + " " + str(datetime.now().year), '%d %m %Y').date().strftime(
                            "%d.%m.%Y"),
                        item.find("span", class_="temp__value temp__value_with-unit").get_text(),
                    ])

    def parse(self):

        date_from = datetime.now() - timedelta(days=5)
        date_to = datetime.now() + timedelta(days=25)
        self.get_html(f"{self.url}")
        if self.html.status_code == 200:
            print("All Ok!")
            self.get_content()
            for month in range(date_from.month - 1, date_to.month):

                for elem in self.weather_report:
                    if elem not in self.pages_weather_report:
                        if date_from <= datetime.strptime(elem[0], "%d.%m.%Y") <= date_to:
                            self.pages_weather_report.append(elem)

            if self.path.is_file():
                with open(self.path, 'a', encoding="utf-8", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows([self.pages_weather_report[-1]])
            else:
                with open(self.path, 'a', encoding="utf-8", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(self.pages_weather_report)

        else:
            print("Error")

        return self.pages_weather_report


weather = WeatherMaker().parse()
