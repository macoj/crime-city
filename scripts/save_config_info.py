from config import OFFENCE_CODES
from lib.helpers import OFFENCE_DICT
from lib.logger import info
import os


def save_offence_info_txt(output_path):
    file_output_path = os.path.join(output_path, 'offence_info.txt')
    filtered_dict = {
        code: OFFENCE_DICT.get(code, "Unknown offence code")
        for code in OFFENCE_CODES
    }

    with open(file_output_path, "w") as f:
        for code, description in filtered_dict.items():
            f.write(f"{code}: {description}\n")

    info(f"Offence information saved to {file_output_path}")
