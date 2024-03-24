import boto3
from src.utility.local_loger import logger
from src.api_services.credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, TRANSCRIBE_REGION


def get_Transcript(audio_file, job_name='crtvtask',
                   language_code='en-US', format='mp3',
                   aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, transcribe_region=TRANSCRIBE_REGION) -> str:
    """This function is used to get the transcript of the audio file using AWS Transcribe.

    Args:
        audio_file (str): Path to the audio file.
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
        logger.info(f"Transcribing audio file: {audio_file.split('/')[-1]}")
        logger.info(f"Job name: {job_name}")

        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            MediaFormat=audio_file.split('/').split('.')[-1],
            LanguageCode=language_code,  # e.g., 'en-US'
            Media=dict(AudioFile=audio_file.read()),
            format=format)

        # Waiting for the transcription job to complete
        waiter = transcribe_client.get_waiter('transcription_job_completed')
        waiter.wait(TranscriptionJobName=job_name)

        # transcription results
        transcription_job = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name)
        transcript = transcription_job['Transcript']['Transcript']
        logger.info("Transcription job completed successfully.")

        return transcript
    except Exception as e:
        logger.error(
            f"Error occured during getting transcript from AWS Transcribe. {e.__str__()}")
        return "Error occured during getting transcript from AWS Transcribe."
