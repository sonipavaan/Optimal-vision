# Azure OCR to Speech App

A Python web application that extracts text from images using Azure OCR and converts the extracted text into speech using Azure Speech Services.

Built with:

- Azure Computer Vision API
- Azure Speech Service
- Gradio UI
- Python

---

# Features

- Upload image files
- Extract text using OCR
- Convert extracted text to speech
- Play generated audio directly in browser
- Simple Gradio web interface

---

# Technologies Used

- Python
- Gradio
- Azure Computer Vision
- Azure Speech SDK
- Pillow (PIL)

---

# Project Structure

```text
project/
│
├── app.py
├── requirements.txt
├── README.md
└── output_audio.wav
```

---

# Installation

## 1. Clone Project

```bash
git clone <your-repository-url>
cd <project-folder>
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install azure-cognitiveservices-vision-computervision
pip install azure-cognitiveservices-speech
pip install msrest
pip install gradio
pip install pillow
```

---

# Azure Configuration

Create the following Azure resources:

## 1. Computer Vision Resource

Get:

- Endpoint
- API Key

## 2. Speech Service Resource

Get:

- Speech Key
- Speech Region

---

# Environment Variables (Recommended)

Create a `.env` file:

```env
ENDPOINT=YOUR_AZURE_ENDPOINT
API_KEY=YOUR_COMPUTER_VISION_KEY
SPEECH_KEY=YOUR_SPEECH_KEY
SPEECH_REGION=eastus
```

---


# Running the Application

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:7860
```

---

# Supported Image Formats

- PNG
- JPG
- JPEG
- BMP

---

# Example Workflow

1. Upload image
2. OCR extracts text
3. Text appears in textbox
4. Audio speech generated automatically

---

# Example Use Cases

- Reading scanned documents
- Voice assistance
- Accessibility applications
- AI document readers
- Smart OCR systems

---

# Security Warning

Never expose:

- Azure API keys
- Speech keys
- Endpoints

Use environment variables or `.env` files.

---

# Future Improvements

- Multi-language OCR
- PDF support
- Real-time camera OCR
- Voice selection
- Download speech button
- Dark mode UI

---

# License

MIT License
