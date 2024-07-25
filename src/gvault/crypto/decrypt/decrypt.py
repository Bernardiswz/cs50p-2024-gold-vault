from ..utils.crypto_utils import derive_key, decrypt_data
from ..utils.file_utils import read_file, write_file


__all__ = ["decrypt_file"]


def decrypt_file(input_path: str, output_path: str, password):
    encrypted_data: bytes = read_file(input_path)
    salt: bytes = encrypted_data[:16]
    iv: bytes = encrypted_data[16:32]
    ciphertext: bytes = encrypted_data[32:]
    key = derive_key(password, salt)
    decrypted_data: bytes = decrypt_data(ciphertext, key, iv)
    write_file(output_path, decrypted_data)
