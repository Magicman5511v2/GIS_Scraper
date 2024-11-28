import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import os
import platform
import subprocess

csv_file = "Data/searchables.csv"
image_directory = "Data/Screenshots/"  # Directory where images are stored
output_file = "responses.csv"  # File to save user responses

# Load image list from the CSV file
try:
    with open(csv_file, "r") as f:
        image_list = [os.path.join(image_directory, line.strip()) for line in f.readlines()]
except FileNotFoundError:
    print(f"Error: {csv_file} not found!")
    exit()

current_index = 0  # Track current image index

# Create the output file with headers if it doesn't already exist
if not os.path.exists(output_file):
    with open(output_file, "w") as f:
        f.write("Image,Response\n")  # Add CSV headers


def open_csv_in_excel(file_path):
    """Open a CSV file in Excel after processing."""
    try:
        if platform.system() == "Windows":  # For Windows systems
            os.startfile(file_path)
        else:
            print("Unable to open the file automatically. Please open it manually.")
    except Exception as e:
        print(f"Error opening file: {e}")

def record_response(response):
    global current_index

    # Record the response directly into the CSV file
    with open(output_file, "a") as f:
        f.write(f"{os.path.basename(image_list[current_index])},{response}\n")

    # Move to the next image
    current_index += 1

    if current_index < len(image_list):
        show_image()
    else:
        print(f"All responses saved to {output_file}.")
        open_csv_in_excel(output_file)  # Open the CSV in Excel
        root.destroy()

def show_image():
    global img

    # Load the current image
    image_path = image_list[current_index]+".png"
    try:
        image = Image.open(image_path)

        # Resize the image to fit in the GUI
        image.thumbnail((800, 800))  # Adjust size as needed
        img = ImageTk.PhotoImage(image)

        # Update the label to display the new image
        image_label.config(image=img)
        image_label.image = img
        image_label_text.config(text=f"Image {current_index + 1} of {len(image_list)}: {os.path.basename(image_path)}")
    except FileNotFoundError:
        print(f"Error: Image file {image_path} not found. Skipping.")
        record_response("File Not Found")

# Create the GUI
root = tk.Tk()
root.title("Image Viewer")

# Image display label
image_label_text = Label(root, text="", font=("Arial", 14))
image_label_text.pack(pady=10)

image_label = Label(root)
image_label.pack()

# Buttons for user responses
yes_button = Button(root, text="Yes", command=lambda: record_response("Yes"))
yes_button.pack(side=tk.LEFT, padx=20, pady=20)

no_button = Button(root, text="No", command=lambda: record_response("No"))
no_button.pack(side=tk.RIGHT, padx=20, pady=20)

# Key bindings for Yes/No responses
root.bind("y", lambda event: record_response("Yes"))
root.bind("n", lambda event: record_response("No"))

# Start with the first image
if image_list:
    show_image()
else:
    print("No images found in the list.")
    root.destroy()

# Start the GUI loop
root.mainloop()
