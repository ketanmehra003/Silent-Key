import numpy as np
from PIL import Image

def hide_image(encrypted_image_file, cover_image_file, output_file):
    # Load the encrypted image (the one to hide)
    encrypted_image = Image.open(encrypted_image_file)
    encrypted_data = np.array(encrypted_image)  # Convert to numpy array
    width, height = encrypted_image.size
    mode = encrypted_image.mode

    # Load the cover image (the one that will hide the encrypted image)
    cover_image = Image.open(cover_image_file)
    cover_data = np.array(cover_image)  # Convert to numpy array

    # Ensure the cover image is large enough to hide the encrypted image
    if encrypted_data.shape[0] > cover_data.shape[0] or encrypted_data.shape[1] > cover_data.shape[1]:
        raise ValueError("The cover image is too small to hide the encrypted image.")

    # Flatten the data to make it easier to work with bitwise operations
    encrypted_flat = encrypted_data.flatten()
    cover_flat = cover_data.flatten()

    # Hide the width, height, and mode of the encrypted image in the first pixels (header)
    header = [width, height, len(mode)]  # Store the width, height, and mode length
    header_bin = ''.join(f'{x:016b}' for x in header)  # Convert to binary string, 16 bits each for width and height

    # Hide the header in the first few pixels
    for i in range(len(header_bin)):
        cover_flat[i] = (cover_flat[i] & 0b11111110) | int(header_bin[i])  # Store header bits in LSB

    # Hide the encrypted image data in the cover image by storing 4 bits of the encrypted image per LSB of the cover
    for i in range(len(encrypted_flat)):
        # Take the first four bits from the encrypted image pixel and hide them in the cover image LSBs
        cover_flat[len(header_bin) + i] = (cover_flat[len(header_bin) + i] & 0b11110000) | (encrypted_flat[i] >> 4)

    # Reshape the cover data back into the original image dimensions
    stego_data = cover_flat.reshape(cover_data.shape)

    # Convert the stego data back into an image and save it
    stego_image = Image.fromarray(stego_data.astype('uint8'))
    stego_image.save(output_file)

    print(f"Steganography complete! Encrypted image hidden in {output_file}.")


def reveal_image(stego_image_file, revealed_output_file):
    # Load the stego image (the cover image with the hidden data)
    stego_image = Image.open(stego_image_file)
    stego_data = np.array(stego_image)  # Convert to numpy array

    # Flatten the data for easier manipulation
    stego_flat = stego_data.flatten()

    # Extract the header to get the width, height, and mode length
    header_bin = ''.join(str((stego_flat[i] & 1)) for i in range(48))  # First 48 bits (16 bits * 3 values)
    width = int(header_bin[:16], 2)
    height = int(header_bin[16:32], 2)
    mode_len = int(header_bin[32:48], 2)

    # Determine the mode of the encrypted image
    mode = 'RGB'[:mode_len]  # Use mode length to determine RGB, RGBA, etc.

    # Calculate the size of the encrypted image data
    encrypted_size = width * height * mode_len

    # Create an array to store the extracted encrypted image data
    extracted_flat = np.zeros(encrypted_size, dtype=np.uint8)

    # Extract the hidden bits from the LSB of the cover image (after the header)
    for i in range(encrypted_size):
        # Reconstruct the original pixel value by retrieving the four bits hidden in the LSB
        extracted_flat[i] = (stego_flat[48 + i] & 0b00001111) << 4  # Reconstruct pixel value by left shifting

    # Reshape the extracted data to match the original encrypted image's dimensions
    extracted_data = extracted_flat.reshape((height, width, mode_len))

    # Convert the extracted data back into an image and save it
    extracted_image = Image.fromarray(extracted_data, mode=mode)
    extracted_image.save(revealed_output_file)

    print(f"Hidden image revealed! Decrypted image saved as {revealed_output_file}.")
