
import os
import tempfile
import subprocess
import gradio as gr

def make_clips(video):
    if not video:
        return []

    output_dir = tempfile.mkdtemp()
    output_pattern = os.path.join(output_dir, "ClipKing_%03d.mp4")

    command = [
        "ffmpeg", "-y",
        "-i", video,
        "-t", "1800",
        "-map", "0:v:0",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        "-c:a", "aac",
        "-f", "segment",
        "-segment_time", "30",
        "-reset_timestamps", "1",
        output_pattern
    ]

    try:
        subprocess.run(command, check=True, capture_output=True)
        files = sorted(
            os.path.join(output_dir, f)
            for f in os.listdir(output_dir)
            if f.endswith(".mp4")
        )
        return files
    except Exception as e:
        raise gr.Error(str(e))

demo = gr.Interface(
    fn=make_clips,
    inputs=gr.Video(label="Upload your video"),
    outputs=gr.File(label="Download your clips", file_count="multiple"),
    title="👑 ClipKing AI",
    description="Upload a video up to 30 minutes and create 30-second clips."
)

demo.launch(server_name="0.0.0.0",
            server_port=int(os.environ.get("PORT", 7860)))
