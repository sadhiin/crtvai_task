import os
from src.utility.local_loger import logger
import subprocess

def convert_audio(input_file, output_file):
    """
    Converts an audio file from one format to another using FFmpeg.

    Args:
        input_file: Path to the input audio file (including extension).
        output_file: Path to the desired output file (including extension).

        """
    try:
        logger.info(f"Converting audio file: {input_file} -> {output_file}")

        command = "ffmpeg -i {} -acodec libmp3lame -ab 128k {}".format(input_file, output_file)

        subprocess.run(command, check=True)

    except Exception as e:
        logger.error(f"Error during conversion audio file.: {e}")


def delete_file(file_path):
    """This function is used to delete a file from the system.

    Args:
        file_path (str): Path of the file to be deleted.

    Returns:
        bool: Returns True if file is deleted successfully, else False.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        logger.error(f"Error occured during deleting file. {e.__str__()}")
