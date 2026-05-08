import azure.cognitiveservices.vision.computervision as computervision
from msrest.authentication import CognitiveServicesCredentials
import azure.cognitiveservices.speech as speechsdk
import gradio as gr
import os
import time
from PIL import Image

from dotenv import load_dotenv
import os

load_dotenv()

ENDPOINT = os.getenv("ENDPOINT")
API_KEY = os.getenv("API_KEY")
SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")

# -----------------------------
# CREATE CLIENT
# -----------------------------
client = computervision.ComputerVisionClient(
    ENDPOINT,
    CognitiveServicesCredentials(API_KEY)
)

# ----------------------------------------
# 2. Text-to-Speech Function
# ----------------------------------------
def text_to_speech(line, output_file="output_audio.wav"):
    # Configuration with your Azure key + region
    speech_config = speechsdk.SpeechConfig(
        subscription=SPEECH_KEY,
        region=SPEECH_REGION
    )

    # Choose neural voice (you can change it)
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    # Output audio configuration
    audio_config = speechsdk.audio.AudioConfig(filename=output_file)

    # Create synthesizer
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    # Convert text → speech
    result = synthesizer.speak_text_async(line).get()

    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Audio saved successfully as: {output_file}")
    else:
        print("Speech synthesis failed.")
        print("Reason:", result.reason)

def process_image_and_speak(image_input):
    if image_input is None:
        return "Please upload an image.", None

    # Save the uploaded image temporarily
    input_image_path = "uploaded_image.png"
    Image.fromarray(image_input).save(input_image_path)

    try:
        # --- OCR part ---
        with open(input_image_path, "rb") as image_file:
            read_response = client.read_in_stream(image_file, raw=True)

        operation_id = read_response.headers["Operation-Location"].split("/")[-1]

        while True:
            result_ocr = client.get_read_result(operation_id)
            if result_ocr.status not in ["notStarted", "running"]:
                break
            time.sleep(1)

        combined_text = ""
        if result_ocr.status == "succeeded":
            for page in result_ocr.analyze_result.read_results:
                for line_obj in page.lines:
                    combined_text += line_obj.text + "\n"

            if combined_text:
                # --- Text-to-Speech part ---
                output_audio_file = "gradio_output_audio.wav"
                text_to_speech(combined_text.strip(), output_file=output_audio_file)

                return combined_text, output_audio_file
            else:
                return "OCR successful, but no text found.", None
        else:
            return f"OCR failed with status: {result_ocr.status}", None

    except Exception as e:
        return f"An error occurred: {e}", None

# Gradio Interface
iface = gr.Interface(
    fn=process_image_and_speak,
    inputs=gr.Image(type="numpy", label="Upload Image"),
    outputs=[
        gr.Textbox(label="Extracted Text"),
        gr.Audio(label="Generated Speech", type="filepath")
    ],
    title="Image OCR to Speech",
    description="Upload an image, and this app will extract text using Azure OCR and convert it to speech."
)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7860))
    iface.launch(server_name="0.0.0.0", server_port=port)
