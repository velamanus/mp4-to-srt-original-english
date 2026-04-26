import os
from deep_translator import GoogleTranslator
import subprocess

def convert_and_translate(mp4_file, wav_file, srt_file, output_srt_file):
    # Step 1: Convert MP4 to WAV using ffmpeg
    subprocess.run(["ffmpeg", "-i", mp4_file, "-ar", "16000", "-ac", "1", wav_file])

    # Step 2: Transcribe WAV to SRT using Whisper
    subprocess.run(["whisper", wav_file, "--model", "small", "--language", "zh", "--output_format", "srt"])


    # Step 3: Read original SRT file
    with open(srt_file, "r", encoding="utf-8") as file:
        content = file.read()

    # Split content into blocks
    blocks = content.strip().split("\n\n")
    translated_blocks = []

    # Translate subtitle blocks
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 3:
            index = lines[0]
            time = lines[1]
            text_lines = lines[2:]
            text = " ".join(text_lines)
            try:
                translated_text = GoogleTranslator(source="auto", target="en").translate(text)
            except Exception:
                translated_text = "[Translation Error]"
            translated_block = f"{index}\n{time}\n{translated_text}"
            translated_blocks.append(translated_block)

    # Write translated SRT file
    with open(output_srt_file, "w", encoding="utf-8") as file:
        file.write("\n\n".join(translated_blocks))

    print(f"Translation complete. Output saved to: {output_srt_file}")


# Loop through multiple files
for i in range(1, 11):  # Adjust the range as needed
    mp4_file = f"{i}.mp4"
    wav_file = f"{i}.wav"
    srt_file = f"{i}.srt"       # Whisper will create this
    output_srt_file = f"en{i}.srt"

    if os.path.exists(mp4_file):
        print(f"Processing file: {mp4_file}")
        convert_and_translate(mp4_file, wav_file, srt_file, output_srt_file)
    else:
        print(f"File not found: {mp4_file}")
