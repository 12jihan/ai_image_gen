import os
from tkinter import Listbox, StringVar, messagebox
from tkinter.font import Font
from typing import ValuesView

# from google.genai import Client
# from google.genai.types import GenerateContentConfig, Modality
from PIL import Image, ImageTk
import tkinter as tk

from dotenv import load_dotenv


# def test(label: tk.Label):
# _label: tk.Label = label
def test(e=None):
    selected_indices = lb.curselection()
    messagebox.showinfo(title="Alert", message="This worked!")
    print(f"this worked\n-\t{e}")


def main():
    load_dotenv()

    cwd: str = os.getcwd()
    dir_list = os.listdir()
    api_key = os.getenv("API_KEY")

    root = tk.Tk()

    root.title("What the fuck bitch")
    root.geometry("800x800")

    test_label = tk.Label(root, text="Testing this shit", font="19")
    test_label.pack(pady=10)

    test_btn = tk.Button(root, text="test", command=test)
    test_btn.pack(pady=10)

    print(cwd)
    print(dir_list)
    choices = tk.Variable(value=dir_list)

    # if dir_list:
    print("works")
    lb = tk.Listbox(root, height=15, listvariable=choices)
    lb.selection_set
    lb.pack()

    try:
        img = Image.open("imgs/generate_image.png")
    except FileNotFoundError as e:
        print(f"There was an error: {e}")
        root.destroy()
        return

    test_image = ImageTk.PhotoImage(img)
    img_label = tk.Label(root, image=test_image)
    img_label.pack()

    root.mainloop()

    # try:
    #     client = Client(api_key=api_key)
    #
    #     prompt = "Create a test image for me"
    #     response = client.models.generate_content(
    #         model="gemini-2.0-flash-preview-image-generation",
    #         contents=prompt,
    #         config=GenerateContentConfig(
    #             response_modalities=[Modality.IMAGE, Modality.TEXT]
    #         ),
    #     )
    #     print("Creating test image...")
    #
    #     if response.parts:
    #         text_part = response.parts[0]
    #         image_part = response.parts[1]
    #         pil_image = image_part.as_image()
    #
    #         if text_part:
    #             print(text_part)
    #         if pil_image:
    #             output_name = "generate_image.png"
    #             pil_image.save(output_name)
    #         else:
    #             print("Can't convert to an image...")
    #
    #         # print(f"response: {response}")
    #
    # except Exception as e:
    #     print(f"Error: {e}")


if __name__ == "__main__":
    main()
