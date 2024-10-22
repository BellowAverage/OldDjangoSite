import random
import time
import requests
import parsel
import pandas as pd
import fake_useragent


def topsellers():
    url = f'https://store.steampowered.com/contenthub/querypaginated/specials/TopSellers/render/?query=&start=1&count=15&cc=TW&l=schinese&v=4&tag='
    
    user_agent = fake_useragent.UserAgent()
    headers = {
        'User-Agent': user_agent.random
    }
    
    response = requests.get(url=url, headers=headers)

    html_data = response.json()['results_html']

    selector = parsel.Selector(html_data)
    data = []

    lis = selector.css('a.tab_item')
    for li in lis:
        href = li.css('::attr(href)').get()
        title = li.css('.tab_item_name::text').get()
        tag_list = li.css('.tab_item_top_tags .top_tag::text').getall()
        tag = ''.join(tag_list)
        price = li.css('.discount_original_price::text').get()
        price_1 = li.css('.tab_item_discount .discount_final_price::text').get()
        discount = li.css('.tab_item_discount .discount_pct::text').get()
        data.append([title, tag, price, price_1, discount, href])

    df = pd.DataFrame(data, columns=['Title', 'Tag', 'Original Price', 'Final Price', 'Discount', 'URL'])
    return df

def offline_topsellers():
    df = pd.read_excel("media/NegativeComments.xlsx", usecols=["玩家pid","累计充值rmb"], nrows=10)
    return df