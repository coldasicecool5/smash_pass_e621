import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
import threading

USER_AGENT = "smash_pass/1.0 (by manter)"

# Counter variables
smash_counter = 0
pass_counter = 0
previous_image_url = ""
image_label = None  # Declare image_label as a global variable
counter_label = None  # Declare counter_label as a global variable
lock = threading.Lock()  # Add a lock object
session = requests.Session()
session.headers.update({'User-Agent': USER_AGENT})

def get_random_image(tags):
    try:
        response = session.get(f'https://e621.net/posts/random?tags={tags}')
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            image_element = soup.find('img', {'id': 'image'})
            if image_element and 'src' in image_element.attrs:
                return image_element['src']
            else:
                print("Image URL not found in response.")
        else:
            print("Error fetching image. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making image request:", e)
    return None

def fetch_image(tags_entry):
    global previous_image_url, image_label
    tags = "oc " + tags_entry.get()
    new_image_url = get_random_image(tags)
    if new_image_url and new_image_url != previous_image_url:
        try:
            response = session.get(new_image_url, stream=True)
            if response.status_code == 200:
                try:
                    image = Image.open(response.raw)
                    threading.Thread(target=resize_image, args=(image,)).start()
                    previous_image_url = new_image_url
                except Exception as e:
                    print("Error opening image:", e)
            else:
                print("Error fetching image. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error making image request:", e)

def resize_image(image):
    global image_label
    image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
    current_image = ImageTk.PhotoImage(image)
    image_label.configure(image=current_image)
    image_label.image = current_image

def smash(tags_entry):
    global smash_counter, counter_label
    with lock:
        threading.Thread(target=fetch_image, args=(tags_entry,)).start()
        if previous_image_url:
            smash_counter += 1
            counter_label.config(text=f"Smashes: {smash_counter}  Passes: {pass_counter}")

def pass_(tags_entry):
    global pass_counter, counter_label
    with lock:
        threading.Thread(target=fetch_image, args=(tags_entry,)).start()
        if previous_image_url:
            pass_counter += 1
            counter_label.config(text=f"Smashes: {smash_counter}  Passes: {pass_counter}")

def toggle_dark_light_mode():
    current_theme = window.tk.call("tk", "theme", "use")
    if current_theme == "alt":
        window.tk.call("tk", "theme", "use", "default")
    else:
        window.tk.call("tk", "theme", "use", "alt")

def initialize_gui():
    global image_label, counter_label
    window = tk.Tk()

    style = ttk.Style()
    style.theme_use("alt")
    toggle_button = tk.Button(window, text="Toggle Mode", command=toggle_dark_light_mode)
    toggle_button.pack()

    current_image = ImageTk.PhotoImage(Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT)))
    image_label = tk.Label(window, image=current_image)
    image_label.pack()

    counter_label = tk.Label(window, text=f"Smashes: {smash_counter}  Passes: {pass_counter}")
    counter_label.pack()

    tag_frame = tk.Frame(window)
    tag_frame.pack()

    tags_label = tk.Label(tag_frame, text="Tags:")
    tags_label.pack(side=tk.LEFT)

    tags_entry = tk.Entry(tag_frame)
    tags_entry.pack(side=tk.LEFT)

    button_frame = tk.Frame(window)
    button_frame.pack()

    smash_button = tk.Button(button_frame, text='Smash', command=lambda: smash(tags_entry), bg='green', width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
    smash_button.pack(side=tk.LEFT)

    pass_button = tk.Button(button_frame, text='Pass', command=lambda: pass_(tags_entry), bg='red', width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
    pass_button.pack(side=tk.LEFT)

    return window, counter_label, tags_entry  # Return tags_entry

def update_counter_labels():
    counter_label.config(text=f"Smashes: {smash_counter}  Passes: {pass_counter}")

def start_gui():
    window, counter_label, tags_entry = initialize_gui()  # Receive tags_entry
    fetch_image(tags_entry)  # Pass the tags_entry argument

    window.mainloop()

IMAGE_WIDTH = 700
IMAGE_HEIGHT = 700
BUTTON_WIDTH = 20
BUTTON_HEIGHT = 3

if __name__ == "__main__":
    start_gui()
