from bs4 import BeautifulSoup
import random
import requests
import re,json
from playwright.sync_api import sync_playwright
url = "https://www.ricardo.ch/"
def remove_duplicates(word_list):
    unique_words = list(set(word_list))
    return unique_words


def product(url: str):
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True, channel="chrome")
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/115.0.0.0"
        )
        fo = None
        co = None
        all_images = []
        finished = False
        page = context.new_page()
        page.goto(url)
        page.wait_for_selector('img')
        page.wait_for_load_state("load")
        soup = BeautifulSoup(page.content(), 'html.parser')

        while finished == False:
            img_src = page.locator('img').first.get_attribute('src')
            page.wait_for_timeout(100)
            co = img_src
            all_images.append(img_src)

            if fo == None:
                fo = img_src
            else:
                
                if co == fo:
                    finished = True
                    break
            page.wait_for_timeout(100)
            try:  
                page.click('button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeLarge.mui-1iqj9qi', timeout=100)
            except:
                break
           

        type = None
        pricing = []
        instant_buy = False
        bid_button = soup.find("button", {"id": "btnPlaceBidCTA"}) # page.query_selector("#btnPlaceBidCTA")
        price1 = soup.find("div", class_="MuiBox-root mui-xf2v4p")
        price2 = soup.find("p", class_="MuiBox-root mui-xf2v4p")
        if bid_button:
            type = "auction"
            pricing.append({"starting_price": price2.text})
            if price1:
                pricing.append({"buy_now_price": price1.text})
                instant_buy = True
            else:
                instant_buy = False
        else:
            type = "sale"
            pricing.append({"buy_now_price": price2.text})
        title = soup.find("h1", class_="MuiBox-root mui-1mg8wvf").text
        description = soup.find("div", class_="MuiBox-root mui-wvzkyj").text# page.query_selector("div.MuiBox-root.mui-wvzkyj").text_content

        abholung = soup.find("button", class_="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone MuiLink-button mui-1ogmf2r").text.split(" ")

        browser.close()
        
        return {
            "type": type,
            "images": all_images,
            "title": title,
            "uncut_url": url,
            "cut_url": url,
            "pricing": pricing,
            "description":description,
            "instant_buy": instant_buy,
            "pickup": {
                "location": abholung[1],
                "plz": abholung[0]
            }

        }


e = product("https://www.ricardo.ch/de/a/imac-(retina-5k-27-zoll-ende-2015)-1278553784/")
print(e)
with open("result.json", "w") as vb:
    json.dump(e, vb, indent=4)



def AmountOfOfferPages(name: str) -> list:
    global url
    pages = []
    page = 1
    while True:
        response = requests.get(url=url+f"de/shop/{name}/offers/?page={page}")
        if response.status_code != 200:
            break
        pages.append(page)
        page += 1
    return pages

def ShopOffers(name:str, page:int=1, exclude_owi:bool=False, links_only:bool=False):
    global url
    v_results = []

    if page < 1:
        raise ValueError("page parameter has to be 1 or over")
    
    html = requests.get(url=url+F"de/shop/{name}/offers/?page={str(page)}")
    if html.status_code == 404:
        return ["None found"]
    s = BeautifulSoup(html.content, 'html.parser')
    results = s.find_all('a', class_="style_link__ewXtk")
    if links_only:
        for result in results:
            v_results.append(result.get('href'))
    else:
        for result in results:
            text_elements = result.stripped_strings
            img_tag = result.find('img', class_="MuiBox-root mui-htynqc")
            img = img_tag.get("src") if img_tag else None  # Handle None case
            if exclude_owi and img is None:
                continue
            separated_texts = "|".join(text_elements).split("|")
            try:
                    if len(separated_texts) == 3:
                        v_results.append({  "shop": name,
                                            "image": img,
                                            "title": separated_texts[0],
                                            "price": float(str(separated_texts[2]).replace("'", "")),
                                            "link": "https://www.ricardo.ch"+result.get('href')})
                    elif len(separated_texts) == 4:
                        v_results.append({  "shop": name,
                                            "image": img,
                                            "title": separated_texts[0],
                                            "extra": separated_texts[1],
                                            "price": float(str(separated_texts[2]).replace("'", "")),
                                            "link": "https://www.ricardo.ch"+result.get('href')})
            except:
                continue

    return v_results


def ShopRatings(name:str, names_only=False):
    global url
    html = requests.get(url=url+F"de/shop/{name}/ratings/")
    s = BeautifulSoup(html.content, 'html.parser')
    results = s.find_all('div', class_="MuiBox-root mui-x1sij0")
    v_results=None
    if names_only:
        v_results = []
        for result in results:
            v_results.append("|".join(result.stripped_strings).split("|")[0])
            v_results = remove_duplicates(v_results)
        
    else:
        v_results = {"polarity": {}, "ratings": []}

        # get polartiy (positive neutral negative score)
        results_v2 = s.find_all('div', class_="mui-1qtkas9")
        for result in results_v2:
            separated_texts = "|".join(result.stripped_strings).split("|")
            v_results["polarity"][str(separated_texts[0].lower()+"e").replace("neutrale", "neutrals")] = int(separated_texts[1])



        # get ratings 
        for result in results:
            separated_texts = "|".join(result.stripped_strings).split("|")
            v_results["ratings"].append({"type": separated_texts[3].lower()+"e",
                              "user": separated_texts[0],
                              "article-nr": int(separated_texts[2].replace("Art.-Nr. ", "")),
                              "content": separated_texts[4]})
    return v_results




class Crawler:
    def ContinousShopFinder(self, start_shop: str):
        current_shop = start_shop
        shops_found = set()
        shops_crawled = set()
        while True:
            try:
                raters = ShopRatings(current_shop, True)
                shops_found.update(raters)
                shops_crawled.add(current_shop)

                not_yet_crawled = shops_found - shops_crawled
                if not_yet_crawled:
                    current_shop = random.choice(list(not_yet_crawled))

                chunk = {"users": raters,
                         "total_shops": len(shops_found),
                         "total_shops_c": len(shops_crawled),
                         "not_crawled": len(not_yet_crawled)
                         }    
                yield chunk 
            except Exception as e:
                print(f"An error occurred: {e}")
                break