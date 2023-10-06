import requests
from bs4 import BeautifulSoup
import pandas as pd


def request(url):
    data_url = url.split('/')[-1]
    respon = requests.get(url)
    with open("HTML/{}.html".format(data_url), "w+", encoding="utf-8") as f:
        f.write(respon.text)

def save_html():
    for x in range(1, 11):
        url = f'https://www.cnbcindonesia.com/tech/indeks/12/{x}'
        request(url)

def parser_data():
    data_artikel = []
    for x in range(1, 11):
        with open("HTML/{}.html".format(x), encoding="utf-8") as f:
            page = f.read()
            soup = BeautifulSoup(page, "html.parser")
            artikel = soup.find('ul', {'class':'list media_rows middle thumb terbaru gtm_indeks_feed'})
            all_artikel = artikel.find_all('article')
            for data in all_artikel:
                title = data.find('h2').text.strip()
                image = data.find('img').get('src')
                link = data.find('a').get('href')
                date = data.find('span', {'class':'date'}).text.strip().replace('Tech', '').replace('-', '').strip()
                label = data.find('span', {'class':'label'}).text.strip()
                list_data = {
                    'Title':title,
                    'Image':image,
                    'URL':link,
                    'Date':date,
                    'Label':label
                }
                data_artikel.append(list_data)
    return data_artikel

def save_data():
    datas = parser_data()
    df = pd.DataFrame(datas)
    print(df)
    df.to_csv('artikel.csv', index=False)




if __name__ == '__main__':
    save_html()
    save_data()
