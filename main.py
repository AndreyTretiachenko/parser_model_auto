import requests
from bs4 import BeautifulSoup
import json

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

def getCommercial():
    r = requests.get('https://www.exist.ru/Catalog/Global/Commercial', headers=headers)

    with open('data/brand.html', 'w') as file:
        file.write(r.text)


def getDataBrand():
    with open('data/brand.html') as file:
        src = file.read()
        return src


def main():
    '''getCommercial()'''
    listBrand = []
    soup = BeautifulSoup(getDataBrand(), 'lxml')
    for a in  soup.find('div', {'id': 'bmVendorTypesC1'}).find_all('a', href=True):
        listBrand.append({
            'brand': a.text,
            'link': a['href'],
            'modelList': []
        })
    for brand in listBrand:
        r = requests.get('https://www.exist.ru/'+brand['link'], headers=headers)
        modelList = BeautifulSoup(r.text, 'lxml').find('div', {'id': 'models'}).find_all('div', class_="cell2")
        for model in modelList:
            m = model.find('div', class_="car-info car-info--catalogs").find('div', class_='car-info__car-name').text
            years = model.find('div', class_="car-info car-info--catalogs").find('div',
                                                                                                            class_='car-info__car-years').text
            if m or years:
                brand['modelList'].append({
                    'model': m,
                    'years':  years,
                })
    with open('cars.json', 'w') as file:
        file.write(json.dumps(listBrand))



if __name__ == "__main__":
    main()