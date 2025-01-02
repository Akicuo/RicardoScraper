from scraper import ShopOffers, ShopRatings, AmountOfOfferPages, Crawler
import json
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # For progress bar

MAX_SHOPS = 150

def get_offers(shop: str, page: int) -> list:
    """Fetch offers for a given shop and page."""
    return ShopOffers(shop, page, True, False)

def dump_data(data: dict, filepath: str):
    """Dump data to a JSON file."""
    with open(filepath, "w") as file_j:
        json.dump(data, file_j, indent=4)

def gather_users(start_user: str) -> list:
    """Gather users starting from a given user."""
    users = []
    shops = Crawler().ContinousShopFinder(start_shop=start_user)
    for result in shops:
        if len(users) >= MAX_SHOPS:
            break
        users += result["users"]
        print(f"Current Total: {len(users)}", end="\r")
    print(f"Gathered {len(users)} users")
    return users

def gather_offers(users: list) -> list:
    """Gather offers for a list of users using multi-threading."""
    offers = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for number, user in enumerate(users):
            pages = AmountOfOfferPages(name=user)
            for c_page in pages:
                futures.append(executor.submit(get_offers, user, c_page))
                print(f"[SUCCESS] | Page: {c_page} | {number} User: {user}")
        for future in tqdm(as_completed(futures), total=len(futures), desc="Fetching Offers"):
            try:
                offers += future.result()

            except Exception as e:
                print(f"Error fetching offers: {e}")
    return offers

def main():
    """Main function to orchestrate the data gathering process."""
    start_user = input("Who is the starting user?: ")
    
    if not ShopRatings(start_user, True):
        print("No ratings found for this user")
        return
    
    users = gather_users(start_user)
    dump_data({"users": users}, "users.json")
    
    offers = gather_offers(users)
    dump_data({"offers": offers}, "offers.json")

if __name__ == "__main__":
    main()