import gradio as gr
import subprocess
import os

def resize_video_for_youtube_shorts(input_file, output_file):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, os.path.basename(output_file))
    
    command = [
        'ffmpeg',
        '-i', input_file,
        '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2',
        '-c:a', 'copy',
        output_file
    ]
    
    try:
        subprocess.run(command, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error resizing video: {e}")
        return None

def split_video(input_video_path):
    output_folder = "output/shorts_clips"
    os.makedirs(output_folder, exist_ok=True)
    
    # Get video duration using ffmpeg
    duration_cmd = [
        'ffmpeg',
        '-i', input_video_path,
        '-f', 'null',
        '-'
    ]
    
    # Get video duration
    result = subprocess.run(duration_cmd, capture_output=True)
    duration_output = result.stderr.decode()
    duration_line = [line for line in duration_output.split('\n') if "Duration" in line][0]
    duration_str = duration_line.split("Duration: ")[1].split(",")[0]
    h, m, s = map(float, duration_str.split(':'))
    total_seconds = h * 3600 + m * 60 + s
    
    # Calculate number of clips
    num_clips = int(total_seconds // 59) + (1 if total_seconds % 59 > 0 else 0)
    output_files = []
    
    for i in range(num_clips):
        start_time = i * 59
        output_filename = f"clip_{i+1:03d}.mp4"
        output_path = os.path.join(output_folder, output_filename)
        
        split_cmd = [
            'ffmpeg',
            '-i', input_video_path,
            '-ss', str(start_time),
            '-t', '59',
            '-c', 'copy',
            output_path
        ]
        
        subprocess.run(split_cmd, check=True)
        output_files.append(output_path)
    
    return output_files
def process_resize(video):
    if video is None:
        return None
        
    # Handle both string paths and file objects
    input_path = video.name if hasattr(video, 'name') else video
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, os.path.basename(input_path).replace(".mp4", "_shorts.mp4"))
    return resize_video_for_youtube_shorts(input_path, output_filename)

def process_split(video):
    if video is None:
        return None
        
    input_path = video.name if hasattr(video, 'name') else video
    
    output_dir = "output/shorts_clips"
    os.makedirs(output_dir, exist_ok=True)
    return split_video(input_path)

with gr.Blocks(title="YouTube Video Processor") as demo:
    gr.Markdown("# YouTube Video Processor")
    
    with gr.Tabs():
        with gr.TabItem("Resize for Shorts"):
            with gr.Column():
                video_input_resize = gr.File(label="Upload Video")
                resize_output = gr.Video(label="Resized Video")
                resize_button = gr.Button("Convert to Shorts Format")
                resize_button.click(fn=process_resize, inputs=video_input_resize, outputs=resize_output)
        
        with gr.TabItem("Split Video"):
            with gr.Column():
                video_input_split = gr.File(label="Upload Video")
                split_output = gr.File(label="Split Video Clips", file_count="multiple")
                split_button = gr.Button("Split into 59s Clips")
                split_button.click(fn=process_split, inputs=video_input_split, outputs=split_output)

if __name__ == "__main__":
    demo.launch()
    