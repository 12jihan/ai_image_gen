from logging import disable
import os
from io import BytesIO
from tkinter import (
    BOTH,
    EW,
    LEFT,
    Event,
    Listbox,
    Misc,
    StringVar,
    messagebox,
    ttk,
    font,
)
from tkinter.font import Font
from typing import List, Literal, ValuesView, cast

from google.genai import Client
from google.genai.types import (
    GenerateContentConfig,
    GenerateImagesConfig,
    ListModelsConfig,
    Modality,
    Part,
    SafetySetting,
)
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
    client: Client = Client(api_key=api_key)
    models = list(client.models.list())

    print(f"Total models: {len(models)}\n")
    print("Available models:")
    for model in models:
        print(f"- {model.name}")

    def generate_content(message: str, history_list: list):
        prompt: str = message
        contents = history_list
        print(f"CheckBox State: {check_box_state.get()}")
        generate_img = check_box_state.get()

        try:
            response = None
            if not generate_img:
                print("Text generation model!!")
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=GenerateContentConfig(
                        response_modalities=[Modality.TEXT],
                    ),
                )
            else:
                print("Image generation model!!")
                response = client.models.generate_content(
                    model="gemini-2.5-flash-image",
                    contents=contents,
                    config=GenerateContentConfig(
                        response_modalities=[Modality.TEXT, Modality.IMAGE],
                    ),
                )
                print(f"response: {response.parts}")

            if response and response.parts:
                text_part: Part = response.parts[0]
                print(f"response: {response.candidates}")
                # img_part =
                # print(f"img: {img_part}")

                if text_part.text:
                    add_to_history(text_part.text, "model")

        except Exception as e:
            print(f"Errors: {e}")
            add_to_history(str(e), "model")

    def openImage(filename: str):
        try:
            img = Image.open("imgs/" + filename)
        except FileNotFoundError as e:
            print(f"There was an error: {e}")
            # root.destroy()
            return

    def reload_img(e: tk.Event):
        """
        Calls an external Python script when an item is selected.
        """
        nonlocal cur_pil_img

        listbox = cast(tk.Listbox, e.widget)
        selected_indices = listbox.curselection()

        if selected_indices:
            index = selected_indices[0]
            value = listbox.get(index)

            try:
                new_pil_img = Image.open(f"./imgs/{value}")
                cur_pil_img = new_pil_img

                # new_img = ImageTk.PhotoImage(new_pil_img)
                # img_label.config(image=new_img)
                # img_label.image = new_img  # type: ignore
                #
                # print(f"value: {value}")
                frame_width = rfrm.winfo_width()
                frame_height = rfrm.winfo_height()

                class FakeEvent:
                    def __init__(self, w, h):
                        self.width = w
                        self.height = h

                on_frame_resize(FakeEvent(frame_width, frame_height))
            except Exception as ex:
                print(f"Error: {ex}")

        # selected_indices = lb.curselection()
        # print(f"this worked\n{dir(e)}")
        # print(f"this worked\n{e.state}")

    def button_test():
        print("clicked")

    def add_to_history(message: str, tag: str):
        chat_history.config(state="normal")
        print(f"Adding to history:: {tag}: {message}")
        contents = {"role": tag, "parts": [{"text": message}]}

        chat_history_context.append(contents)
        print(chat_history_context)
        chat_history.insert(tk.END, message + "\n\n", tag)

        chat_history.config(state="disabled")
        chat_history.see(tk.END)

    def submit():
        message = user_input.get("1.0", "end-1c").strip()
        if message:
            add_to_history(message, "user")
            generate_content(message, chat_history_context)
            user_input.delete("1.0", tk.END)

    def on_frame_resize(event):
        # This event fires when 'rfrm' is resized

        # Get the frame's new size (minus a little padding)
        new_width = event.width - 10
        new_height = event.height - 10

        # --- Calculate new size, maintaining aspect ratio ---
        img_w, img_h = cur_pil_img.size
        ratio = min(new_width / img_w, new_height / img_h)

        # Don't scale up, only down
        if ratio >= 1.0:
            # Image is smaller than frame, just use original
            new_size = (img_w, img_h)
        else:
            # Image is larger, scale it down
            new_size = (int(img_w * ratio), int(img_h * ratio))

        # --- Prevent errors on minimize ---
        if new_size[0] < 1 or new_size[1] < 1:
            return  # Don't try to resize to 0

        # --- Create the new, resized image ---
        # 1. Resize the *original* PIL image
        resized_pil_img = cur_pil_img.resize(new_size, Image.Resampling.LANCZOS)

        # 2. Create a new PhotoImage
        new_tk_img = ImageTk.PhotoImage(resized_pil_img)

        # 3. Update the label's image
        img_label.config(image=new_tk_img)

        # 4. CRITICAL: Anchor the new image to the label
        img_label.image = new_tk_img  # type: ignore

    root = tk.Tk()
    root.title("Image Generator")
    root.geometry("1200x700")

    lfrm = ttk.Frame(root, relief="solid", borderwidth=2)
    lfrm.pack(side="left", fill="both", expand=False, padx=5, pady=5)

    rfrm = ttk.Frame(root, relief="solid", borderwidth=2)
    rfrm.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    chat_frame = ttk.Frame(lfrm, relief="solid")
    chat_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

    chat_scroll = ttk.Scrollbar(chat_frame)
    chat_scroll.pack(side="right", fill="y")

    user_input_frame = ttk.Frame(lfrm, relief="solid", borderwidth=1)
    user_input_frame.pack(fill="x", padx=5, pady=5)

    bottom_frame = tk.Frame(lfrm, relief="solid", borderwidth=1)
    bottom_frame.pack(side="right", padx=5, pady=5)

    img_listbox_choices = tk.Variable(value=dir_list)
    img_listbox = tk.Listbox(rfrm, listvariable=img_listbox_choices)
    img_listbox.pack(side="top", fill="both", expand=True)
    # image_frame = ttk.Frame(rfrm, relief="solid", borderwidth=1)
    # image_frame.pack()
    pil_img = Image.open("./imgs/sample_image.png")
    cur_pil_img = pil_img
    tk_img = ImageTk.PhotoImage(pil_img)
    img_label = tk.Label(rfrm, image=tk_img)
    # img_label.image = tk_img
    img_label.pack(side="bottom", padx=5, pady=5)

    chat_history = tk.Text(
        chat_frame,
        height=20,
        wrap="word",
        state="disabled",
        yscrollcommand=chat_scroll.set,
        # padx=5,
        # pady=5,
    )
    chat_history.pack(side="bottom", fill="both", expand=True)

    chat_scroll.config(command=chat_history.yview)

    user_font = font.Font(family="Helvetica", size=18, weight="bold")
    ai_font = font.Font(family="Helvetica", size=18, weight="bold")

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
        borderwidth=1,
        relief="solid",
    )
    chat_history.tag_configure(
        "model",
        background="#444",
        font=ai_font,
        lmargin1=15,
        rmargin=15,
        spacing1=10,
        borderwidth=1,
        relief="solid",
    )

    # Create User Input Frame
    # user_input_frame = ttk.Frame(lfrm, relief="solid", borderwidth=1)

    user_input = tk.Text(user_input_frame, height=3, font=ai_font, wrap="word")
    user_input.pack(side="left", fill="y")

    user_input_submit = ttk.Button(user_input_frame, text="Send")
    user_input_submit.pack(side="right", fill="y")

    # Bottom Frame
    check_box_state = tk.BooleanVar()
    check_box = tk.Checkbutton(
        bottom_frame, text="Image Generation", variable=check_box_state
    )
    check_box.pack()

    # Bindings:
    user_input_submit.config(command=submit)
    img_listbox.bind("<<ListboxSelect>>", reload_img)
    user_input.bind("<Return>", lambda event: submit())
    rfrm.bind("<Configure>", on_frame_resize)

    # test_image = ImageTk.PhotoImage(img)
    # img_label = tk.Label(rfrm, image=test_image)
    # img_label.pack()

    # Add a welcome message
    add_to_history("Hello! I am a helpful AI. Ask me anything.", "model")
    root.mainloop()


if __name__ == "__main__":
    main()
