# Silent Key

A command-line tool designed to provide multi-layered image security by combining advanced encryption (ChaCha20) and custom steganography techniques. This project enables secure image transmission and storage, making it ideal for use cases in defense, privacy protection, and digital content management.  

---

## **Features**  
- **Image Encryption**: Secure images using ChaCha20 encryption, resulting in an encrypted image and a key file.  
- **Image Decryption**: Decrypt images with the corresponding key file to restore the original image.  
- **Steganography**: Hide an image within another using a custom LSB-based embedding algorithm.  
- **Extreme Encryption Mode**:  
  - Divide images into quadrants and encrypt each with a unique key.  
  - Reassemble encrypted quadrants into a single image with a consolidated key file.  

---

## **Use Cases**  
- **High-Security Environments**: Protect sensitive images during transmission or storage in military and defense scenarios.  
- **Privacy Advocates**: Secure personal data from unauthorized access.  
- **Content Creators**: Protect intellectual property from theft or misuse.  

---

## **Installation**  
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/hybrid-image-security-tool.git
   cd hybrid-image-security-tool
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## **Usage**
### **Encrypt an Image**
   Apply plain encryption
   ```bash
   python tool.py encrypt --input_file <input_image> --output_file <output_image> --key_file <key_file>
   ```

   Use hybrid function of encryption and steganography
   ```bash
   python tool.py encrypt --input_file <input_image> --output_file <output_image> --key_file <key_file> --cover_file <cover_image>
   ```

   Use extreme encryption
   ```bash
   python tool.py encrypt --input_file <input_image> --output_file <output_image> --key_file <key_file> --extreme
   ```

### **Decrypt an Image**
   For plain decryption
   ```bash
   python tool.py decrypt --input_file <encrypted_image> --output_file <decrypted_image> --key_file <key_file>
   ```

   For hybrid encrypted images
   ```bash
   python tool.py decrypt --input_file <encrypted_image> --output_file <decrypted_image> --key_file <key_file> --reveal_file
   ```

   For extreme encrypted images
   ```bash
   python tool.py decrypt --input_file <encrypted_image> --output_file <decrypted_image> --key_file <key_file> --extreme
   ```

### **Steganography (Hide an Image)**
   ```bash
   python tool.py hide --cover_file <cover_image> --input_file <image_to_hide> --output_file <output_image>
   ```

### **Steganography (Reveal an Image)**
   ```bash
   python tool.py reveal --input_file <image_to_hide> --output_file <output_image>
   ```

## **Dependencies**
- **Python Libraries:**
  - Pillow: For image handling.
  - Numpy: For efficient computations.
  - Cryptography: For ChaCha20 encryption.
  - argparse: For command-line argument parsing.
