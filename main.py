import os
from dotenv import load_dotenv
from google.genai import Client
from google.genai.types import GenerateContentConfig, Modality
from PIL import Image


def main():
    load_dotenv()
    # print("Hello from aiimage!")
    api_key = os.getenv("API_KEY")
    print("api_key")
    print(api_key)

    try:
        client = Client(api_key=api_key)

        prompt = "Create a test image for me"
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=GenerateContentConfig(
                response_modalities=[Modality.IMAGE, Modality.TEXT]
            ),
        )
        print("Creating test image...")

        if response.parts:
            text_part = response.parts[0]
            image_part = response.parts[1]
            pil_image = image_part.as_image()

            if text_part:
                print(text_part)
            if pil_image:
                output_name = "generate_image.png"
                pil_image.save(output_name)
            else:
                print("Can't convert to an image...")

            # print(f"response: {response}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
