from constant import *
from util.file import clean_name

from itertools import count
import time
import os
import zipfile
import io
import logging

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG, filename="log.txt", filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

def gather_material(session, main_page_soup, verbose):
    course_list = main_page_soup.find("li", {"aria-labelledby": "label_2_11"}).find("ul")
    for i in course_list.find_all("li"):
        course_info = i.find("a")
        if course_info.text == "Moodle101(S)":
            continue
        else:
            course_name = clean_name(course_info['title'])
            course_url = course_info['href']
            if verbose:
                logging.info(f"Download {course_name}? (y/n): ")
                user_input = input()
                logging.debug(f"User entered {user_input}.")
                if user_input.lower() not in ["y", "yes", ""]:
                    logging.debug(f"Skipping f{course_name}.")
                    continue
            logging.info(f"Now downloading subject {course_name}")
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
        file_path = COURSE_MATERIAL_PATH / course / section_title
        logging.debug(f"Setting file_path at {file_path}")
        logging.info(f"Now downloading section: {section_title}")

        (file_path).mkdir(parents=True, exist_ok=True)

        # Download non-folder resources
        for resource in section.select("li.activity.resource"):
            download_resource(session, resource, file_path)
        
        # Download folder resources
        for folder in section.select("li.activity.folder"):
            download_folder(session, folder, file_path)

def download_resource(session, resource, file_path):
    material_url = resource.find("a")['href']
    material_name = clean_name(resource.find("a").find("span").contents[0])
    material_extension = get_material_extension(resource.select("img.activityicon")[0], material_name)

    if os.path.exists(file_path / (material_name + material_extension)):
        logging.info(f"File {material_name + material_extension} already exists.")
        return

    else:
        logging.debug(f"Now downloading {material_name + material_extension}")
        material_content = session.get(material_url)
        
        assert material_content.status_code == 200

        with open(file_path / (material_name + material_extension) , "wb") as f:
            f.write(material_content.content)
            logging.info(f"Successfully wrote {material_name + material_extension}")
            time.sleep(3)

def download_folder(session, folder, file_path):
    folder_url = folder.find("a")['href']
    folder_response = session.get(folder_url)

    assert folder_response.status_code == 200

    folder_html = BeautifulSoup(folder_response.text, 'lxml')
    folder_title = clean_name(folder_html.find("h2").text)

    if (file_path / folder_title).is_dir():
        logging.info(f"Folder {file_path / folder_title} already exists")
        return

    else:
        download_form = folder_html.find("form", {"method": "post"})
        download_url = download_form["action"]
        data_payload = {
            "id": download_form.find("input", {"type": "hidden", "name": "id"})["value"],
            "sesskey": download_form.find("input", {"type": "hidden", "name": "sesskey"})["value"]
        }
        download_response = session.post(download_url, data=data_payload)

        assert download_response.status_code == 200

        folder_zip = download_response.content
        with io.BytesIO(folder_zip) as f:
            zip_ref = zipfile.ZipFile(f)
            zip_ref.extractall(file_path / folder_title)
        logging.info(f"Successfully wrote folder: {folder_title}")
        time.sleep(3)

def get_material_extension(img_html, material_name):
    file_type = img_html['src'].rsplit('/', 1)[-1]
    logging.debug(f"File type name is: {file_type}")
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
        logging.info(f"{material_name} has unknown file extension.")
        logging.info("This file will be named with no file extension")
        return ""

    else:
        raise ValueError(f"File extension {file_type} not recognized")