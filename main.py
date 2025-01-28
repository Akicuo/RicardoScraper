from scraper import *

if __name__ == "__main__":
    e = product("https://www.ricardo.ch/de/a/neuer-gaming-pc-i5-14600kf-2tb-ssd-32gb-ram-rtx-4060-1279671826/")
    print(e)
    with open("result.json", "w") as vb:
        json.dump(e, vb, indent=4)