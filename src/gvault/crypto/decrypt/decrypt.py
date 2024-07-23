from ..utils.crypto_utils import derive_key, decrypt_data
from ..utils.file_utils import read_file, write_file


__all__ = ["decrypt_file"]


def decrypt_file(input_path: str, output_path: str, password):
    data: bytes = read_file(input_path)
    key: bytes = derive_key(password)

    # Extract IV and encrypted data
    iv: bytes = data[:16]
    encrypted_data: bytes = data[16:]
    decrypted_data: bytes = decrypt_data(encrypted_data, key, iv)
    write_file(output_path, decrypted_data)
