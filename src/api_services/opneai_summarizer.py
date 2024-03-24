import openai
from src.utility.local_loger import logger
from src.api_services.credentials import OPNEAI_API_KEY


def get_summary(transcript):
    """This function is used to get the summary of the transcript using OpenAI API.

    Args:
        transcript (str): Text transcript for which summary is required.

    Returns:
        str: Returns the summary of the transcript.
    """

    openai.api_key = OPNEAI_API_KEY

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-instruct",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
                },
                {
                    "role": "user",
                    "content": transcript
                }
            ],
            max_tokens=256,
            frequency_penalty=0,
            presence_penalty=0
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        logger.error(
            f"Error occured during geting summary from Openai. {e.__str__()}")
        return "Error occured during geting summary from Openai."
