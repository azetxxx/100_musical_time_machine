from bs4 import BeautifulSoup
import datetime as dt
import requests

# Constants
BASE_URL = 'https://www.billboard.com/charts/hot-100/'

today = dt.date.today()

# Function to validate date formate
def is_date_format_valid(date_input):
    try:
        dt_input_obj = dt.datetime.strptime(date_input, "%Y-%m-%d")
        return dt_input_obj.date() <= dt.date.today()
    except ValueError:
        return False


def get_valid_date():
    while True:
        picked_date = input("📅 Pick a date in the past for time traveling! \
            \nHint: Use the following format (YYYY-MM-DD) ➡️ ")
        if is_date_format_valid(picked_date):
            return picked_date
        else:
            print("\n❌ Invalid date format or future date. Try again! \n")


def main():
    picked_date = get_valid_date()
    print(f"\n✅ Picked date: {picked_date}\n")

    response = requests.get(BASE_URL + picked_date)
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        return

    chart_page = response.text
    soup = BeautifulSoup(chart_page, 'html.parser')

    # song_titles = soup.select(selector='div.o-chart-results-list-row-container ul li:nth-of-type(4) ul li:first-of-type span')
    song_titles = soup.select(selector='li ul li h3')

    for song in song_titles:
        for string in song.stripped_strings:
            print(string)


if __name__ == '__main__':
    main()
