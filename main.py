from scraper import *
import json

if __name__ == "__main__":
    e = product("https://www.ricardo.ch/de/a/specia-gaming-pc-core-i7-13th-32gb-1tb-rtx3060ti-wakue-*neu*-1279881060//")
    print(e)
    with open("result.json", "w", encoding="utf-8") as vb:  # Use UTF-8 encoding for proper handling of umlauts
        json.dump(e, vb, indent=4, ensure_ascii=False)  # ensure_ascii=False keeps special characters
