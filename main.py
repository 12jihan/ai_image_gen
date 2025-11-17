import os
from io import BytesIO
from tkinter import (
    ttk,
    font,
)
from typing import cast

from google.genai import Client
from google.genai.types import (
    GenerateContentConfig,
    Modality,
)
from PIL import Image, ImageTk
import tkinter as tk
import uuid

from dotenv import load_dotenv


def main():
    load_dotenv()

    dir_list: list[str] = os.listdir("./imgs")
    api_key: str | None = os.getenv("API_KEY")
    chat_history_context: list = []
    client: Client = Client(api_key=api_key)
    models = list(client.models.list())

    def list_models():
        print(f"Total models: {len(models)}\n")
        print("Available models:")
        for model in models:
            print(f"- {model.name}")

    def refresh_image_list():
        print("Refreshing image list...")
        new_dir_list = os.listdir("./imgs")
        img_listbox_choices.set(new_dir_list)
        return new_dir_list

    def generate_content(message: str, history_list: list):
        prompt: str = message
        contents = history_list
        generate_img = check_box_state.get()

        try:
            response = None
            if not generate_img:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=GenerateContentConfig(
                        response_modalities=[Modality.TEXT],
                    ),
                )
            else:
                response = client.models.generate_content(
                    model="gemini-2.5-flash-image",
                    contents=contents,
                    config=GenerateContentConfig(
                        response_modalities=[Modality.TEXT, Modality.IMAGE],
                    ),
                )

            if response.parts:
                for part in response.parts:
                    if part.inline_data:
                        nonlocal cur_pil_img

                        blob = part.inline_data

                        if blob.data:
                            image_bytes = BytesIO(blob.data)
                            pil_img = Image.open(image_bytes)
                            img_name = f"{uuid.uuid4()}-gen-image.png"
                            output_name = f"imgs/{img_name}"
                            pil_img.save(output_name)

                            new_list = refresh_image_list()

                            print(f"Successfully saved image to: {output_name}")

                            try:
                                index = new_list.index(img_name)

                                img_listbox.selection_clear(0, tk.END)
                                img_listbox.selection_set(index)
                                img_listbox.see(index)
                            except ValueError:
                                print(
                                    f"Error: Could not find {output_name} in listbox."
                                )
                            cur_pil_img = pil_img
                            frame_width = rfrm.winfo_width()
                            frame_height = rfrm.winfo_height()

                            # Create a "fake" event to pass to the resize function
                            class FakeEvent:
                                def __init__(self, w, h):
                                    self.width = w
                                    self.height = h

                            on_frame_resize(FakeEvent(frame_width, frame_height))

                    if part.text:
                        add_to_history(part.text, "model")

        except Exception as e:
            print(f"Errors: {e}")
            add_to_history(str(e), "model")

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

                frame_width = rfrm.winfo_width()
                frame_height = rfrm.winfo_height()

                class FakeEvent:
                    def __init__(self, w, h):
                        self.width = w
                        self.height = h

                on_frame_resize(FakeEvent(frame_width, frame_height))
            except Exception as ex:
                print(f"Error: {ex}")

    def add_to_history(message: str, tag: str):
        chat_history.config(state="normal")
        contents = {"role": tag, "parts": [{"text": message}]}

        chat_history_context.append(contents)
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
        new_width = event.width - 10
        new_height = event.height - 10

        img_w, img_h = cur_pil_img.size
        ratio = min(new_width / img_w, new_height / img_h)

        if ratio >= 1.0:
            new_size = (img_w, img_h)
        else:
            new_size = (int(img_w * ratio), int(img_h * ratio))

        if new_size[0] < 1 or new_size[1] < 1:
            return  # Don't try to resize to 0

        resized_pil_img = cur_pil_img.resize(new_size, Image.Resampling.LANCZOS)

        new_tk_img = ImageTk.PhotoImage(resized_pil_img)
        img_label.config(image=new_tk_img)
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

    pil_img = Image.open("./imgs/sample_image.png")
    cur_pil_img = pil_img
    tk_img = ImageTk.PhotoImage(pil_img)
    img_label = tk.Label(rfrm, image=tk_img)
    img_label.pack(side="bottom", padx=5, pady=5)

    chat_history = tk.Text(
        chat_frame,
        height=20,
        wrap="word",
        state="disabled",
        yscrollcommand=chat_scroll.set,
    )
    chat_history.pack(side="bottom", fill="both", expand=True)

    chat_scroll.config(command=chat_history.yview)

    user_font = font.Font(family="Helvetica", size=18, weight="bold")
    ai_font = font.Font(family="Helvetica", size=18, weight="bold")

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

    # Add a welcome message
    add_to_history("Hello! I am a helpful AI. Ask me anything.", "model")
    root.mainloop()


if __name__ == "__main__":
    main()
