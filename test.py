from src.api_services.aws_transcriber import get_transcribe

url = "s3://shan-arabic-audio-bucket/E_Projects_MLOPS_crtvai_task_client_uploads_audios_WhatsApp_Audio_2024-03-17_at_15.55.02.mp3"


get_transcribe(url, job_name='crtvtask', language_code='ar-SA', media_format='mp3')