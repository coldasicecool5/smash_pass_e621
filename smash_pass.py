import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from bs4 import BeautifulSoup

USER_AGENT = "smash_pass/1.0 (by manter)"

# Counter variables
smash_counter = 0
pass_counter = 0

# Flag to toggle between API and web scraping methods
use_api = True

# Cache the API key
API_KEY_CACHE_FILE = "api_key_cache.txt"

def get_random_image_api(api_key, tags):
    try:
        headers = {'User-Agent': USER_AGENT, 'Authorization': f"Bearer {api_key}"}
        params = {'limit': 1000, 'tags': tags}
        response = requests.get('https://e621.net/posts.json', params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Process the response data as needed
            if 'posts' in data and len(data['posts']) > 0:
                return data['posts'][0]['file']['url']
        else:
            print("Error fetching API response. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error making API request:", e)
    return None

def get_random_image_scrape(tags):
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

def save_api_key(api_key):
    with open(API_KEY_CACHE_FILE, 'w') as f:
        f.write(api_key)

def load_api_key():
    if os.path.exists(API_KEY_CACHE_FILE):
        with open(API_KEY_CACHE_FILE, 'r') as f:
            return f.read().strip()
    return ""

def smash():
    global smash_counter, current_image, use_api
    if use_api:
        new_image_url = get_random_image_api(API_KEY.get(), tags_entry.get())
        use_api = False
    else:
        new_image_url = get_random_image_scrape(tags_entry.get())
        use_api = True

    if new_image_url:
        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(new_image_url, stream=True, headers=headers)
            if response.status_code == 200:
                try:
                    image = Image.open(response.raw)
                    image = image.resize((500, 500))
                    current_image = ImageTk.PhotoImage(image)
                    image_label.configure(image=current_image)  # Update the image
                    image_label.image = current_image  # Keep a reference to the new image
                    smash_counter += 1
                    counter_label.config(text=f"Smashes: {smash_counter}  Passes: {pass_counter}")
                except Exception as e:
                    print("Error opening image:", e)
            else:
                print("Error fetching image. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error making image request:", e)

def pass_():
    global pass_counter, current_image, use_api
    if use_api:
        new_image_url = get_random_image_api(API_KEY.get(), tags_entry.get())
        use_api = False
    else:
        new_image_url = get_random_image_scrape(tags_entry.get())
        use_api = True

    if new_image_url:
        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(new_image_url, stream=True, headers=headers)
            if response.status_code == 200:
                try:
                    image = Image.open(response.raw)
                    image = image.resize((500, 500))
                    current_image = ImageTk.PhotoImage(image)
                    image_label.configure(image=current_image)  # Update the image
                    image_label.image = current_image  # Keep a reference to the new image
                    pass_counter += 1
                    counter_label.config(text=f"Smashes: {smash_counter}  Passes: {pass_counter}")
                except Exception as e:
                    print("Error opening image:", e)
            else:
                print("Error fetching image. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error making image request:", e)

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

current_image = ImageTk.PhotoImage(Image.new('RGB', (500, 500)))

image_label = tk.Label(window, image=current_image)
image_label.pack()

counter_label = tk.Label(window, text=f"Smashes: {smash_counter}  Passes: {pass_counter}")
counter_label.pack()

tags_label = tk.Label(window, text="Tags:")
tags_label.pack()

tags_entry = tk.Entry(window)
tags_entry.pack()

api_key_label = tk.Label(window, text="API Key:")
api_key_label.pack()

API_KEY = tk.StringVar()
API_KEY.set(load_api_key())
api_key_entry = tk.Entry(window, textvariable=API_KEY)
api_key_entry.pack()

smash_button = tk.Button(window, text='Smash', command=smash, bg='green', width=10)
smash_button.pack(side=tk.LEFT)

pass_button = tk.Button(window, text='Pass', command=pass_, bg='red', width=10)
pass_button.pack(side=tk.RIGHT)

window.mainloop()
