


# importing the required libraries
import pandas as pd
import os
import time
import datetime
import webbrowser
import pyautogui
import datetime
#import pytesseract

# Load settings from settings.txt
settings = {}
with open("Data/settings.txt") as f:
    for line in f:
        key, value = line.strip().split("=")
        settings[key] = value

# Initialize variables
file = "Data/searchables.csv"
output_folder = "Data/Screenshots"

# settings
url = settings["url"]
delay = int(settings["delay"])

search_screen_coordinates = tuple(map(int, settings["search_screen_coordinates"].split(",")))
address_top_left_coordinates = tuple(map(int, settings["address_top_left_coordinates"].split(",")))
address_bottom_right_coordinates = tuple(map(int, settings["address_bottom_right_coordinates"].split(",")))
map_top_left_coordinates = tuple(map(int, settings["map_top_left_coordinates"].split(",")))
map_bottom_right_coordinates = tuple(map(int, settings["map_bottom_right_coordinates"].split(",")))

# Store timing information for better estimates
timing_data = []
start_time = 0

# Startup
def open_browser():
    print("Opening browser...")
    webbrowser.open(url)
    input("Please set up the settings of the page.\nPress Enter to continue...")

def get_searchables():
    print("Reading from the file...")
    Searchables = pd.read_csv(file, header=None)
    Searchables = Searchables[0].tolist()
    print(f"found {len(Searchables)} searchables.")
    return Searchables

def search(searchable):
    pyautogui.click(search_screen_coordinates)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.write(searchable)
    time.sleep(delay)
    pyautogui.press('down')
    time.sleep(delay)
    pyautogui.press('down')
    pyautogui.press('enter')

def get_screenshot():
    screenshot = pyautogui.screenshot()
    return screenshot

def save_screenshot(screenshot, searchable):
    screenshot.save(os.path.join(output_folder, f"{searchable}.png"))

def predict_finish_time(Searchables, current_index):
    global timing_data

    # Get the current time
    current_time = time.time()

    if current_index > 0:
        # Record elapsed time for this searchable
        elapsed_time = current_time - timing_data[-1]
        timing_data.append(current_time)

        # Calculate the average time per searchable
        average_time_per_searchable = (timing_data[-1] - timing_data[0]) / current_index
    else:
        # Initialize timing data for the first searchable
        timing_data.append(current_time)
        average_time_per_searchable = delay

    # Calculate remaining time
    remaining_searchables = len(Searchables) - current_index
    remaining_time = average_time_per_searchable * remaining_searchables

    # Estimate the finish time
    finish_time = current_time + remaining_time
    readable_finish_time = datetime.datetime.fromtimestamp(finish_time).strftime('%Y-%m-%d %H:%M:%S')
    return readable_finish_time

def crop_split_image(image):
    address = image.crop(address_top_left_coordinates + address_bottom_right_coordinates)
    map = image.crop(map_top_left_coordinates + map_bottom_right_coordinates)
    return address, map

def check_address(address, searchable):
    #address_text = pytesseract.image_to_string(address)
    #if searchable in address_text:
    #    return True
    #return False
    return True

def main():
    open_browser()
    global start_time
    start_time = time.time()
    searchables = get_searchables()

    for index, searchable in enumerate(searchables):
        try:
            search(searchable)
            time.sleep(delay)
            address_screenshot,map_screenshot = crop_split_image(get_screenshot())
            if check_address(address_screenshot, searchable):
                save_screenshot(map_screenshot, searchable)
            else:
                print(f"Address not found in screenshot: {searchable}")
            percent_complete = (index + 1) / len(searchables) * 100
            print(f"Percent complete: {percent_complete:.2f}%")
            print(f"Estimated finish time: {predict_finish_time(searchables, index)}")
        except pyautogui.FailSafeException:
            print("Program terminated due to fail-safe check.")
            break


    print("All screenshots saved.")

if __name__ == "__main__":
    main()