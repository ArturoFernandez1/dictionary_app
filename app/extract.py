from bs4 import BeautifulSoup
import requests
from typing import Dict

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chromium/99.0.4844.74 Safari/537.36'}
RAE_URL = "https://dle.rae.es"
SYNONYMS_URL = "https://www.sinonimosonline.com/"

def extract(data: str) -> Dict:

    d = dict()
    l = []
    r = requests.get(f"{RAE_URL}/{data}", headers=HEADERS)
    s = requests.get(f"{SYNONYMS_URL}/{data}", headers=HEADERS)

    rae = BeautifulSoup(r.text, "lxml")
    synonyms = BeautifulSoup(s.text, "lxml")
    try:
        d["etymology"] = BeautifulSoup(rae.find("p", class_="n2").text, "lxml").text
        d["definitions"] = [BeautifulSoup(definition.text, "lxml").text for definition in rae.find_all("p", class_="j")]
        d["synonyms"] = [BeautifulSoup(synonym.text, "lxml").text.replace(".Ejemplo", ". Ejemplo") for synonym in synonyms.find_all("p", class_="sinonimos")]
    except:
        return dict()    
    
    return d
