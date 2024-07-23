from ..utils.crypto_utils import derive_key, encrypt_data
from ..utils.file_utils import read_file, write_file


def encrypt_file(input_path: str, output_path: str, password: str) -> None:
    data: bytes = read_file(input_path)
    key: bytes = derive_key(password)
    encrypted_data, iv = encrypt_data(data, key)
    # Combine IV and encrypted data
    result: bytes = iv + encrypted_data
    write_file(output_path, result)
