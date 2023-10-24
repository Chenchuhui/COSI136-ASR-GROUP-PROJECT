import os
from time import sleep
import requests
import json
from bs4 import BeautifulSoup

# Define a dictionary of Bible book tags and their respective chapter count
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

# Function to retrieve the text content of a specific chapter of a Bible book
def get_chapter_text(tag: str, page: int) -> list:
    # Make a request to the Bible API for the given book tag and chapter page
    response = requests.get(f'https://live.bible.is/bible/ISLICE/{tag}/{str(page)}')
    html_content: str = response.text
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find the script tag with a specific id
    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

    if script_tag:
        # Extract and parse the JSON content of the script tag
        script_content = script_tag.string
        script_dic : dict = json.loads(script_content)
        # Extract the chapter text from the parsed dictionary
        text_list : list = script_dic["props"]["pageProps"]["chapterText"]
        return text_list
    else:
        raise ValueError("Script tag with id '__NEXT_DATA__' not found!")


# Function to get a file object for reading and writing
def get_file_object(filename: str):
    return open(filename, 'w+')

# Main function to extract text content from the Bible
def extract_text():
    chapter = 0
     # Iterate over chapter count
    for key, value in bible_tags.items():
        chapter += 1
        # Iterate over each page of the current Bible book
        for i in range(1, value+1):
            try:
                text_list = None
                retry_count = 0
                max_retries = 5
                # Keep trying to fetch the chapter text until successful
                while not text_list and retry_count < max_retries:
                    try:
                        text_list = get_chapter_text(key, i)
                    except KeyError:
                        retry_count += 1
                        sleep(2) # Pause for 2 seconds and retry
                if retry_count == max_retries:
                    raise ValueError(f"Reached max retries for {key} chapter {i}")
                print("Chapter: " + str(chapter) + " Page: " + str(i))
                # Get the file object for the current chapter
                inputfile = get_file_object(f'{dir_path}/B{chapter:02}_{i:02}.txt')
                line = 0
            except ValueError as err:
                # Handle any errors during the extraction process                
                print(err)
                return
            # Write each verse to the file
            for ele in text_list:
                line += 1
                inputfile.write(str(line) + '. ' + ele["verse_text"] + "\n")
            inputfile.close()

# The main execution
if __name__ == "__main__" :
    dir_path = 'Icelandic_isl_Bible_Text'
    # Check if the directory exists, and if not, create it
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    extract_text()
    
                