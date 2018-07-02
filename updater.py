from bs4 import BeautifulSoup
import requests
import json


def main():
    write_players()
    write_coaches()
    write_news()


# Pulling player data (name, number, picture, bio, position, year, height, weight, previous school) and writing to json
def write_players():
    players = []
    page = requests.get('http://www.vcuathletics.com/sports/mbkb/2017-18/roster').content
    soup = BeautifulSoup(page, 'lxml')
    player_entry = soup.find('div', {'class': 'roster'}).find_all('tr')

    for player in player_entry[1:len(player_entry)]:
        info = player.find('a')['aria-label'].split(':')
        bio = player.find('a')['href']
        picture = player.find('img')['data-src']
        name = info[0]
        number = info[1].split(' ')[3]
        other_data = player.find_all('td')
        position = other_data[1].text.replace(' ', '').replace('\t', '').replace('\n', '').replace('Pos.:', '')
        year = other_data[2].text.replace(' ', '').replace('\t', '').replace('\n', '').replace('Cl.:', '')
        height = other_data[3].text.replace(' ', '').replace('\t', '').replace('\n', '').replace('Ht.:', '')
        weight = other_data[4].text.replace(' ', '').replace('\t', '').replace('\n', '').replace('Wt.:', '')
        prev_school = other_data[5].text.replace(' ', '').replace('\t', '').replace('\n', '')\
            .replace('Hometown/PreviousSchool:', '')
        players.append(dict([('name', name), ('number', number), ('bio', bio), ('picture', picture),
                             ('position', position), ('year', year), ('height', height), ('weight', weight),
                             ('prevSchool', prev_school)]))

    with open('VCU_Players.json', 'w') as outfile:
        json.dump(players, outfile)


# Pulling coach data (name, picture, bio) and writing to json
def write_coaches():
    coaches_data = []
    page = requests.get('http://www.vcuathletics.com/sports/mbkb/coaches/index').content
    soup = BeautifulSoup(page, 'lxml')
    coach_data = soup.find('div', {'class': 'coach-bios'}).find_all('div', {'class': 'row-fluid'})

    for entry in coach_data:
        coaches = entry.find_all('div', {'class', 'span6'})
        for coach in coaches:
            name = coach.find('span', {'class': 'name'}).text
            picture = coach.find('img', {'class': 'thumb'})['src']
            bio = coach.find('a')['href']
            coaches_data.append(dict([('name', name), ('picture', picture), ('bio', bio)]))

    with open('VCU_Coaches.json', 'w') as outfile:
        json.dump(coaches_data, outfile)


# Pulling news (title, date, link, picture) and writing to json
def write_news():
    news = []
    page = requests.get('http://vcuathletics.com/sports/mbkb/2017-18/news').content
    soup = BeautifulSoup(page, 'lxml')
    articles = soup.find('div', {'class': 'stories'}).find('ul', {'class': 'clearfix'}).find_all('li', {'class': 'story'})

    for article in articles:
        title = article.find('span', {'class': 'title'}).text
        date = article.find('div', {'class': 'date'}).text
        link = article.find('a', {'class': 'title-box'})['href']
        picture = article.find('img')['data-src']
        news.append(dict([('title', title), ('date', date), ('link', link), ('picture', picture)]))

    with open('VCU_News.json', 'w') as outfile:
        json.dump(news, outfile)


if __name__ == '__main__':
    main()
