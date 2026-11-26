
import os
import tempfile
import subprocess
import gradio as gr

def make_clips(video):
    if video is None:
        return "Please upload a video first."

    output_dir = tempfile.mkdtemp()

    command = [
        "ffmpeg", "-i", video,
        "-t", "1800",
        "-vf", "fps=1/30,scale=720:-2",
        "-an",
        os.path.join(output_dir, "clip_%03d.mp4")
    ]

    try:
        subprocess.run(command, check=True)
        return "Video processed successfully: " + output_dir
    except Exception as e:
        return "Processing error: " + str(e)

demo = gr.Interface(
    fn=make_clips,
    inputs=gr.Video(label="Upload your video"),
    outputs=gr.Textbox(label="Result"),
    title="ClipKing AI 👑",
    description="AI Video Clip Maker"
)

demo.launch()
  
