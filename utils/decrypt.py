from PIL import Image
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

def decrypt_file(encrypted_file, output_file, key_file):
    # Load the encrypted image
    encrypted_image = Image.open(encrypted_file)
    encrypted_data = encrypted_image.tobytes()  # Extract pixel data
    width, height = encrypted_image.size
    mode = encrypted_image.mode

    # Load the ChaCha20 key and nonce from the file
    with open(key_file, 'rb') as kf:
        key = kf.read(32)  # First 32 bytes for the key
        nonce = kf.read(16)  # Next 16 bytes for the nonce

    # Initialize ChaCha20 decryption
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data)

    # Create an image from the decrypted data
    decrypted_image = Image.frombytes(mode, (width, height), decrypted_data)

    # Save the decrypted image
    decrypted_image.save(output_file)

    print(f"Decryption complete! Decrypted file saved as {output_file}.")