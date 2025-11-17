AI Image & Chat Generator
This is a desktop application built with Python and Tkinter that provides a dual-purpose AI interface. It functions as both a text-based AI chatbot using Google's Gemini models and an AI image generator using Google's Imagen or Gemini 2.5 Flash Image models.

The application features a responsive image gallery that displays generated images and allows you to browse all images in the imgs/ directory.

Features
Dual AI Modes: A checkmark toggles between "Text Generation" and "Image Generation" modes.

AI Chatbot: A familiar chat interface that connects to Google's Gemini API (gemini-1.5-pro or gemini-2.5-flash) for text-based conversations.

AI Image Generation: Generates images from text prompts using the gemini-2.5-flash-image or imagen models.

Image Gallery: A listbox on the right displays all images (PNG, JPG, etc.) found in the imgs/ directory.

Responsive Image Viewer: The image display panel automatically resizes the selected image to fit the window, maintaining its aspect ratio.

Interactive Gallery:

Clicking a filename in the list loads it into the viewer.

Newly generated images are automatically saved to the imgs/ folder, added to the list, and instantly selected and displayed.

Technologies Used
Python 3

Tkinter: For the core GUI.

Pillow (PIL): For opening, resizing, and displaying images.

google-genai: The official Google Python library for the Gemini and Imagen APIs.

python-dotenv: For secure management of the API key.

uv: Used for fast virtual environment and package management.

Setup and Installation
Follow these steps to get the application running on your local machine.

1. Install uv (if you haven't already)
uv is an extremely fast Python package installer and resolver, intended as a drop-in replacement for pip and venv.

Bash

# For macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# For Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
2. Clone the Repository
Bash

git clone https://github.com/12jihan/ai_image_gen.git
cd ai_image_gen
3. Create a Virtual Environment (with uv)
uv combines virtual environment creation and activation in one step.

Bash

# Create and activate a virtual environment named .venv
uv venv
source .venv/bin/activate

# On Windows (PowerShell)
# .\venv\Scripts\Activate.ps1
4. Install Dependencies (with uv)
This will install the packages from a requirements.txt file (if you have one) or you can install them directly.

Bash

# Option A: Install packages directly
uv pip install google-genai pillow python-dotenv

# Option B: If you create a requirements.txt file
# uv pip install -r requirements.txt
5. Set Up Your API Key
Create a file named .env in the root of the project directory.

Open the .env file and add your Google AI Studio API key:

Code snippet

API_KEY="YOUR_GOOGLE_API_KEY_HERE"
6. Create the Image Folder
The application requires an imgs/ folder to exist and contain at least one image to load on startup.

Create the folder:

Bash

mkdir imgs
Add an image to this folder and name it sample_image.png. This is the image the app will load by default.

7. Configure .gitignore
To prevent your generated images from being committed to your repository, your .gitignore file should contain:

Code snippet

# Ignore everything in the imgs/ folder
imgs/*

# BUT, do NOT ignore the default sample_image.png
!imgs/sample_image.png

# Ignore the uv virtual environment
.venv/
How to Run
Once you have completed the setup, run the main script from your terminal:

Bash

python main.py
(Note: Your main script might be named app.py or similar. Adjust the command as needed.)
