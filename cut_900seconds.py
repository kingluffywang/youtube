from moviepy.editor import VideoFileClip
import os
import sys
from moviepy.config import get_setting
import subprocess

def get_ffmpeg_path():
    """获取 ffmpeg 路径"""
    return get_setting("FFMPEG_BINARY")

def check_ffmpeg():
    """检查 ffmpeg 是否正确安装"""
    try:
        subprocess.run([get_ffmpeg_path(), "-version"], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
        return True
    except Exception as e:
        print(f"FFMPEG 检查失败: {str(e)}")
        return False

def split_video(input_video_path, output_folder):
    # 检查输入文件是否存在
    if not os.path.exists(input_video_path):
        raise FileNotFoundError(f"找不到输入视频文件: {input_video_path}")
        
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 检查 ffmpeg
    if not check_ffmpeg():
        print("请确保已正确安装 ffmpeg")
        return

    video = None
    try:
        # 加载视频
        print("正在加载视频文件...")
        video = VideoFileClip(input_video_path)
        
        # 检查视频是否正确加载
        if video.reader is None:
            raise ValueError("视频文件无法正确加载")
        
        # 计算需要分割的片段数 (15分钟 = 900秒)
        duration = video.duration
        segment_duration = 900  # 15分钟
        num_clips = int(duration // segment_duration) + (1 if duration % segment_duration > 0 else 0)
        
        print(f"视频总时长: {duration:.2f} 秒")
        print(f"将分割成 {num_clips} 个片段")
        
        for i in range(num_clips):
            start_time = i * segment_duration
            end_time = min((i + 1) * segment_duration, duration)
            
            # 提取片段
            print(f"\n开始处理片段 {i+1}/{num_clips}")
            print(f"时间范围: {start_time:.2f}s - {end_time:.2f}s")
            
            # 生成输出文件名
            start_minutes = int(start_time // 60)
            end_minutes = int(end_time // 60)
            output_filename = f"clip_{i+1:03d}_{start_minutes:02d}min-{end_minutes:02d}min.mp4"
            output_path = os.path.join(output_folder, output_filename)
            
            print(f"正在导出: {output_filename}")
            
            try:
                # 使用 ffmpeg 直接切割视频
                ffmpeg_cmd = [
                    get_ffmpeg_path(),
                    "-i", input_video_path,
                    "-ss", str(start_time),
                    "-t", str(end_time - start_time),
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    "-avoid_negative_ts", "1",
                    output_path,
                    "-y"  # 覆盖现有文件
                ]
                
                # 执行 ffmpeg 命令
                process = subprocess.run(
                    ffmpeg_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                if process.returncode != 0:
                    print(f"片段导出失败，错误信息：{process.stderr}")
                    continue
                    
                print(f"片段 {i+1}/{num_clips} 导出完成")
                
            except Exception as e:
                print(f"导出片段时出错: {str(e)}")
                continue
        
        print("\n所有片段处理完成！")
    
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")
        print("错误详情:", sys.exc_info()[2])
    
    finally:
        # 确保视频文件被正确关闭
        if video is not None:
            video.close()

if __name__ == "__main__":
    # 使用示例
    input_video = "input.mp4"  # 替换为你的视频文件路径
    output_folder = "output_clips"  # 替换为你想要保存片段的文件夹路径
    
    split_video(input_video, output_folder)
