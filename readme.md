# Ricardo Web Crawler

This Python script provides a set of tools to crawl and extract data from the Ricardo.ch website. It includes functions to retrieve shop offers, ratings, and a continuous shop finder that explores related shops.

## Features

- **AmountOfOfferPages**: Determines the number of offer pages available for a specific shop.
- **ShopOffers**: Retrieves offers from a specific shop, with options to exclude offers without images and return only links.
- **ShopRatings**: Fetches ratings for a specific shop, with an option to return only the names of the raters.
- **ContinousShopFinder**: A generator that continuously finds and crawls related shops based on raters.

## Installation

To use this script, you need to have Python installed along with the following libraries:

```bash
pip install requests beautifulsoup4
```
## Usage

### AmountOfOfferPages | Get the amount of pages a shop/seller has
```
pages = AmountOfOfferPages("Senn24")
print(f"Number of offer pages: {pages}")
```

### ShopOffers 
```
offers = ShopOffers("Senn24", page=1, exclude_owi=True, links_only=False)
for offer in offers:
    print(offer)
```
### ShopRatings
```
ratings = ShopRatings("Senn24", names_only=False)
print(ratings)
```

### ContinousShopFinder
```
csf = Crawler().ContinousShopFinder("Senn24")
for chunk in csf:
    print(f"Found: {chunk['users']}")
    print(f"Shops Total: {chunk['total_shops']}")
    print(f"Shops Crawled: {chunk['total_shops_c']}")
    print(f"Not yet crawled: {chunk['not_crawled']}")
    print(f"Progress: {chunk['total_shops_c'] / chunk['total_shops'] * 100:.2f}%")
    print("\n\n")
```
## Parameters

- **exclude_owi**: Exclude any offers without images.
- **name**: Name of the shop/seller.
- **page**: Page number to retrieve offers from.
- **links_only**: Return only the links of the offers.
- **names_only**: Return only the names of the raters.

## File Examples
- **users.json**: Contain an example list of users
- **offers.json**: Contain an example list of offers
