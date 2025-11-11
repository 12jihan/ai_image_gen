import os
from tkinter import Event, Listbox, StringVar, messagebox, ttk
from tkinter.font import Font
from typing import ValuesView, cast

from google.genai import Client
from google.genai.types import GenerateContentConfig, Modality
from PIL import Image, ImageTk
import tkinter as tk

from dotenv import load_dotenv


# def test(label: tk.Label):
# _label: tk.Label = label


def main():
    load_dotenv()

    cwd: str = os.getcwd()
    dir_list: list[str] = os.listdir("./imgs")
    api_key: str | None = os.getenv("API_KEY")

    current: str | None = None

    def generateImage():
        try:
            client = Client(api_key=api_key)

            prompt = "Create a sample image for me"
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
                    output_name = "sample_image.png"
                    pil_image.save(output_name)
                else:
                    print("Can't convert to an image...")

                # print(f"response: {response}")

        except Exception as e:
            print(f"Error: {e}")

    def openImage():
        try:
            img = Image.open("imgs/sample_image.png")
        except FileNotFoundError as e:
            print(f"There was an error: {e}")
            # root.destroy()
            return

    def test(e: tk.Event):
        """
        Calls an external Python script when an item is selected.
        """
        listbox = cast(tk.Listbox, e.widget)
        selected_indices = listbox.curselection()

        if selected_indices:
            index = selected_indices[0]
            value = listbox.get(index)
            print(f"value: {value}")

        # selected_indices = lb.curselection()
        # print(f"this worked\n{dir(e)}")
        # print(f"this worked\n{e.state}")

    def button_test():
        print("clicked")
        # generateImage()

    root = tk.Tk()
    root.title("Image Generator")
    root.geometry("800x400")

    lfrm = ttk.Frame(root, relief="solid", borderwidth=2)
    lfrm.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    rfrm = ttk.Frame(root, relief="solid", borderwidth=2)
    rfrm.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    txt_frm = ttk.Frame(lfrm, relief="solid", borderwidth=2)
    test_input = tk.Text(
        width=40, height=10, wrap="word", yscrollcommand=ttk.Scrollbar()
    )
    test_btn0 = ttk.Button(lfrm, text="refresh", command=button_test)
    test_btn0.grid(row=1, column=0)

    # print(cwd)
    # print(dir_list)
    choices = tk.Variable(value=dir_list)
    # if dir_list:
    lb = tk.Listbox(rfrm, listvariable=choices)
    lb.bind("<<ListboxSelect>>", test)
    # lb.selection_set
    lb.pack()

    # print("works")

    # test_image = ImageTk.PhotoImage(img)
    # img_label = tk.Label(root, image=test_image)
    # img_label.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
