#!/bin/bash

mkdir -p Icelandic_isl_ICE_NT_Non-Drama_Converted

# Loop through all .mp3 files in the current directory
for file in Icelandic_isl_ICE_NT_Non-Drama/*.mp3; do
  # Use basename to get the file name without the extension
  base_name=$(basename "$file" .mp3)
  
  # Construct the output file path with the new extension
  output="Icelandic_isl_ICE_NT_Non-Drama_Converted/${base_name}.wav"
  
  # Run ffmpeg command
  ffmpeg -i "$file" -ar 16000 -ac 1 -ss 00:00:04 "$output"
done
