import os
from praatio import tgio
from pydub import AudioSegment

class DataValidator:
    @staticmethod
    def check_data_validity(text_files, audio_files):
        if len(text_files) != len(audio_files):
            return False
        for tf, af in zip(text_files, audio_files):
            if os.path.splitext(tf)[0] != os.path.splitext(af)[0]:
                return False
        return True

class AudioTextProcessor:
    def __init__(self, audio_base_dir, text_base_dir, textgrid_dir, audio_dir):
        self.audio_base_dir = audio_base_dir
        self.text_base_dir = text_base_dir
        self.textgrid_dir = textgrid_dir
        self.audio_dir = audio_dir

    def process_files(self):
        textgrid_files = sorted([f for f in os.listdir(self.textgrid_dir) if f.endswith('.TextGrid')])
        audio_files = sorted([f for f in os.listdir(self.audio_dir) if f.endswith('.wav')])

        if not DataValidator.check_data_validity(textgrid_files, audio_files):
            print("Data is not in pairs. Invalid Data")
            return

        for tg_filename, wav_filename in zip(textgrid_files, audio_files):
            self.process_file_pair(tg_filename, wav_filename)

    def process_file_pair(self, tg_filename, wav_filename):
        tg_basename = os.path.splitext(tg_filename)[0]
        wav_basename = os.path.splitext(wav_filename)[0]

        audio_dir_path = os.path.join(self.audio_base_dir, tg_basename)
        text_dir_path = os.path.join(self.text_base_dir, tg_basename)
        os.makedirs(audio_dir_path, exist_ok=True)
        os.makedirs(text_dir_path, exist_ok=True)

        tg_path = os.path.join(self.textgrid_dir, tg_filename)
        wav_path = os.path.join(self.audio_dir, wav_filename)

        self.split_audio_text(tg_path, wav_path, audio_dir_path, text_dir_path, tg_basename)

    def split_audio_text(self, tg_path, wav_path, audio_dir_path, text_dir_path, tg_basename):
        tg = tgio.openTextgrid(tg_path)
        seg = AudioSegment.from_wav(wav_path)

        tier = tg.tierNameList[0]
        EL = tg.tierDict[tier].entryList

        utt, begin, end, cpt = "", -1, 0, 0

        for i, tg_part in enumerate(EL):
            utt += tg_part[2] + " "
            if begin == -1:
                begin = tg_part[0]
            if i+1 == len(EL) or tg_part[1] != EL[i+1][0]:
                if self.should_split(tg_basename, i, len(EL), tg_part, EL, begin):
                    end = tg_part[1]
                    cpt += 1
                    self.export_audio_text(seg, begin, end, audio_dir_path, text_dir_path, tg_basename, cpt, utt)
                    utt, begin, end = "", -1, 0

    def should_split(self, tg_basename, i, length, tg_part, EL, begin):
        if tg_basename.startswith('B'):
            return i+1 == length or tg_part[1] - begin >= 5 or EL[i+1][0] - tg_part[1] >= 0.6
        else:
            return i+1 == length or tg_part[1] - begin >= 5 or EL[i+1][0] - tg_part[1] >= 1

    def export_audio_text(self, seg, begin, end, audio_dir_path, text_dir_path, tg_basename, cpt, utt):
        sub_seg = seg[begin*1000: end*1000]
        sub_seg.export(os.path.join(audio_dir_path, f'{tg_basename}_{cpt:02}.wav'), format="wav")
        with open(os.path.join(text_dir_path, f'{tg_basename}_{cpt:02}.text'), mode='w') as tfile:
            tfile.write(utt.strip().lower())

# Usage
audio_base_dir = "audio_data"
text_base_dir = "text_data"
textgrid_files_dir_path = 'ResultTextGrid'
audio_files_dir_path = 'converted_audio'

processor = AudioTextProcessor(audio_base_dir, text_base_dir, textgrid_files_dir_path, audio_files_dir_path)
processor.process_files()
