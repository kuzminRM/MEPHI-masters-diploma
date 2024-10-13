from bs4 import BeautifulSoup

category_links = {
    'Стройматериалы': 'https://obi.ru/strojmaterialy',
    'Инструмент': 'https://obi.ru/instrument',
    'Сантехника': 'https://obi.ru/santehnika',
    'Плитка': 'https://obi.ru/plitka',
    'Крепеж и фурнитура': 'https://obi.ru/krepezh-i-furnitura',
    'Напольные покрытия': 'https://obi.ru/napolnye-pokrytija',
    'Лакокрасочные материалы': 'https://obi.ru/lakokrasochnye-materialy',
    'Столярные изделия': 'https://obi.ru/stoljarnye-izdelija',
    'Сад и досуг': 'https://obi.ru/sad-i-dosug',
    'Хозяйственные товары': 'https://obi.ru/hozjajstvennye-tovary',
    'Хранение и порядок': 'https://obi.ru/hranenie-i-porjadok',
    'Декор': 'https://obi.ru/dekor',
    'Освещение': 'https://obi.ru/osveschenie',
    'Климат и отопление': 'https://obi.ru/klimat-i-otoplenie',
    'Кухни': 'https://obi.ru/kuhni',
    'Электрика': 'https://obi.ru/jelektrika',
    'Инженерные системы': 'https://obi.ru/inzhenernye-sistemy',
    'Окна и двери': 'https://obi.ru/okna-i-dveri',
    'Автотовары': 'https://obi.ru/avtotovary',
}


def get_top_categories_url():
    with open("./data/catalog.html", "r") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    links = soup.find_all('a')
    return {link.text: f"https://obi.ru{link.get('href')}" for link in links}


if __name__ == '__main__':
    print(get_top_categories_url())
