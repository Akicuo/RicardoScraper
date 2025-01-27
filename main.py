from scraper import *

if __name__ == "__main__":
    e = product("https://www.ricardo.ch/de/a/imac-(retina-5k-27-zoll-ende-2015)-1278553784/")
    print(e)
    with open("result.json", "w") as vb:
        json.dump(e, vb, indent=4)