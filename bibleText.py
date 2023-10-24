import os
from time import sleep
import requests
import json
from bs4 import BeautifulSoup

bible_tags: dict = {
    "MAT": 28,
    "MRK": 16,
    "LUK": 24,
    "JHN": 21,
    "ACT": 28,
    "ROM": 16,
    "1CO": 16,
    "2CO": 13,
    "GAL": 6,
    "EPH": 6,
    "PHP": 4,
    "COL": 4,
    "1TH": 5,
    "2TH": 3,
    "1TI": 6,
    "2TI": 4,
    "TIT": 3,
    "PHM": 1,
    "HEB": 13,
    "JAS": 5,
    "1PE": 5,
    "2PE": 3,
    "1JN": 5,
    "2JN": 1,
    "3JN": 1,
    "JUD": 1,
    "REV": 22,
}

def get_chapter_text(tag: str, page: int) -> list:
    response = requests.get(f'https://live.bible.is/bible/ISLICE/{tag}/{str(page)}')
    html_content: str = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
    if script_tag:
        # Extract the content of the script tag
        script_content = script_tag.string
        script_dic : dict = json.loads(script_content)
        text_list : list = script_dic["props"]["pageProps"]["chapterText"]
        return text_list
    else:
        raise ValueError("Script tag with id '__NEXT_DATA__' not found!")


# Give the file object for I/O. Give write permission
def get_file_object(filename: str):
    return open(filename, 'w+')

def extract_text():
    chapter = 0
    # for each chapter
    for key, value in bible_tags.items():
        chapter += 1
        # for each page
        for i in range(1, value+1):
            try:
                text_list = None
                while (not text_list):
                    try:
                        text_list = get_chapter_text(key, i)
                    except KeyError:
                        sleep(2)
                print("Chapter: " + str(chapter) + " Page: " + str(i))
                inputfile = get_file_object(f'{dir_path}/B{chapter:02}_{i:02}.txt')
                line = 0
            except ValueError as err:
                # Nothing in the list, print something unusual and terminate the program
                print(err)
                return
            for ele in text_list:
                line += 1
                inputfile.write(str(line) + '. ' + ele["verse_text"] + "\n")
            inputfile.close()

# The main execution of scraping
if __name__ == "__main__" :
    dir_path = 'Icelandic_isl_Bible_Text'

    # Check if the directory exists, and if not, create it
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    extract_text()
    
                