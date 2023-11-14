import os
from praatio import tgio
from pydub import AudioSegment

def checkDataValidity(tf, af):
        if len(tf) != len(af):
                return False
        for i in range(len(tf)):
                if os.path.splitext(tf[i])[0] != os.path.splitext(af[i])[0]:
                        return False
        
        return True

audio_base_dir = "Bible_Split_Corp_audio" # Path where we will categorize and store chopped audio
text_base_dir = "Bible_Split_Corp_text" # Path where we will categorize and store chopped text
textgrid_files_dir_path = 'BibleResultTextGrid' # Path where textgrid we read from
audio_files_dir_path = 'Icelandic_isl_ICE_NT_Non-Drama_Converted' # Path where audio we read from 

if not os.path.exists(audio_base_dir):
        os.makedirs(audio_base_dir)
if not os.path.exists(text_base_dir):
        os.makedirs(text_base_dir)

# List and sort all TextGrid files
textgrid_files = sorted([f for f in os.listdir(textgrid_files_dir_path) if f.endswith('.TextGrid')])

# List and sort all WAV files
audio_files = sorted([f for f in os.listdir(audio_files_dir_path) if f.endswith('.wav')])

if not checkDataValidity(textgrid_files, audio_files):
       print("Data is not in pairs. Invalid Data")
else:
       for tg_filename, wav_filename in zip(textgrid_files, audio_files):
        # Extract the base filename without extension
        tg_basename = os.path.splitext(tg_filename)[0]
        wav_basename = os.path.splitext(wav_filename)[0]

        audio_dir_path = os.path.join(audio_base_dir, tg_basename)
        text_dir_path = os.path.join(text_base_dir, tg_basename)
        os.makedirs(audio_dir_path, exist_ok=True)
        os.makedirs(text_dir_path, exist_ok=True)
        
        # Get textgrid path and wav path ready to read
        tg_path = os.path.join(textgrid_files_dir_path, tg_filename)
        wav_path = os.path.join(audio_files_dir_path, wav_filename)
        
        tg = tgio.openTextgrid(tg_path)
        seg = AudioSegment.from_wav(wav_path)
        
        tier = tg.tierNameList[0]  # Get first tier name
        EL = tg.tierDict[tier].entryList  # get all the entries of your tier
        
        utt = ""
        begin = -1
        end = 0
        cpt = 0
        
        for i, tg_part in enumerate(EL):
            utt += tg_part[2] + " "
            if begin == -1:
                begin = tg_part[0]
            if i+1 == len(EL) or tg_part[1] != EL[i+1][0]:
                if i+1 == len(EL) or tg_part[1] - begin >= 5 or EL[i+1][0] - tg_part[1] >= 0.6:
                    end = tg_part[1]
                    cpt += 1
                    # Chop the audio given begin and end time
                    sub_seg = seg[begin*1000: end*1000]
                    # Export to the designated path
                    sub_seg.export(os.path.join(audio_dir_path, f'{tg_basename}_{cpt:02}.wav'), format="wav")
                    # Write back to the designated file
                    with open(os.path.join(text_dir_path, f'{tg_basename}_{cpt:02}.text'), mode='w') as tfile:
                        tfile.write(utt.strip().lower())
                    # Reset every variable
                    utt = ""
                    begin = -1
                    end = 0