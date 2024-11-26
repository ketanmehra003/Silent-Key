import os
import argparse
import tempfile
from utils.encrypt import encrypt_file
from utils.decrypt import decrypt_file
from utils.stegano import hide_image, reveal_image
from utils.extreme import process_image

def main_cli(args):
    parser = argparse.ArgumentParser(description='Image Encryption CLI using ChaCha20.')
    subparsers = parser.add_subparsers(dest="command")

    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a file')
    encrypt_parser.add_argument('-i','--input_file', type=str, help='File to encrypt', required=True)
    encrypt_parser.add_argument('-o','--output_file', type=str, help='File name to save/load the encrypted output', required=False, default='encrypted.png')
    encrypt_parser.add_argument('-k','--key_file', type=str, help='File name to save/load the encryption key. Note that file name must be ".bin" extension', required=False, default='key.bin')
    encrypt_parser.add_argument('-c','--cover_file', type=str, help='File to use as the cover image for steganography', required=False, default=None)
    encrypt_parser.add_argument('-e','--extreme', action='store_true', help='Use extreme encryption mode', required=False, default=False)

    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt a file')
    decrypt_parser.add_argument('-i','--input_file', type=str, help='File to decrypt', required=True)
    decrypt_parser.add_argument('-o','--output_file', type=str, help='Output decrypted file', required=False, default='decrypted.png')
    decrypt_parser.add_argument('-k','--key_file', type=str, help='File to load the encryption key', required=True)
    decrypt_parser.add_argument('-r','--reveal_file', action='store_true', help='Extract encrypted image from steganography', required=False)
    decrypt_parser.add_argument('-e','--extreme', action='store_true', help='Use extreme decryption mode', required=False)

    # Hide command
    hide_parser = subparsers.add_parser('hide', help='Hide an image in another image')
    hide_parser.add_argument('-i','--input_file', type=str, help='File to hide', required=True)
    hide_parser.add_argument('-o','--output_file', type=str, help='File name to save the stego image', required=False, default='stego_image.png')
    hide_parser.add_argument('-c','--cover_file', type=str, help='File to use as the cover image for steganography', required=True)

    # Reveal command
    reveal_parser = subparsers.add_parser('reveal', help='Reveal an image from an image')
    reveal_parser.add_argument('-i','--input_file', type=str, help='Stego image file', required=True)
    reveal_parser.add_argument('-o','--output_file', type=str, help='File name to save the extracted file', required=False, default='revealed.png')

    args = parser.parse_args(args)

    # Key file extension check (applies to both encrypt and decrypt commands)
    if args.command in ["encrypt", "decrypt"]:
        if not args.key_file.endswith('.bin'):
            raise ValueError("Key file must have a '.bin' extension")

    if args.command == "encrypt":
        if args.extreme:
            if args.cover_file:
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False, dir='./') as temp_file:
                    temp_filename = temp_file.name
                    process_image(args.input_file, temp_filename, args.key_file, mode='encrypt')
                    hide_image(temp_filename, args.cover_file, args.output_file)
                os.remove(temp_filename)
            else:
                process_image(args.input_file, args.output_file, args.key_file, mode='encrypt')
        else:
            if args.cover_file:
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False, dir='./') as temp_file:
                    temp_filename = temp_file.name
                    encrypt_file(args.input_file, temp_filename, args.key_file)
                    hide_image(temp_filename, args.cover_file, args.output_file)
                os.remove(temp_filename)
            else:
                encrypt_file(args.input_file, args.output_file, args.key_file)
    elif args.command == "decrypt":
        if args.extreme:
            if args.reveal_file:
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False, dir='./') as temp_file:
                    temp_filename = temp_file.name
                    reveal_image(args.input_file, temp_filename)
                    process_image(temp_filename, args.output_file, args.key_file, mode='decrypt')
                os.remove(temp_filename)
            else:
                process_image(args.input_file, args.output_file, args.key_file, mode='decrypt')
        else:
            if args.reveal_file:
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False, dir='./') as temp_file:
                    temp_filename = temp_file.name
                    reveal_image(args.input_file, temp_filename)
                    decrypt_file(temp_filename, args.output_file, args.key_file)
                os.remove(temp_filename)
            else:
                decrypt_file(args.input_file, args.output_file, args.key_file)
    elif args.command == "hide":
        hide_image(args.input_file, args.cover_file, args.output_file)
    elif args.command == "reveal":
        reveal_image(args.input_file, args.output_file)
    else:
        parser.print_help()
