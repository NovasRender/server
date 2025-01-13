import os
import time
import subprocess
import requests
from tqdm import tqdm
import sys

# Function to check and install a module
def install_module(module):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])
    except subprocess.CalledProcessError:
        print(f"Failed to install {module}. Please install it manually.")
        sys.exit(1)

# Ensure tqdm is installed first (since it's used for progress bars)
install_module('tqdm')

# Prompt for password and hint
passs = input("Please Choose A Password: ")
hintt = input("Please Choose A Password Hint: ")

# Save the password and hint to a file "env_variables.txt"
with open("env_variables.txt", "w") as file:
    file.write(f"serverpass={passs}\n")
    file.write(f"pass_hint={hintt}\n")

# Define the required paths
requiredpaths = [
    "sounds", "scripts", "images", "images/languages", 
    "images/system", "sounds/ambience", "sounds/ui"
]

# List of files to download
downloads = {
    "images/languages/py.png": "https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png",
    "images/languages/placeholder.png": "https://cdn-icons-png.flaticon.com/512/3097/3097257.png",
    "sounds/ui/ui1.mp3": "https://cdn.pixabay.com/download/audio/2024/04/29/audio_406ff08fee.mp3?filename=click-buttons-ui-menu-sounds-effects-button-14-205402.mp3",
    "sounds/ui/ui2.mp3": "https://cdn.pixabay.com/download/audio/2024/04/29/audio_718a944b93.mp3?filename=click-buttons-ui-menu-sounds-effects-button-13-205396.mp3",
    "sounds/ui/ui3.mp3": "https://cdn.pixabay.com/download/audio/2024/04/21/audio_6158d88dcf.mp3?filename=click-buttons-ui-menu-sounds-effects-button-2-203594.mp3",
    "sounds/ui/ui4.mp3": "https://cdn.pixabay.com/download/audio/2024/04/21/audio_34c0167350.mp3?filename=click-buttons-ui-menu-sounds-effects-button-6-203600.mp3"
}

# List of required Python modules
required_modules = [
    "customtkinter", "Pillow", "os", "time", "threading", 
    "datetime", "pygame", "random", "glob", "subprocess"
]

# Function to download files using requests
def download_file(url, file_path):
    if not os.path.exists(file_path):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
            return False
    return False

# Create required directories if they don't exist
for path in requiredpaths:
    if not os.path.exists(path):
        os.makedirs(path)

# Install required Python modules with a progress bar
def install_modules(modules):
    for module in modules:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

# Download all files and check installation
def setup():
    # Progress bar for downloading files
    with tqdm(total=len(downloads), desc="Downloading Files", unit="file") as pbar:
        for file_path, url in downloads.items():
            if download_file(url, file_path):
                print(f"Downloaded: {file_path}")
            pbar.update(1)
            time.sleep(0.5)  # Pause between downloads

    # Clear the console after each file download
    os.system('cls' if os.name == 'nt' else 'clear')

    # Install Python modules
    with tqdm(total=len(required_modules), desc="Installing Modules", unit="module") as pbar:
        for module in required_modules:
            try:
                print(f"Installing: {module}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
                pbar.update(1)
            except subprocess.CalledProcessError:
                print(f"Failed to install: {module}")
                pbar.update(1)
            time.sleep(0.5)  # Pause between installations

    # Clear the console after all installations
    os.system('cls' if os.name == 'nt' else 'clear')

# Start the setup
setup()
