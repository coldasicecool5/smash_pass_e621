import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from bs4 import BeautifulSoup
import threading

USER_AGENT = "smash_pass/1.0 (by manter)"

# Counter variables
smash_counter = 0
pass_counter = 0
previous_image_url = ""

def get_random_image(tags):
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(f'https://e621.net/posts/random?tags={tags}', headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            image_element = soup.find('img', {'id': 'image'})
            if image_element and 'src' in image_element.attrs:
                return image_element['src']
        else:
            print("Error fetching image. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making image request:", e)
    return None

def fetch_image():
    global previous_image_url
    tags = "oc " + tags_entry.get()  # Combine hardcoded "oc" tag with user-specified tag
    new_image_url = get_random_image(tags)
    if new_image_url and new_image_url != previous_image_url:
        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(new_image_url, stream=True, headers=headers)
            if response.status_code == 200:
                try:
                    image = Image.open(response.raw)
                    image = image.resize((700, 700))
                    current_image = ImageTk.PhotoImage(image)
                    image_label.configure(image=current_image)  # Update the image
                    image_label.image = current_image  # Keep a reference to the new image
                    previous_image_url = new_image_url  # Update the previous image URL
                except Exception as e:
                    print("Error opening image:", e)
            else:
                print("Error fetching image. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error making image request:", e)

def smash():
    global smash_counter
    threading.Thread(target=fetch_image).start()
    if previous_image_url:
        smash_counter += 1
        counter_label.config(text=f"Smashes: {smash_counter}  Passes: {pass_counter}")

def pass_():
    global pass_counter
    threading.Thread(target=fetch_image).start()
    if previous_image_url:
        pass_counter += 1
        counter_label.config(text=f"Smashes: {smash_counter}  Passes: {pass_counter}")

def toggle_dark_light_mode():
    current_theme = window.tk.call("tk", "theme", "use")
    if current_theme == "alt":
        window.tk.call("tk", "theme", "use", "default")
    else:
        window.tk.call("tk", "theme", "use", "alt")

window = tk.Tk()

# Dark and light mode toggle
style = ttk.Style()
style.theme_use("alt")
toggle_button = tk.Button(window, text="Toggle Mode", command=toggle_dark_light_mode)
toggle_button.pack()

current_image = ImageTk.PhotoImage(Image.new('RGB', (700, 700)))

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

smash_button = tk.Button(button_frame, text='Smash', command=smash, bg='green', width=20, height=3)
smash_button.pack(side=tk.LEFT)

pass_button = tk.Button(button_frame, text='Pass', command=pass_, bg='red', width=20, height=3)
pass_button.pack(side=tk.LEFT)

fetch_image()  # Fetch the initial image

window.mainloop()
