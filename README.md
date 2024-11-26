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
   ```bash
   python tool.py --encrypt --input <input_image> --output <output_image> --keyfile <key_file>
   ```
