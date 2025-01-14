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

    video = VideoFileClip(input_video_path)
    duration = video.duration
    num_clips = int(duration // 59) + (1 if duration % 59 > 0 else 0)
    output_files = []
    
    for i in range(num_clips):
        start_time = i * 59
        end_time = min((i + 1) * 59, duration)
        clip = video.subclip(start_time, end_time)
        
        output_filename = f"clip_{i+1:03d}.mp4"
        output_path = os.path.join(output_folder, output_filename)
        
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        output_files.append(output_path)
    
    video.close()
    return output_files
def process_resize(video):
    if video is None:
        return None
    input_path = video.name
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, os.path.basename(input_path).replace(".mp4", "_shorts.mp4"))
    return resize_video_for_youtube_shorts(input_path, output_filename)

def process_split(video):
    if video is None:
        return None
    input_path = video.name
    output_dir = "output/shorts_clips"
    os.makedirs(output_dir, exist_ok=True)
    return split_video(input_path)

with gr.Blocks(title="YouTube Video Processor") as demo:
    gr.Markdown("# YouTube Video Processor")
    
    with gr.Tabs():
        with gr.TabItem("Resize for Shorts"):
            with gr.Column():
                video_input_resize = gr.Video(label="Upload Video")
                resize_output = gr.Video(label="Resized Video")
                resize_button = gr.Button("Convert to Shorts Format")
                resize_button.click(fn=process_resize, inputs=video_input_resize, outputs=resize_output)
        
        with gr.TabItem("Split Video"):
            with gr.Column():
                video_input_split = gr.Video(label="Upload Video")
                split_output = gr.File(label="Split Video Clips", file_count="multiple")
                split_button = gr.Button("Split into 59s Clips")
                split_button.click(fn=process_split, inputs=video_input_split, outputs=split_output)

if __name__ == "__main__":
    demo.launch()
    