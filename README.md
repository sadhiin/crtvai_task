# **Project Name: Crtvai-Task Audio Transcribe and Summarizer**

This Flask application allows users to upload audio files, transcribe them to text, and get a summary of the transcript.

## Project Structure

```
.
├── app.py                   # Main Flask application file
├── README.md                # This file (instructions)
├── src/
│   ├── __init__.py           # Empty file to mark directory as a package
│   ├── api_services/
│   │   ├── aws_s3_bucket.py  # Functions for interacting with AWS S3 bucket
│   │   ├── aws_transcriber.py # Functions for interacting with AWS Transcribe
│   │   └── opneai_summarizer.py# Functions for interacting with OpenAI Summarizer
│   └── utility/
│       ├── file_handler.py    # Functions for file conversion and deletion
│       └── local_loger.py     # Simple logging utility
├── client_uploads/          # Folder to store uploaded audio files (created on startup)
└── templates/
    └── home.html            # User interface for uploading audio
    └── summary.html         # Template to display transcript and summary
```

## Requirements

- Python 3.x ([https://www.python.org/downloads/](https://www.python.org/downloads/))
- Flask ([https://flask.palletsprojects.com/](https://flask.palletsprojects.com/))
- boto3 (for AWS interaction) - `pip install boto3`
- Additional libraries based on your specific implementations of `convert_audio`, `get_transcribe`, and `get_summary` (check their documentation for installation instructions)

## Configuration

- Update the following settings in `app.py`:
    - `UPLOAD_FOLDER`: Path to the folder where uploaded audio files will be stored.
    - `ALLOWED_EXTENSIONS`: Set of allowed audio file extensions.
    - AWS credentials (if using AWS services): Configure your AWS credentials using environment variables or a configuration file (refer to boto3 documentation).

## Running the Application

1. Install required libraries (`pip install -r requirements.txt` if you have a requirements.txt file listing dependencies).
- **Note:** To converting the given audio files in acceptable format by AWS-Trasncriber [ffmpeg](https://www.ffmpeg.org/) is required.
2. Run the application using: `python app.py`
3. Access the application in your web browser at `http://localhost:5000/` (default port).

## Usage

1. Upload an audio file (supported formats: mp3, wav, etc.).
2. Click "Upload".
3. The application will transcribe the audio and summarize the transcript.
4. The transcript and summary will be displayed on the screen.

