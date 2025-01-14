import gradio as gr
from scripts.zimu_jianti import transcribe_audio_to_srt
from scripts.CN_mp3_audio2text import transcribe_audio
from scripts.helper_srt_spacerm import remove_spaces_newlines
import os
import subprocess
import pkg_resources
import webbrowser

def open_folder(path):
    """Opens the folder in file explorer"""
    if os.path.exists(path):
        webbrowser.open(os.path.realpath(path))
    return path

def check_requirements():
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
    
    for requirement in requirements:
        try:
            pkg_resources.require(requirement)
        except:
            print(f"Installing {requirement}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])

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
    
    duration_cmd = [
        'ffmpeg',
        '-i', input_video_path,
        '-f', 'null',
        '-'
    ]
    
    result = subprocess.run(duration_cmd, capture_output=True)
    duration_output = result.stderr.decode()
    duration_line = [line for line in duration_output.split('\n') if "Duration" in line][0]
    duration_str = duration_line.split("Duration: ")[1].split(",")[0]
    h, m, s = map(float, duration_str.split(':'))
    total_seconds = h * 3600 + m * 60 + s
    
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
    input_path = video.name if hasattr(video, 'name') else video
    output_dir = "output/resized_videos"
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

def process_audio_srt(audio_file, language, chinese_conversion, device):
    if audio_file is None:
        return "Please upload an audio file"
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    original_filename = os.path.basename(audio_file.name)
    base_name = os.path.splitext(original_filename)[0]
    output_path = os.path.join(output_dir, base_name + ".srt")
    
    to_simplified = chinese_conversion == "To Simplified"
    
    try:
        transcribe_audio_to_srt(
            audio_file.name, 
            output_path, 
            language=language,
            to_simplified=to_simplified,
            device=device
        )
        
        with open(output_path, "r", encoding="utf-8") as f:
            srt_content = f.read()
            
        return f"Subtitle file saved in: {output_path}\n\n{srt_content}"
        
    except Exception as e:
        return f"Error processing audio: {str(e)}"

def process_audio_text(audio_file, language, device):
    if audio_file is None:
        return "Please upload an audio file"
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    original_filename = os.path.basename(audio_file.name)
    base_name = os.path.splitext(original_filename)[0]
    output_path = os.path.join(output_dir, base_name + ".txt")
    
    try:
        result = transcribe_audio(
            audio_file.name, 
            output_path, 
            language=language,
            device=device
        )
        return f"Text file saved in: {output_path}\n\n{result}"
    except Exception as e:
        return f"Error processing audio: {str(e)}"

def process_srt_spaces(input_srt):
    if input_srt is None:
        return "Please upload an SRT file"
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    original_filename = os.path.basename(input_srt.name)
    base_name = os.path.splitext(original_filename)[0]
    output_path = os.path.join(output_dir, f"{base_name}_nospaces.srt")
    
    try:
        remove_spaces_newlines(input_srt.name, output_path)
        
        with open(output_path, "r", encoding="utf-8") as f:
            processed_content = f.read()
            
        return f"Processed file saved in: {output_path}\n\n{processed_content}"
    except Exception as e:
        return f"Error processing SRT: {str(e)}"

def create_ui():
    with gr.Blocks(title="Audio, Subtitle & Video Processing Tool") as app:
        gr.Markdown("# Audio, Subtitle & Video Processing Tool")
        
        with gr.Tabs():
            with gr.Tab("Subtitle Generator (SRT)"):
                with gr.Row():
                    with gr.Column():
                        srt_audio_input = gr.File(label="Upload Audio File", file_types=["audio"])
                        srt_language = gr.Dropdown(
                            choices=["zh", "en", "ja", "ko", "fr", "de", "es", "ru"],
                            value="zh",
                            label="Select Language"
                        )
                        with gr.Row():
                            srt_device = gr.Radio(
                                choices=["cpu", "cuda"],
                                value="cpu",
                                label="Processing Device"
                            )
                            chinese_conversion = gr.Dropdown(
                                choices=["No Conversion", "To Simplified", "To Traditional"],
                                value="To Simplified",
                                label="Chinese Character Conversion"
                            )
                        srt_submit_btn = gr.Button("Generate Subtitles", variant="primary")
                    
                    with gr.Column():
                        srt_output = gr.TextArea(label="Generated Subtitles (SRT format)", lines=10)
                        gr.Markdown("Output files will be saved to: `./output/*.srt`")

            with gr.Tab("Plain Text Transcription"):
                with gr.Row():
                    with gr.Column():
                        text_audio_input = gr.File(label="Upload Audio File", file_types=["audio"])
                        text_language = gr.Dropdown(
                            choices=["zh", "en", "ja", "ko", "fr", "de", "es", "ru"],
                            value="zh",
                            label="Select Language"
                        )
                        with gr.Row():
                            text_device = gr.Radio(
                                choices=["cpu", "cuda"],
                                value="cpu",
                                label="Processing Device"
                            )
                        text_submit_btn = gr.Button("Transcribe to Text", variant="primary")
                    
                    with gr.Column():
                        text_output = gr.TextArea(label="Transcribed Text", lines=10)
                        gr.Markdown("Output files will be saved to: `./output/*.txt`")
                        

            with gr.Tab("SRT Space Removal"):
                with gr.Row():
                    with gr.Column():
                        srt_file_input = gr.File(
                            label="Upload SRT File",
                            file_types=[".srt"]
                        )
                        space_remove_btn = gr.Button("Remove Spaces and Newlines", variant="primary")
                    
                    with gr.Column():
                        space_remove_output = gr.TextArea(
                            label="Processed SRT Content",
                            lines=10
                        )
                        gr.Markdown("Output files will be saved to: `./output/*_nospaces.srt`")

            with gr.Tab("YouTube Shorts Converter"):
                with gr.Row():
                    with gr.Column():
                        video_input_resize = gr.File(label="Upload Video")
                        resize_button = gr.Button("Convert to Shorts Format", variant="primary")
                    with gr.Column():
                        resize_output = gr.Video(label="Resized Video")
                        gr.Markdown("Output files will be saved to: `./output/resized_videos/`")                       

            with gr.Tab("Video Splitter"):
                with gr.Row():
                    with gr.Column():
                        video_input_split = gr.File(label="Upload Video")
                        split_button = gr.Button("Split into 59s Clips", variant="primary")
                    with gr.Column():
                        split_output = gr.File(label="Split Video Clips", file_count="multiple")
                        gr.Markdown("Output files will be saved to: `./output/shorts_clips/`")
                    

        srt_submit_btn.click(
            fn=process_audio_srt,
            inputs=[srt_audio_input, srt_language, chinese_conversion, srt_device],
            outputs=srt_output
        )

        text_submit_btn.click(
            fn=process_audio_text,
            inputs=[text_audio_input, text_language, text_device],
            outputs=text_output
        )

        space_remove_btn.click(
            fn=process_srt_spaces,
            inputs=[srt_file_input],
            outputs=space_remove_output
        )

        resize_button.click(
            fn=process_resize,
            inputs=video_input_resize,
            outputs=resize_output
        )

        split_button.click(
            fn=process_split,
            inputs=video_input_split,
            outputs=split_output
        )
    return app

if __name__ == "__main__":
    check_requirements()  # Add this line before creating the UI
    app = create_ui()
    app.launch()