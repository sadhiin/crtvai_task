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
                    "content": "أنا ذكاء اصطناعي ماهر للغاية مدرب على فهم اللغة والتلخيص. أريد منك قراءة النص التالي وتلخيصه في فقرة مجردة موجزة. هدفنا هو الحفاظ على أهم النقاط ، مع توفير ملخص متماسك وقابل للقراءة يمكن أن يساعد الشخص على فهم النقاط الرئيسية للمناقشة دون الحاجة إلى قراءة النص بأكمله. يرجى تجنب التفاصيل غير الضرورية أو النقاط التماسية."
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
            f"Error occured during geting summary from Openai. {e}")
        return "Error occured during geting summary from Openai."
