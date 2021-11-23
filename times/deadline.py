from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd

from constant import *
from util import display, cache

def get_deadlines(session, main_page_soup):
    deadline_data = []
    target = main_page_soup.find_all("div", {"class": "event"})
    for i in target:
        # Don't take the AP classes
        try:
            if i.find("span").find("i") is not None and \
            i.find("span").find("i")['title'] == "Course event":
                continue    
        except KeyError:
            pass
        
        entry = {
            "Title": i.find("a").text,
            "Subject": extract_deadline_subject(session, i.find("a")['href']),
            "Date": i.find("div").text.replace(",", "")
        }

        display.display_dict(entry)
        deadline_data.append(entry)
    
    cache.cache_dict(deadline_data, "deadlines.csv")

def get_cached_deadlines():
    if (Path(DATA_PATH) / "deadlines.csv").is_file():
        df = pd.read_csv(Path(DATA_PATH) / 'deadlines.csv')
        display.display_pandas_rbr(df)
    else:
        raise FileNotFoundError()

def extract_deadline_subject(session, url):
    response = session.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.text, 'lxml')
    return soup.find("h1").text
