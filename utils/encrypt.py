import os
from PIL import Image
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

def generate_key():
    return os.urandom(32)  # 256-bit key for ChaCha20

def encrypt_file(input_file, output_file, key_file):
    # Load the image
    image = Image.open(input_file)
    image_data = image.tobytes()  # Extract pixel data
    width, height = image.size
    mode = image.mode

    # Generate a random nonce for ChaCha20
    nonce = os.urandom(16)

    # Generate the ChaCha20 key
    key = generate_key()

    # Save the key to a file (for decryption later)
    with open(key_file, 'wb') as kf:
        kf.write(key)
        kf.write(nonce)

    # Initialize ChaCha20 encryption
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(image_data)

    # Combine the encrypted data with the original image header
    encrypted_image = Image.frombytes(mode, (width, height), encrypted_data)

    # Save the encrypted image
    encrypted_image.save(output_file)

    print(f"Encryption complete! Encrypted file saved as {output_file}. Key saved as {key_file}.")
