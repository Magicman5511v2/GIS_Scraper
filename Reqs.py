import subprocess
import sys

def update_pip():
    try:
        # Run pip install --upgrade pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("pip has been successfully updated!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while updating pip: {e}")

# Call the function to update pip
update_pip()

# Function to install a package if not already installed
def install_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure installed packages
install_package("keyboard")
install_package("pandas")
install_package("webbrowser")
install_package("pyautogui")
install_package("xlrd")
install_package("xlwt")
install_package("tkinter")
install_package("PIL")
install_package("openpyxl")

#install_package("pytesseract")