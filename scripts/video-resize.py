# 导入所需的库
import subprocess  # 用于执行外部命令
import os  # 用于文件和目录操作

def resize_video_for_youtube_shorts(input_file, output_file):
   """
   将视频转换为YouTube Shorts格式(1080x1920)的竖屏视频
   
   参数:
       input_file (str): 输入视频文件的路径
       output_file (str): 输出视频文件的路径
       
   处理流程:
   1. 将视频缩放到1080x1920的尺寸
   2. 保持原始视频的宽高比
   3. 在视频周围添加黑边使其居中
   4. 保持原始音频不变
   """
   
   # 确保输出文件的目录存在,如果不存在则创建
   os.makedirs(os.path.dirname(output_file), exist_ok=True)
   
   # 构建 FFmpeg 命令参数列表
   command = [
       'ffmpeg',  # FFmpeg 程序
       '-i', input_file,  # 输入文件参数
       # 视频滤镜参数:
       '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2',
       # scale=1080:1920 - 设置目标分辨率
       # force_original_aspect_ratio=decrease - 保持原始宽高比,确保视频不会被拉伸
       # pad=1080:1920:(ow-iw)/2:(oh-ih)/2 - 添加黑边使视频居中
       # (ow-iw)/2:(oh-ih)/2 计算填充边距,使视频在画面中居中
       
       '-c:a', 'copy',  # 复制音频流,不进行重新编码
       output_file  # 输出文件路径
   ]
   
   # 执行 FFmpeg 命令
   try:
       # check=True 表示在命令执行失败时抛出异常
       subprocess.run(command, check=True)
       print(f"视频已成功调整大小并保存为 {output_file}")
   except subprocess.CalledProcessError as e:
       # 捕获并打印 FFmpeg 执行过程中的错误
       print(f"调整视频大小时出错: {e}")

# 使用示例
input_video = "input.mp4"    # 输入视频文件路径
output_video = "output.mp4"  # 输出视频文件路径
resize_video_for_youtube_shorts(input_video, output_video)
