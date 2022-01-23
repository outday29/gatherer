import sys
import requests
import argparse

sys.path.insert(0, "D:\Personal_Project\automate\login")

from login.login import login_times
from times.deadline import gather_deadlines, get_cached_deadlines
from times.course import gather_material

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--course", 
                    help="Download course materials", 
                    action="store_true",
                    default=False)
parser.add_argument("-s", "--single",
                    help="Prompt before downloading course materials",
                    action="store_true",
                    default=False)
parser.add_argument("-d", "--deadlines",
                    help="Get deadlines details. Results are cached",
                    action="store_true",
                    default=False)
args = parser.parse_args()

with requests.Session() as s:
    main_page = login_times(s)
    main_page_soup = BeautifulSoup(main_page.content, "lxml")
    if args.course:
        gather_material(s, main_page_soup, verbose=args.single)
    
    if args.deadlines:
        gather_deadlines()