import os
import numpy as np
from PIL import Image
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

def encrypt_data(data, nonce, key_file):
    key = os.urandom(32)
    with open(key_file, 'ab') as kf:
        kf.write(key)
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data)
    return encrypted_data

def decrypt_data(data, nonce, key):
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(data)
    return decrypted_data

def process_image(image_path, output_path, key_file, mode='encrypt'):
    # Open the image
    img = Image.open(image_path)
    width, height = img.size

    # Convert image to numpy array
    img_array = np.array(img)

    # Calculate quadrant dimensions
    half_width, half_height = width // 2, height // 2

    # Split the image into quadrants
    quadrants = [
        img_array[:half_height, :half_width],
        img_array[:half_height, half_width:],
        img_array[half_height:, :half_width],
        img_array[half_height:, half_width:]
    ]

    # Process each quadrant
    processed_quadrants = []
    if mode == 'encrypt':
        nonce = os.urandom(16)
        for quadrant in quadrants:
            flat_quadrant = quadrant.tobytes()
            processed_data = encrypt_data(flat_quadrant, nonce, key_file)
            processed_quadrant = np.frombuffer(processed_data, dtype=quadrant.dtype).reshape(quadrant.shape)
            processed_quadrants.append(processed_quadrant)
        with open(key_file, 'ab') as kf:
            kf.write(nonce)
    elif mode == 'decrypt':
        with open(key_file, 'rb') as kf:
            kf.seek(-16, 2)
            nonce = kf.read(16)
            kf.seek(0)
            for quadrant in quadrants:
                key = kf.read(32)
                flat_quadrant = quadrant.tobytes()
                processed_data = decrypt_data(flat_quadrant, nonce, key)
                processed_quadrant = np.frombuffer(processed_data, dtype=quadrant.dtype).reshape(quadrant.shape)
                processed_quadrants.append(processed_quadrant)

    # Reassemble the processed quadrants
    top = np.concatenate((processed_quadrants[0], processed_quadrants[1]), axis=1)
    bottom = np.concatenate((processed_quadrants[2], processed_quadrants[3]), axis=1)
    processed_img_array = np.concatenate((top, bottom), axis=0)

    # Create a new image from the processed array
    processed_img = Image.fromarray(processed_img_array)

    # Save the processed image
    processed_img.save(output_path)
