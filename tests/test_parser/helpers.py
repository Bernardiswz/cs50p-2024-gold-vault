from typing import List


class ParseArgsGenerator:
    # Expected format:
    # [script.py] [-e|--encrypt|-d|--decrypt] [input...] [-o|--output] [output...]
    ARGV_TEMPLATE: List[str] = ["script.py",]

    def __init__(self):
        ...

    def get_encrypt_parse_args_params(self) -> List[str]:
        argv_template: List[str] = self.ARGV_TEMPLATE
        short_enc_flag_argv: List[str] = argv_template.append("-e")
        full_enc_flag_argv: List[str] = argv_template.append("--encryption")
        
    def _generate_appended_io_args_list(self, argv: List[str]) -> List[str]:
        return argv.extend(["input_file.py", "-o", "output_file.py"])

