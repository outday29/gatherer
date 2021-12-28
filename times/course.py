from constant import *
from util.file import clean_name

from itertools import count
import time
import os

from bs4 import BeautifulSoup

def gather_material(session, main_page_soup):
    course_list = main_page_soup.find("li", {"aria-labelledby": "label_2_11"}).find("ul")
    for i in course_list.find_all("li"):
        course_info = i.find("a")
        if course_info.text == "Moodle101(S)":
            continue
        else:
            course_name = clean_name(course_info['title'])
            course_url = course_info['href']
            print("Now downloading subject: ", course_name)
            download_course_material(session, course_name, course_url)


def download_course_material(session, course, url):
    response = session.get(url)
    assert response.status_code == 200
    response_soup = BeautifulSoup(response.text, 'lxml')
    material_list = response_soup.find(id="content")
    for i in count(start=0):
        section = material_list.find(id=f"section-{i}")

        if section is None:
            break

        section_title = clean_name(section.find("span", {"class": "hidden sectionname"}).text)
        print("Now downloading section: ", section_title)
        print(COURSE_MATERIAL_PATH / course / section_title)
        (COURSE_MATERIAL_PATH / course / section_title).mkdir(parents=True, exist_ok=True)

        for resource in section.select("li.activity.resource"):
            material_url = resource.find("a")['href']
            material_name = clean_name(resource.find("a").find("span").contents[0])
            material_extension = get_material_extension(resource.select("img.activityicon")[0], material_name)

            if os.path.exists(COURSE_MATERIAL_PATH / course / section_title / (material_name + material_extension)):
                print(f"File {material_name + material_extension} already exists.")
                continue

            else:
                print(f"Now downloading {material_name + material_extension}")
                material_content = session.get(material_url)
                
                assert material_content.status_code == 200

                with open(COURSE_MATERIAL_PATH / course / section_title / (material_name + material_extension) , "wb") as f:
                    f.write(material_content.content)
                    print(f"Successfully wrote {material_name + material_extension}")
                    time.sleep(3)
                

def get_material_extension(img_html, material_name):
    file_type = img_html['src'].rsplit('/', 1)[-1]
    print("File type name is: ", file_type)
    if "spreadsheet" in file_type:
        return ".csv"
    
    elif "pdf" in file_type:
        return ".pdf"
    
    elif "document" in file_type:
        return ".docx"
    
    elif "text" in file_type:
        return ".txt"
    
    elif "powerpoint" in file_type:
        return ".ppt"
    
    elif "html" in file_type:
        return ".html"

    elif "unknown" in file_type:
        print(f"{material_name} has unknown file extension.")
        print("This file will be named with no file extension")
        return ""

    else:
        raise ValueError(f"File extension {file_type} not recognized")