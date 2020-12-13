import speech_recognition as sr
import numpy as np
import os, sys, wave, math, struct
from scipy import int16

if len(sys.argv) < 2:
    print("Usage: python transcribe.py <wav file> [output file]")
    print("Example: python transcribe.py hoge.wav output.txt")
    exit()

if len(sys.argv) > 2:
    output_file_name = sys.argv[2]
    if os.path.exists(output_file_name):
        os.remove(output_file_name)

temp_dir_name = "tmp"
input_file_name = sys.argv[1]
split_time = 60 # 何秒ごとに分割するか

if os.path.exists(temp_dir_name) == False:
    os.mkdir(temp_dir_name)

with wave.open(input_file_name, "rb") as wr:
    channels = wr.getnchannels()    # オーディオチャンネル数
    width = wr.getsampwidth()      # サンプルサイズのバイト数
    framerate = wr.getframerate()  # サンプリングレート
    nframes = wr.getnframes()      # オーディオフレーム数

    total_time = math.floor(1.0 * nframes / framerate)  # オーディオファイルの秒数
    frames = int(channels * framerate * split_time)     # 分割したときのフレーム数
    split_num = math.ceil(total_time / split_time)     # 分割数

    data = wr.readframes(nframes)

audio_data = np.frombuffer(data, dtype=int16)

for i in range(split_num):
    temp_path = f"{temp_dir_name}/{i}.wav"
    start_cut = int(i * frames)
    end_cut = int(i * frames + frames)
    cut_audio_data = audio_data[start_cut:end_cut]
    temp_audio = struct.pack("h" * len(cut_audio_data), *cut_audio_data)

    # 分割した音声ファイルの書き出し
    with wave.open(temp_path, "w") as wr:
        wr.setnchannels(channels)
        wr.setsampwidth(width)
        wr.setframerate(framerate)
        wr.writeframes(temp_audio)

    r = sr.Recognizer()
    with sr.AudioFile(temp_path) as wr:
        audio = r.record(wr)

    try:
        result = r.recognize_google(audio, language="ja-JP")
        if len(sys.argv) == 2:
            print(result)
        else:
            with open(sys.argv[2], mode="a") as f:
                f.write(result)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results form Google Speech Recognition service; {e}")

    os.remove(temp_path)

os.rmdir(temp_dir_name)