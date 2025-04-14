# LSB Steganography Tool

A simple yet powerful tool for hiding **secret messages** inside images using **Least Significant Bit (LSB) steganography**. This application is built using **Flask** and includes robust features such as **AES encryption**, optional authentication, and guest access with limitations.

---

## Features
- **Image encoding:** Hide text data inside images securely using LSB steganography.
- **Image decoding:** Retrieve hidden data from encoded images.
- **AES Encryption:** Encrypt the secret message before embedding it into the image, offering an additional layer of security.
- **Authentication:**
  - Supports both authenticated and guest access.
  - Guest users are limited in their usage and can decode or encode images a **limited number of times**.
- **Web-based User Interface (UI):** A simple front-end to interact with the tool.
- **Error handling:** Handles invalid input, corrupted images, or insufficient permissions gracefully.

---

## How It Works

### 1. **Encoding Process**
A user uploads an image and provides:
- **Text**: The secret message to be hidden.
- **Encryption Key**: A key to encrypt the secret message.
  
The system encrypts the message using AES, encodes it into the image with LSB steganography, and then provides the user with the resultant image.

### 2. **Decoding Process**
A user uploads an **encoded image** file and provides:
- **Decryption Key**: The encryption key used during encoding.
  
The system extracts the hidden data using LSB decoding and decrypts it using the provided key to reveal the original text.

---

## API Endpoints

### **POST** `/api/lsb_stego/encode`
#### Description:
Encodes a secret message into an image.

#### Parameters:
- **image** (File): The image to encode the message into.
- **text** (String): The message to hide.
- **key** (String): The encryption key for securing the message.

#### Response:
- On success: Encoded image as a downloadable `.jpg` file.
- On failure: JSON response with an error message.

---

### **POST** `/api/lsb_stego/decode`
#### Description:
Decodes the secret message from an encoded image.

#### Parameters:
- **image** (File): The encoded image file.
- **key** (String): The decryption key used for the original message.

#### Response:
- On success: The decoded secret message.
- On failure: JSON response with an error message.

---

## Key Modules and Functions

### **Blueprint:** `image_handling.py`
Handles all image-related routes for encoding and decoding messages.

- **`/api/lsb_stego/encode:`**
  - Validates input.
  - Encrypts the message using AES.
  - Encodes the encrypted data into the image using LSB steganography.

- **`/api/lsb_stego/decode:`**
  - Extracts the hidden data using LSB decoding.
  - Decrypts the data with AES using the provided key.

### **Utility Functions:**
- **Guest Access Handling:** Limits unauthenticated users by tracking their usage through tokens and browser fingerprinting.
- **Error Handling:** Verifies files, catches invalid inputs, and handles corrupted/unsupported image formats.

---

## Technologies Used
- **Backend:**
  - Flask
- **Image Processing:**
  - OpenCV
  - NumPy
  - PIL (Pillow)
- **Encryption:**
  - AES (Advanced Encryption Standard)
- **Frontend:**
  - HTML
  - CSS (with responsive design)
  - JavaScript (for dynamic UI)

---

## Requirements
To run the project locally, ensure that the following are installed:
- Python 3.12 or higher.
- The following Python packages:
  ```bash
  pip install flask flask-jwt-extended numpy opencv-python pillow
  ```
- Browser to access the web-based UI.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/me-athxrva/steganography-project.git
   cd steganography-project
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application:**
   ```bash
   python app.py
   ```

5. Open your browser and visit `http://127.0.0.1:5000`.

---

## Usage

1. **Encode a message:**
   - Upload your image.
   - Enter the secret text and an encryption key.
   - Download the encoded image.

2. **Decode a message:**
   - Upload the encoded image.
   - Provide the encryption key.
   - Retrieve the hidden text.

---

## Contact
[Atharva Deore](https://atharvadeore.me)


