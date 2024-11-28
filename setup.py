import os
import keyboard
import pyautogui
import webbrowser

# Define paths for the necessary files and directories
data_folder = "Data"
settings_file = os.path.join(data_folder, "settings.txt")
searchables_file = os.path.join(data_folder, "searchables.csv")
screenshots_folder = os.path.join(data_folder, "Screenshots")

def create_directories_and_files():
    # Create the necessary directories if they don't exist
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f"Created directory: {data_folder}")
    else:
        print(f"Directory already exists: {data_folder}")

    if not os.path.exists(screenshots_folder):
        os.makedirs(screenshots_folder)
        print(f"Created directory: {screenshots_folder}")
    else:
        print(f"Directory already exists: {screenshots_folder}")

    # Ensure settings.txt exists by calling configure_settings()
    if not os.path.exists(settings_file):
        print(f"Settings file not found. Initializing configuration...")
        configure_settings()
    else:
        print(f"Settings file already exists: {settings_file}")

    # Create placeholder searchables.csv if it doesn't exist
    if not os.path.exists(searchables_file):
        with open(searchables_file, "w") as f:
            f.write("example_searchable\n")
        print(f"Created placeholder searchables file: {searchables_file}")
    else:
        print(f"Searchables file already exists: {searchables_file}")

def configure_settings():
    # Check if settings file exists and is populated with key values
    needs_configuration = True
    if os.path.exists(settings_file):
        with open(settings_file, "r") as f:
            content = f.read()
        required_keys = {"url", "search_screen_coordinates", "delay"}
        present_keys = {line.split("=")[0] for line in content.splitlines() if "=" in line}

        if required_keys.issubset(present_keys):
            needs_configuration = False

    if not needs_configuration:
        print(f"Settings file already exists at {settings_file}.")
        modify = input("Do you want to modify the existing settings? (y/n): ").strip().lower()
        if modify != "y":
            print("Skipping settings configuration.")
            return

    print("\n--- Configure Settings ---")
    url = input("Enter the URL for the browser automation (default: http://example.com): ") or "http://example.com"
    delay = input("Enter the delay between actions in seconds (default: 5): ") or "5"

    webbrowser.open(url)
    search_screen_coordinates = configure_coordinates(url, "Move your mouse to the search box.")
    address_top_left_coordinates = configure_coordinates(url, "Move your mouse to the top left corner of the address box.")
    address_bottom_right_coordinates = configure_coordinates(url, "Move your mouse to the bottom right corner of the address box.")
    map_top_left_coordinates = configure_coordinates(url, "Move your mouse to the top left corner of the map.")
    map_bottom_right_coordinates = configure_coordinates(url, "Move your mouse to the bottom right corner of the map.")


    with open(settings_file, "w") as f:
        f.write(f"url={url}\n")
        f.write(f"delay={delay}\n")
        f.write(f"search_screen_coordinates={search_screen_coordinates}\n")
        f.write(f"address_top_left_coordinates={address_top_left_coordinates}\n")
        f.write(f"address_bottom_right_coordinates={address_bottom_right_coordinates}\n")
        f.write(f"map_top_left_coordinates={map_top_left_coordinates}\n")
        f.write(f"map_bottom_right_coordinates={map_bottom_right_coordinates}\n")



    print(f"Settings saved to {settings_file}")


def configure_coordinates(url, prompt):
    print("\n--- Configure Coordinates ---")
    print(prompt)
    print("Press 's' to save the coordinates.")

    # Wait for the user to press 's'
    while True:
        if keyboard.is_pressed('s'):  # Detect hotkey press
            position = pyautogui.position()  # Capture mouse position
            coordinates = f"{position.x},{position.y}"
            print(f"Search box coordinates captured: {coordinates}")
            while keyboard.is_pressed('s'):
                pass  # Wait for key release
            return coordinates

def main():
    create_directories_and_files()
    print("\nSetup complete! You can now run the main script.\nHope you have fun with this tool!")

if __name__ == "__main__":
    main()
