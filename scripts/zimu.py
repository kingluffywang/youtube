from faster_whisper import WhisperModel
from pydub import AudioSegment
import numpy as np
import time

def seconds_to_srt_timestamp(seconds: float) -> str:
    """
    将秒数转换为 SRT 时间戳格式（HH:MM:SS,mmm）
    例如：3.456秒 -> "00:00:03,456"
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def transcribe_audio_to_srt(audio_file_path: str, output_srt_path: str, language="zh"):
    """
    将音频文件转录为带有时间戳的 SRT 字幕文件。
    输出格式示例：
    1
    00:00:24,400 --> 00:00:25,200
    烟雨

    :param audio_file_path: 音频文件路径（如 mp3）
    :param output_srt_path: 输出字幕文件路径（.srt）
    :param language: 语言代码（默认为中文 "zh"）
    """
    print(f"开始处理音频文件: {audio_file_path}")
    start_time = time.time()

    # 1) 加载 WhisperModel
    print("正在加载Whisper模型...")
    model = WhisperModel("large-v2", device="cpu", compute_type="int8")
    print(f"模型加载完成，用时 {time.time() - start_time:.2f} 秒")

    # 2) 加载并预处理音频
    print("正在加载音频文件...")
    audio = AudioSegment.from_file(audio_file_path, format="mp3")
    audio = audio.set_channels(1).set_frame_rate(16000)
    print(f"音频加载完成，音频长度: {len(audio) / 1000:.2f} 秒")

    # 3) 转为 NumPy 数组
    print("正在将音频转换为 numpy 数组...")
    audio_numpy = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0
    print("转换完成")

    # 4) 开始转录
    print("开始转录音频...")
    transcribe_start = time.time()
    segments, info = model.transcribe(audio_numpy, language=language)
    print(f"转录完成，用时 {time.time() - transcribe_start:.2f} 秒")

    # 5) 生成 SRT 内容
    print("正在生成字幕文件...")
    srt_lines = []
    for idx, segment in enumerate(segments, start=1):
        # 生成 SRT 时间戳
        start_srt_time = seconds_to_srt_timestamp(segment.start)
        end_srt_time = seconds_to_srt_timestamp(segment.end)

        # 序号
        srt_lines.append(str(idx))
        # 时间轴
        srt_lines.append(f"{start_srt_time} --> {end_srt_time}")
        # 文本内容（去除首尾空格）
        srt_lines.append(segment.text.strip())
        # 空行分隔
        srt_lines.append("")

        # 打印进度
        print(f"片段 {idx}: {segment.start:.2f}s --> {segment.end:.2f}s")

    # 6) 写入 .srt 文件
    with open(output_srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))

    total_time = time.time() - start_time
    print(f"字幕文件已生成: {output_srt_path}")
    print(f"全部处理完成，总用时 {total_time:.2f} 秒")

    return output_srt_path

# 使用示例
if __name__ == "__main__":
    audio_file = "audio_file.mp3"   # 替换为你的音频文件路径
    output_srt = audio_file + ".srt"   # 替换为你要输出的字幕文件名称
    result_srt_path = transcribe_audio_to_srt(audio_file, output_srt, language="zh")
    print(f"转录字幕文件已保存到: {result_srt_path}")
