# Author: Chenchuhui Hu
# Purpose: Create metadata.csv that contains metadata for each audio file.
# Each metadata includes speaker id, file path, file name, sentence, gender, age group, status.

import csv
import openpyxl
import os

class AudioMetadataProcessor:
    def __init__(self, read_file, result_file, audio_base_dir, text_base_dir):
        self.read_file = read_file
        self.result_file = result_file
        self.audio_base_dir = audio_base_dir
        self.text_base_dir = text_base_dir
        self.headers = ['speaker_id', 'filepath', 'filename', 'sentence', 'gender', 'age_group', 'status']

    @staticmethod
    def get_txt_content(txt_path):
        with open(txt_path, 'r') as txt_file:
            return txt_file.read()
    
    @staticmethod
    def compare_files_in_pairs(f1, f2):
        if os.path.splitext(f1)[0] == os.path.splitext(f2)[0]:
            return True
        else:
            return False

    def process_files(self):
        workbook = openpyxl.load_workbook(self.read_file)
        sheet = workbook.active

        with open(self.result_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.headers)

            for row in sheet.iter_rows(min_row=2):
                audio_chapter_name = row[0].value
                gender = row[1].value
                age_group = row[2].value
                audio_chapter = row[3].value
                speaker_id = row[4].value

                audio_folders = sorted([f for f in os.listdir(self.audio_base_dir) if f.startswith(audio_chapter)])
                text_folders = sorted([f for f in os.listdir(self.text_base_dir) if f.startswith(audio_chapter)])

                if len(audio_folders) == len(text_folders):
                    for i in range(len(audio_folders)):
                        if audio_folders[i] == text_folders[i]:
                            audio_folder_path = os.path.join(self.audio_base_dir, audio_folders[i])
                            text_folder_path = os.path.join(self.text_base_dir, text_folders[i])
                            audio_files = sorted(os.listdir(audio_folder_path))
                            text_files = sorted(os.listdir(text_folder_path))

                            if len(audio_files) == len(text_files):
                                for j in range(len(text_files)):
                                    if self.compare_files_in_pairs(audio_files[j], text_files[j]):
                                        audio_file_path = os.path.join(audio_folder_path, audio_files[j])
                                        audio_file_name = audio_files[j]
                                        text_file_path = os.path.join(text_folder_path, text_files[j])
                                        sentence = self.get_txt_content(text_file_path)
                                        write_content = [speaker_id, audio_file_path, audio_file_name, sentence, gender, age_group, '']
                                        writer.writerow(write_content)


# The main execution
if __name__ == "__main__" :
    readFile = 'Audio_Types.xlsx'
    resultFile = 'metadata/metadata.csv'
    bible_audio_base_directory = 'audio_data'
    bible_text_base_directory = 'text_data'
    os.makedirs('metadata', exist_ok=True)

    processor = AudioMetadataProcessor(readFile, resultFile, bible_audio_base_directory, bible_text_base_directory)
    processor.process_files()

