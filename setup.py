import os
import time
import subprocess
import urllib.request
from tqdm import tqdm

passs = input("Please Choose A Password: ")
hintt = input("Please Choose A Password Hint: ")

with open("env_variables.txt", "w") as file:
    file.write(f"setuppass={passs}\n")
    file.write(f"pass_hint={hintt}\n")

requiredpaths = [
    "sounds", "scripts", "images", "images/languages", 
    "images/system", "sounds/ambience", "sounds/ui"
]

downloads = {
    "images/languages/py.png": "https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png",
    "images/languages/placeholder.png": "https://cdn-icons-png.flaticon.com/512/3097/3097257.png",
    "sounds/ui/ui1.mp3": "https://cdn.pixabay.com/download/audio/2024/04/29/audio_406ff08fee.mp3?filename=click-buttons-ui-menu-sounds-effects-button-14-205402.mp3",
    "sounds/ui/ui2.mp3": "https://cdn.pixabay.com/download/audio/2024/04/29/audio_718a944b93.mp3?filename=click-buttons-ui-menu-sounds-effects-button-13-205396.mp3",
    "sounds/ui/ui3.mp3": "https://cdn.pixabay.com/download/audio/2024/04/21/audio_6158d88dcf.mp3?filename=click-buttons-ui-menu-sounds-effects-button-2-203594.mp3",
    "sounds/ui/ui4.mp3": "https://cdn.pixabay.com/download/audio/2024/04/21/audio_34c0167350.mp3?filename=click-buttons-ui-menu-sounds-effects-button-6-203600.mp3"
}

required_modules = [
    "customtkinter", "Pillow", "os", "time", "threading", 
    "datetime", "pygame", "random", "glob", "subprocess"
]

def download_file(url, file_path):
    if not os.path.exists(file_path):
        urllib.request.urlretrieve(url, file_path)
        return True
    return False

for path in requiredpaths:
    if not os.path.exists(path):
        os.makedirs(path)

def install_modules(modules):
    for module in modules:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

def setup():
    with tqdm(total=len(downloads), desc="Downloading Files", unit="file") as pbar:
        for file_path, url in downloads.items():
            if download_file(url, file_path):
                print(f"Downloaded: {file_path}")
            pbar.update(1)
            time.sleep(0.5)

    os.system('cls' if os.name == 'nt' else 'clear')

    with tqdm(total=len(required_modules), desc="Installing Modules", unit="module") as pbar:
        for module in required_modules:
            try:
                print(f"Installing: {module}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
                pbar.update(1)
            except subprocess.CalledProcessError:
                print(f"Failed to install: {module}")
                pbar.update(1)
            time.sleep(0.5)

    os.system('cls' if os.name == 'nt' else 'clear')

setup()
