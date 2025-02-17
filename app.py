"""
This file is part of Face Swapper, a modified version of roop.
Original work Copyright (C) 2025 s0md3v (https://github.com/s0md3v)
Modified work Copyright (C) 2025 Jose Thomas

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import streamlit as st
import os
import subprocess
from pathlib import Path

# Set up local directories for file uploads and the roop repository
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
ROOP_DIR = BASE_DIR / "roop"
UPLOAD_DIR.mkdir(exist_ok=True)

def run_script(image_file, video_file):
    """
    Save uploaded files locally and execute the face swapping process using the roop repository.
    
    Parameters:
    image_file: Uploaded image file (e.g., jpg, png)
    video_file: Uploaded target video file (mp4)
    
    Returns:
    Path to the generated video file with swapped faces.
    """
    # Define paths for saving input and output files
    image_path = UPLOAD_DIR / "input_image.jpg"
    video_path = UPLOAD_DIR / "input_video.mp4"
    output_video_path = UPLOAD_DIR / "swapped.mp4"
    
    # Save the uploaded image and video to disk
    with open(image_path, "wb") as f:
        f.write(image_file.getvalue())
    with open(video_path, "wb") as f:
        f.write(video_file.getvalue())
    
    # Construct the command to run the face swapping script locally
    cmd = [
        "python", str(ROOP_DIR / "run.py"),
        "--target", str(video_path),
        "--source", str(image_path),
        "-o", str(output_video_path),
        "--output-video-quality", "80",
        "--execution-provider", "cuda",
        "--frame-processor", "face_swapper", "face_enhancer"
    ]
    
    # Execute the face swapping command within the roop directory context
    subprocess.run(cmd, cwd=ROOP_DIR)
    
    return output_video_path

def main():
    """
    Main entry point for the Streamlit face swapping app.
    Provides a user interface to upload files and displays the result.
    """
    st.title("Face Swapper App")
    
    # Sidebar for file uploads
    st.sidebar.header("Upload Files")
    image_file = st.sidebar.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    video_file = st.sidebar.file_uploader("Upload Video", type=["mp4"])
    
    # Run face swapping process on button click
    if st.sidebar.button("Swap Faces"):
        if image_file is not None and video_file is not None:
            # Obtain the path to the output video after processing
            generated_video_path = run_script(image_file, video_file)
            
            # Read the generated video and display it in the app
            with open(generated_video_path, "rb") as f:
                video_bytes = f.read()
            st.video(video_bytes)
        else:
            st.error("Please upload both an image and a video file.")

if __name__ == "__main__":
    main()

