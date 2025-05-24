#!/bin/bash

# Find files and store in an array
files=($(find . -name "lds4_buoi_02*"))

# Process each file with ffmpeg
no_chapter_files=()
for file in "${files[@]}"; do
    output_file="${file%.*}_no_chapters.mp4"
    ffmpeg -i "$file" -c copy "$output_file"
    no_chapter_files+=("$output_file")
done

no_chapter_files=($(printf "%s\n" "${no_chapter_files[@]}" | sort))

#----------------------#
printf "file '%s'\n" "${no_chapter_files[@]}" > ./input_files.txt

ffmpeg -f concat -safe 0 -i ./input_files.txt -c copy ./2.DS4_SQL_buoi02.mp4

# Optional: Remove temporary files
rm "${no_chapter_files[@]}" input_files.txt
