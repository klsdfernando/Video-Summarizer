import argparse
import os
import sys
import time
import cv2
import whisper
import torch
try:
    from moviepy.editor import VideoFileClip
except ImportError:
    try:
        from moviepy import VideoFileClip
    except ImportError:
        # For MoviePy 2.0+
        from moviepy.video.io.VideoFileClip import VideoFileClip
from openai import OpenAI
from pathlib import Path

def extract_audio(video_path, audio_output_path):
    """Extracts audio from video using MoviePy."""
    print(f"--- Extracting audio from {video_path} ---")
    clip = VideoFileClip(video_path)
    if clip.audio is None:
        raise ValueError("Video does not have an audio track.")
    clip.audio.write_audiofile(audio_output_path, logger=None)
    clip.close()
    print(f"Audio extracted to: {audio_output_path}")

def extract_screenshots(video_path, output_dir, interval_seconds):
    """Extracts screenshots from video at regular intervals using OpenCV."""
    print(f"--- Extracting screenshots every {interval_seconds} seconds ---")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    interval_frames = int(fps * interval_seconds)
    
    count = 0
    frame_idx = 0
    os.makedirs(output_dir, exist_ok=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_idx % interval_frames == 0:
            screenshot_path = os.path.join(output_dir, f"screenshot_{count:04d}.jpg")
            cv2.imwrite(screenshot_path, frame)
            count += 1
        
        frame_idx += 1
    
    cap.release()
    print(f"Extracted {count} screenshots to: {output_dir}")

def transcribe_audio(audio_path, model_name="base"):
    """Transcribes audio using Whisper, utilizing CUDA if available."""
    print(f"--- Transcribing audio using Whisper ({model_name} model) ---")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    model = whisper.load_model(model_name, device=device)
    result = model.transcribe(audio_path)
    return result["text"]

def summarize_text(text, api_url, api_key, model_name="gpt-3.5-turbo", max_tokens=1000):
    """Summarizes text using an OpenAI-compatible API."""
    print(f"--- Summarizing transcript using LLM ({model_name}) ---")
    
    client = OpenAI(
        base_url=api_url,
        api_key=api_key if api_key else "not-needed-for-local"
    )
    
    prompt = (
        "Please provide a concise and well-structured summary of the following video transcript. "
        "Highlight the key points and main takeaways.\n\n"
        f"Transcript:\n{text}"
    )
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": "You are a professional video summarizer."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during summarization: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Video Summarization CLI Tool")
    parser.add_argument("video", help="Path to the input video file")
    parser.add_argument("-o", "--output", default="output", help="Directory for output files (default: 'output')")
    parser.add_argument("-i", "--interval", type=int, default=10, help="Screenshot interval in seconds (default: 10)")
    parser.add_argument("-m", "--model", default="base", help="Whisper model size (tiny, base, small, medium, large) (default: base)")
    parser.add_argument("--llm-url", default="http://localhost:1234/v1", help="URL for the OpenAI-compatible LLM (e.g., LM Studio local URL)")
    parser.add_argument("--llm-key", default="", help="API Key for the LLM (if using a cloud provider)")
    parser.add_argument("--llm-model", default="local-model", help="Model name for the LLM API")
    parser.add_argument("--max-tokens", type=int, default=1000, help="Maximum tokens for the summary output (default: 1000)")

    args = parser.parse_args()

    video_path = args.video
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        sys.exit(1)

    # Setup output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    audio_path = output_dir / "audio_temp.mp3"
    screenshots_dir = output_dir / "screenshots"
    transcript_path = output_dir / "transcript.txt"
    summary_path = output_dir / "summary.txt"

    start_time = time.time()

    try:
        # Step 1: Extract screenshots
        extract_screenshots(video_path, str(screenshots_dir), args.interval)

        # Step 2: Extract audio
        extract_audio(video_path, str(audio_path))

        # Step 3: Transcribe
        transcript = transcribe_audio(str(audio_path), args.model)
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"Transcript saved to: {transcript_path}")

        # Step 4: Summarize
        summary = summarize_text(transcript, args.llm_url, args.llm_key, args.llm_model, args.max_tokens)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"Summary saved to: {summary_path}")

        # Cleanup
        if os.path.exists(audio_path):
            os.remove(audio_path)

        end_time = time.time()
        print(f"\nProcessing complete! Total time: {end_time - start_time:.2f} seconds.")
        print(f"Results are available in: {output_dir}")

    except Exception as e:
        print(f"\nAn error occurred during processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
