import PySimpleGUI as sg
import json
from PIL import Image, ImageTk
import io
import urllib.request
import tkinter as tk

# Load your JSON data
with open(r'list.json') as f:
    data = json.load(f)

# Function to replace spaces with dashes and search the JSON data
def search_and_update_list(search_term):
    search_term = search_term.replace(" ", "-")
    matching_results = [item for item in data if search_term in item["name"]]
    listbox.update(values=matching_results)

# Event handler for listbox selection
def on_listbox_selection(event):
    selected_items = listbox.get()
    if not selected_items:  # Check if any item is selected
        return

    selected_item = selected_items[0]  # Assuming you only want the first selected item
    image_url = selected_item["url"]

    # Load the image from the URL
    image_data = urllib.request.urlopen(image_url).read()
    image = Image.open(io.BytesIO(image_data))

    # Display the image on the right column
    photo = ImageTk.PhotoImage(image)
    image_elem.update(data=photo)

    # Copy the image URL to clipboard
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(image_url)
    root.update()


# Define the layout
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

# Create the window
window = sg.Window("Image Search App", layout, resizable=True, finalize=True)

# Get the elements for event updates
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

# Close the window
window.close()
