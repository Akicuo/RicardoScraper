import requests 
from bs4 import BeautifulSoup
import random
url = "https://www.ricardo.ch/"

def remove_duplicates(word_list):
    unique_words = list(set(word_list))
    return unique_words

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

                chunk = {"sf": shops_found,
                         "users": raters,
                         "total_shops": len(shops_found),
                         "total_shops_c": len(shops_crawled),
                         "not_crawled": len(not_yet_crawled)
                         }    
                yield chunk 
            except Exception as e:
                print(f"An error occurred: {e}")
                break
