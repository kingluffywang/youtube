# 导入所需的库
from moviepy.editor import VideoFileClip  # 导入视频处理库
import os  # 导入操作系统接口库

def split_video(input_video_path, output_folder):
    """
    将输入视频按照59秒为间隔分割成多个片段
    
    参数:
        input_video_path: 输入视频的路径
        output_folder: 分割后视频片段的保存目录
    """
    
    # 确保输出文件夹存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 使用VideoFileClip加载视频文件
    video = VideoFileClip(input_video_path)
    
    # 获取视频总时长并计算需要分割的片段数
    # 如果视频长度不能被59整除，则多加一个片段
    duration = video.duration  # 获取视频总时长(秒)
    num_clips = int(duration // 59) + (1 if duration % 59 > 0 else 0)
    
    # 循环处理每个视频片段
    for i in range(num_clips):
        # 计算当前片段的起始和结束时间
        start_time = i * 59  # 每段起始时间
        end_time = min((i + 1) * 59, duration)  # 每段结束时间，不超过视频总长度
        
        # 从原视频中提取指定时间段的片段
        clip = video.subclip(start_time, end_time)
        
        # 生成输出文件名，格式为"clip_001.mp4"这样的形式
        output_filename = f"clip_{i+1:03d}.mp4"  # 使用3位数字进行编号
        output_path = os.path.join(output_folder, output_filename)
        
        # 将视频片段保存到文件
        # codec指定视频编码格式为H.264
        # audio_codec指定音频编码格式为AAC
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
        # 打印进度信息
        print(f"已生成片段 {i+1}/{num_clips}: {output_filename}")
    
    # 处理完成后关闭视频文件，释放资源
    video.close()
    
    # 打印完成信息
    print(f"视频分割完成。共生成 {num_clips} 个片段。")

# 使用示例
input_video = "sample_video.mp4"  # 输入视频文件路径
output_folder = "video_shorts_clips"  # 输出文件夹路径

# 调用函数进行视频分割
split_video(input_video, output_folder)
