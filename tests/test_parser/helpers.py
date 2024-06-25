from typing import Dict, List, Tuple


class ParseArgsGenerator:
    @staticmethod
    def get_encrypt_parse_args_params() -> Tuple[List[str], Dict[str, bool]]:
        argv_short_enc_flag: List[str] = ["script.py", "-e", "file.py", "-o", "output_file.py"]
        argv_full_enc_flag: List[str] = ["script.py", "--encrypt", "file.py", "-o", "output_file.py"]
        expected_enc_attr: Dict[str, bool] = {"encrypt": True}
        return [(argv_short_enc_flag, expected_enc_attr), (argv_full_enc_flag, expected_enc_attr)]

    @staticmethod
    def get_decrypt_parse_args_params() -> Tuple[List[str], Dict[str, bool]]:
        argv_short_dec_flag: List[str] = ["script.py", "-d", "file.py", "-o", "output_file.py"]
        argv_full_dec_flag: List[str] = ["script.py", "--decrypt", "file.py", "-o", "output_file.py"]
        expected_dec_attr: Dict[str, bool] = {"decrypt": True}
        return [(argv_short_dec_flag, expected_dec_attr), (argv_full_dec_flag, expected_dec_attr)]

