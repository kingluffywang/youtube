import argparse
from faster_whisper import WhisperModel
from pydub import AudioSegment
import numpy as np
import time
import os

def transcribe_audio(audio_file_path, output_file_path, language="zh"):
    print(f"开始处理音频文件: {audio_file_path}")
    start_time = time.time()

    # 假设输入文件为 MP3 格式
    print("正在加载Whisper模型...")
    model = WhisperModel("large-v2", device="cpu", compute_type="int8")
    print(f"模型加载完成，用时 {time.time() - start_time:.2f} 秒")

    print("正在加载音频文件...")
    audio = AudioSegment.from_file(audio_file_path, format="mp3")
    audio = audio.set_channels(1).set_frame_rate(16000)
    print(f"音频加载完成，音频长度: {len(audio) / 1000:.2f} 秒")

    print("正在将音频转换为numpy数组...")
    audio_numpy = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0
    print("转换完成")

    print("开始转录音频...")
    transcribe_start = time.time()
    segments, info = model.transcribe(audio_numpy, language=language)

    print("正在收集转录结果...")
    transcription = ""
    for segment in segments:
        transcription += segment.text + " "
        print(f"已处理 {segment.end:.2f} 秒 / {len(audio) / 1000:.2f} 秒")

    print(f"转录完成，用时 {time.time() - transcribe_start:.2f} 秒")

    print(f"正在保存转录结果到文件: {output_file_path}")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(transcription)
    print("保存完成")

    total_time = time.time() - start_time
    print(f"全部处理完成，总用时 {total_time:.2f} 秒")

    return transcription

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe MP3 audio files to text.")
    parser.add_argument("-i", "--input", required=True, help="Path to the MP3 audio file.")
    parser.add_argument("-o", "--output", required=True, help="Path to save the transcribed text.")
    parser.add_argument("--lang", default="zh", help="Language of the audio (default: zh).")

    args = parser.parse_args()

    result = transcribe_audio(args.input, args.output, language=args.lang)
    print(f"转录结果已保存到: {args.output}")
    print("转录结果的前500个字符:", result[:500])