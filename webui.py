import gradio as gr
from scripts.zimu_jianti import transcribe_audio_to_srt
from scripts.CN_mp3_audio2text import transcribe_audio
from scripts.helper_srt_spacerm import remove_spaces_newlines
import os

def process_audio_srt(audio_file, language, chinese_conversion):
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
            to_simplified=to_simplified
        )
        
        with open(output_path, "r", encoding="utf-8") as f:
            srt_content = f.read()
            
        return f"Subtitle file saved in: {output_path}\n\n{srt_content}"
        
    except Exception as e:
        return f"Error processing audio: {str(e)}"

def process_audio_text(audio_file, language):
    if audio_file is None:
        return "Please upload an audio file"
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    original_filename = os.path.basename(audio_file.name)
    base_name = os.path.splitext(original_filename)[0]
    output_path = os.path.join(output_dir, base_name + ".txt")
    
    try:
        result = transcribe_audio(audio_file.name, output_path, language=language)
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
    with gr.Blocks(title="Audio & Subtitle Processing Tool") as app:
        gr.Markdown("# Audio & Subtitle Processing Tool")
        
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
                        chinese_conversion = gr.Dropdown(
                            choices=["No Conversion", "To Simplified", "To Traditional"],
                            value="To Simplified",
                            label="Chinese Character Conversion"
                        )
                        srt_submit_btn = gr.Button("Generate Subtitles")
                    
                    with gr.Column():
                        srt_output = gr.TextArea(label="Generated Subtitles (SRT format)", lines=10)

            with gr.Tab("Plain Text Transcription"):
                with gr.Row():
                    with gr.Column():
                        text_audio_input = gr.File(label="Upload Audio File", file_types=["audio"])
                        text_language = gr.Dropdown(
                            choices=["zh", "en", "ja", "ko", "fr", "de", "es", "ru"],
                            value="zh",
                            label="Select Language"
                        )
                        text_submit_btn = gr.Button("Transcribe to Text")
                    
                    with gr.Column():
                        text_output = gr.TextArea(label="Transcribed Text", lines=10)

            with gr.Tab("SRT Space Removal"):
                with gr.Row():
                    with gr.Column():
                        srt_file_input = gr.File(
                            label="Upload SRT File",
                            file_types=[".srt"]
                        )
                        space_remove_btn = gr.Button("Remove Spaces and Newlines")
                    
                    with gr.Column():
                        space_remove_output = gr.TextArea(
                            label="Processed SRT Content",
                            lines=10
                        )

        srt_submit_btn.click(
            fn=process_audio_srt,
            inputs=[srt_audio_input, srt_language, chinese_conversion],
            outputs=srt_output
        )

        text_submit_btn.click(
            fn=process_audio_text,
            inputs=[text_audio_input, text_language],
            outputs=text_output
        )

        space_remove_btn.click(
            fn=process_srt_spaces,
            inputs=[srt_file_input],
            outputs=space_remove_output
        )
    
    return app

if __name__ == "__main__":
    app = create_ui()
    app.launch()