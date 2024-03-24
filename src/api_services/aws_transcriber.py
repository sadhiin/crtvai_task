import json
import urllib.request
import time
import boto3
from src.utility.local_loger import logger
from src.api_services.credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, TRANSCRIBE_REGION


def get_transcribe(audio_file_uri, job_name='crtvtask',
                   language_code='en-US', media_format='mp3',
                   aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, transcribe_region=TRANSCRIBE_REGION) -> str:
    """This function is used to get the transcript of the audio file using AWS Transcribe.

    Args:
        audio_file_uri (str): Path to the audio file.
        job_name (str): Name of the transcription job.
        language_code (str): Language code of the audio file.
        format (str): Format of the audio file.
        aws_access_key_id (str): AWS Access Key ID.
        aws_secret_access_key (str): AWS Secret Access Key.

    Returns:
        transcribe (str): Returns the transcript of the audio file.
    """
    try:
        # Transcribe the audio file using AWS Transcribe
        transcribe_client = boto3.client('transcribe',
                                         aws_access_key_id=aws_access_key_id,
                                         aws_secret_access_key=aws_secret_access_key,
                                         region_name=transcribe_region)

        job_name = f'{job_name}_{time.time()}'
        logger.info(f"Job name: {job_name}")

        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': audio_file_uri},
            MediaFormat='mp3',
            LanguageCode=language_code,
            MediaSampleRateHertz=16000)

        logger.info(f"Transcription job started for {audio_file_uri}.")

        while True:
            job = transcribe_client.get_transcription_job(
                TranscriptionJobName=job_name)
            job_status = job['TranscriptionJob']['TranscriptionJobStatus']
            logger.info(f"Transcription job is {job_status}.")

            if job_status in ['COMPLETED', 'FAILED']:
                logger.info(f"Transcription job {job_status}.")
                try:
                    trans_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
                    response = urllib.request.urlopen(trans_uri)
                    data = json.loads(response.read())
                    text = data['results']['transcripts'][0]['transcript']
                    logger.info("========== below is output of speech-to-text ========================\n due to arabic language, it may not be shown in log file properly. \n=====================================================================")
                    logger.info(text)
                    logger.info("=====================================================================")
                    return text
                except Exception as e:
                    logger.info(f"Error retrieving transcript: {e}")
                    return "Error retrieving transcript, although it's completed."

            time.sleep(5)

    except Exception as e:
        logger.info(f"Error during transcription: {e}")
        return "Error during transcription."
