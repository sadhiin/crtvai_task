import subprocess
import json
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for
from src.utility.local_loger import logger
from src.utility.file_handler import convert_audio, delete_file
from src.api_services.aws_transcriber import get_Transcript
from src.api_services.aws_s3_bucket import upload_audio_file_to_s3, get_latest_file_upload
from src.api_services.opneai_summarizer import get_summary

UPLOAD_FOLDER = './client_uploads/audios/'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'm4a','webm', 'ogg', 'amr', 'wma', 'aac', 'aiff', 'aif', 'aifc', 'caf', 'm4r', '3gp', '3g2', 'm4p', 'm4b', 'm4r', 'm4v', 'mov', 'qt', 'avi', 'wmv', 'asf', 'flv', 'swf', 'mkv', 'mpg', 'mpeg', 'ts', 'vob', 'webm', 'hevc', 'heic'}

PORT = 5000
HOST = '0.0.0.0'
DEBUG = True

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def upload_file():
    return render_template('home.html')

@app.route("/", methods=['POST'])
def transcribe_and_summarize():

    if request.method == 'POST':
        if 'audio_file' not in request.files:
            logger.error('No file uploaded')
            return redirect(request.url)

        uploaded_file = request.files['audio_file']
        if uploaded_file.filename == '':
            logger.error('No selected file.')
            return redirect(request.url)

        if uploaded_file and allowed_file(uploaded_file.filename):
            uploaded_file.save(app.config['UPLOAD_FOLDER'] + uploaded_file.filename)

            file_path = app.config['UPLOAD_FOLDER'] + uploaded_file.filename
            logger.info(f"File uploaded successfully. {uploaded_file.filename}")

            # converting the audio file to .mp3 format
            input_file_path = file_path
            input_file = input_file_path.split("/")[-1]
            output_file = "converted_audio.mp3"
            output_file_path = app.config['UPLOAD_FOLDER'] + input_file.split(".")[0] + ".mp3"
            output_format = "mp3"

            try:
                convert_audio(input_file_path, output_file_path, output_format)
                logger.info(f"Audio converted successfully: {input_file} -> {output_file}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Error during conversion audio file.: {e}")

            # saving file to the S3 bucket
            upload_audio_file_to_s3(output_file_path, output_file)
            logger.info(f"File uploaded to S3 bucket successfully. {output_file}")

            last_file = get_latest_file_upload()


            # Get the transcript of the audio file
            transcript = get_Transcript(audio_file=last_file, language_code="en-US")
            logger.info("Transcript generated successfully.")

            # Delete the audio file from the system
            delete_file(output_file_path)
            
            # Get the summary of the transcript
            logger.info("Getting summary of the transcript.")
            summary = get_summary(transcript)
            logger.info("Summary generated successfully.")
            return render_template('summary.html', transcript=transcript, summary=summary)
    else:
        return render_template('home.html')


if __name__=="__main__":
    logger.info("Application running.")
    app.run(host=HOST, port=PORT, debug=DEBUG)