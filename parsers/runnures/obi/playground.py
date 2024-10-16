from parsers.runnures.obi.parser import *

service_log()
category_link = 'https://obi.ru/strojmaterialy'

current_page = 1
page_url = get_product_page_url(category_link, current_page)
response: Response | None = call_api(page_url)
if response:
    soup = BeautifulSoup(response.text, "html.parser")
    product_links = soup.select('#__next > main > div > div._24JVv._2lCzN > div.Ou71e > div._3yNpa > div > div > div > a')
    for product_link in product_links:
        print(product_link.get('href'))
