# import PySimpleGUI as sg ### This library has turned into being nagware
import FreeSimpleGUI as sg
import json
from PIL import Image, ImageTk
import io
import urllib.request
import tkinter as tk

try:
    with open(r'list.json') as f:
        data = json.load(f)
except FileNotFoundError:
    data = json.loads(urllib.request.urlopen("https://raw.githubusercontent.com/rinuwaii/he-brings-you-playback-progress/main/heBringsYouPlaybackProgress.json").read())
    with open(r'list.json', 'w') as f:
        json.dump(data, f)

def search_and_update_list(search_term):
    search_term = search_term.replace(" ", "-")
    matching_results = [item for item in data if search_term in item["name"]]
    listbox.update(values=matching_results)

def on_listbox_selection(event):
    selected_items = listbox.get()
    if not selected_items:
        return

    selected_item = selected_items[0]
    image_url = selected_item["url"]

    try:
        image_data = urllib.request.urlopen(image_url).read()
    except urllib.error.HTTPError:
        sg.popup_error("Failed to download the image.")
        return
    image = Image.open(io.BytesIO(image_data))

    photo = ImageTk.PhotoImage(image)
    image_elem.update(data=photo)

    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(image_url)
    root.update()


layout = [
    [
        sg.Text("Search:"),
        sg.Input(key="_SEARCH_", enable_events=True),
        sg.Button("Search", key="_SEARCH_BUTTON_"),
    ],
    [
        sg.Listbox(values=[], size=(30, 10), key="_LISTBOX_", enable_events=True)
    ],
    [
        sg.Column([[sg.Image(key="_IMAGE_", size=(200, 200))]])
    ]
]

window = sg.Window("Image Search App", layout, resizable=True, finalize=True)

listbox = window["_LISTBOX_"]
image_elem = window["_IMAGE_"]

# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == "_SEARCH_BUTTON_" or event == "_SEARCH_":
        search_term = values["_SEARCH_"]
        search_and_update_list(search_term)
    elif event == "_LISTBOX_":
        on_listbox_selection(event)

window.close()
