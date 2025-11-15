from logging import disable
import os
from tkinter import BOTH, EW, LEFT, Event, Listbox, StringVar, messagebox, ttk, font
from tkinter.font import Font
from typing import ValuesView, cast

from google.genai import Client
from google.genai.types import GenerateContentConfig, Modality
from PIL import Image, ImageTk
import tkinter as tk
import uuid

from dotenv import load_dotenv


# def test(label: tk.Label):
# _label: tk.Label = label


def main():
    load_dotenv()

    cwd: str = os.getcwd()
    dir_list: list[str] = os.listdir("./imgs")
    api_key: str | None = os.getenv("API_KEY")
    chat_history_context: list = []
    current: str | None = None
    img = "./imgs/sample_image.png"

    # Functions:
    def generateImage(message: str, history_list: list):
        prompt: str = message
        contents = history_list
        print(f"contents: {contents}")
        try:
            client: Client = Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=str(contents),
                config=GenerateContentConfig(
                    response_modalities=[Modality.IMAGE, Modality.TEXT]
                ),
            )
            print("Creating image...")
            print(response)
            if response.parts:
                print(len(response.parts))
                if len(response.parts) > 0:
                    text_part = response.parts[0].text
                    print(f"ai text: {text_part}")
                    print(text_part)
                    add_to_history(str(text_part), "ai")
                if len(response.parts) > 1:
                    image_part = response.parts[1]
                    pil_image = image_part.as_image()
                    image_id = str(uuid.uuid4())
                    output_name = image_id + "-gemini-img" + ".png"
                    if pil_image:
                        pil_image.save(f"imgs/{output_name}")

                # print(f"response: {response}")

        except Exception as e:
            print(f"Error: {e}")

    def openImage(filename: str):
        try:
            img = Image.open("imgs/" + filename)
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

    def add_to_history(message: str, tag: str):
        chat_history.config(state="normal")
        print(f"Adding to history:: {tag}: {message}")
        contents = {"role": tag, "parts": [message]}

        chat_history_context.append(contents)
        chat_history.insert(tk.END, message + "\n\n", tag)

        chat_history.config(state="disabled")
        chat_history.see(tk.END)

    def submit():
        message = user_input.get("1.0", "end-1c").strip()
        if message:
            add_to_history(message, "user")
            generateImage(message, chat_history_context)
            user_input.delete("1.0", tk.END)

    root = tk.Tk()
    root.title("Image Generator")
    root.geometry("800x400")

    lfrm = ttk.Frame(root, relief="solid", borderwidth=2)
    lfrm.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    rfrm = ttk.Frame(root, relief="solid", borderwidth=2)
    rfrm.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    chat_frame = ttk.Frame(lfrm, relief="solid", borderwidth=1)
    chat_frame.pack(fill="both", expand=True, padx=5, pady=5)

    chat_scroll = ttk.Scrollbar(chat_frame)
    chat_scroll.pack(side="right", fill="y")

    chat_history = tk.Text(
        chat_frame,
        height=20,
        wrap="word",
        state="disabled",
        yscrollcommand=chat_scroll.set,
        # padx=5,
        # pady=5,
    )
    chat_history.pack(side="left", fill="both", expand=True)

    chat_scroll.config(command=chat_history.yview)

    user_font = font.Font(family="Helvetica", size=15, weight="bold")
    ai_font = font.Font(family="Helvetica", size=15)

    # Create a "tag" for user messages (blue, bold)
    chat_history.tag_configure(
        "user",
        foreground="white",
        background="#007AFF",
        font=user_font,
        justify="right",
        lmargin1=15,
        rmargin=15,
        spacing1=5,
        borderwidth=2,
        relief="solid",
    )
    chat_history.tag_configure(
        "ai",
        background="#AAAAAA",
        font=ai_font,
        lmargin1=15,
        rmargin=15,
        spacing1=10,
        borderwidth=2,
        relief="solid",
    )

    # Create User Input Frame
    user_input_frame = ttk.Frame(lfrm, relief="solid", borderwidth=1)
    user_input_frame.pack(fill="x", expand=True, padx=5, pady=5)

    # user_input_data = tk.StringVar()
    user_input = tk.Text(user_input_frame, height=3, font=ai_font, wrap="word")
    user_input.grid(row=0, column=0, padx=(0, 5))

    user_input_submit = ttk.Button(user_input_frame, text="Send")
    user_input_submit.grid(row=0, column=1, sticky=EW)

    img_listbox_choices = tk.Variable(value=dir_list)
    img_listbox = tk.Listbox(rfrm, listvariable=img_listbox_choices)
    img_listbox.bind("<<ListboxSelect>>", test)
    img_listbox.pack()

    # Bindings:
    user_input_submit.config(command=submit)
    user_input.bind("<Return>", lambda event: submit())

    test_image = ImageTk.PhotoImage(img)
    img_label = tk.Label(rfrm, image=test_image)
    img_label.pack()

    # Add a welcome message
    add_to_history("Hello! I am a helpful AI. Ask me anything.", "ai")
    root.mainloop()


if __name__ == "__main__":
    main()
