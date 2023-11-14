#!/bin/bash

mkdir -p converted_audio

# Loop through all .mp3 files in the current directory
for file in raw_audio/*.mp3; do
  # Use basename to get the file name without the extension
  base_name=$(basename "$file" .mp3)
  
  # Construct the output file path with the new extension
  output="converted_audio/${base_name}.wav"
  
  # Check if the file name contains 'ISLICEN1DA'
  if [[ "$file" == *"ISLICEN1DA"* ]]; then
    # Run ffmpeg command for files containing 'ISLICEN1DA'
    ffmpeg -i "$file" -ar 16000 -ac 1 -ss 00:00:04 "$output"
  else
    # Run ffmpeg command for all other files
    ffmpeg -i "$file" -ar 16000 -ac 1 "$output"
  fi
done
