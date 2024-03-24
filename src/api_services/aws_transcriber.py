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
            LanguageCode=language_code
        )

        logger.info(f"Transcription job started for {audio_file_uri}.")

        while True:
            job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            job_status = job['TranscriptionJob']['TranscriptionJobStatus']
            print(f"Transcription job is {job_status}.")

            if job_status in ['COMPLETED', 'FAILED']:
                print(f"Transcription job {job_status}.")
                break
            time.sleep(5)

        # max_tries = 6
        # while max_tries > 0:
        #     max_tries -= 1

        #     job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        #     logger.info(f"Job {job_name} is {job_status}.")

        #     if job_status in ['COMPLETED', 'FAILED']:
        #         if job_status == 'COMPLETED':
        #             try:
        #                 response = urllib.request.urlopen(job['TranscriptionJob']['Transcript']['TranscriptFileUri'])
        #                 data = json.loads(response.read())
        #                 text = data['results']['transcripts'][0]['transcript']
        #                 logger.info("========== below is output of speech-to-text ========================")
        #                 logger.info(text)
        #                 logger.info(
        #                     "=====================================================================")
        #                 return text
        #             except Exception as e:
        #                 logger.info(f"Error retrieving transcript: {e}")
        #                 return "Error retrieving transcript."
        #         else:
        #             logger.info(
        #                 f"Transcription job failed. Check AWS Transcribe logs for details.")
        #             return "Transcription job failed."
        #     else:
        #         logger.info(
        #             f"Waiting for {job_name}. Current status is {job_status}.")
        #         time.sleep(10)

    except Exception as e:
        logger.info(f"Error during transcription: {e}")
        return "Error during transcription."
