import sys
import requests

sys.path.insert(0, "D:\Personal_Project\automate\login")

from login.login import login_times
from times.deadline import get_deadlines, get_cached_deadlines
from times.course import gather_material

from bs4 import BeautifulSoup
# with requests.Session() as s:
#     main_page = login_times(s)
#     print(main_page.content)

with open("data/main_page.txt") as f:
    with requests.Session() as s:
        main_page = login_times(s)
        text = f.read()
        soup = BeautifulSoup(text, "lxml")
        gather_material(s, soup)
        