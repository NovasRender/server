import os

if not os.path.exists("env_variables.txt"):
    print("[ERROR]: Setup.py has not been ran, run that then try again.")
    input("Press any key to exit...")
    exit()

import customtkinter
from PIL import Image, ImageTk
import os
import time
import threading
from datetime import datetime
import pygame
import random
from glob import glob
import subprocess

process = None


def wrap_text(text, line_length):
    words = text.split()
    wrapped_lines = []
    current_line = []

    for word in words:
        # Add word to the current line if it fits
        if sum(len(w) for w in current_line) + len(current_line) + len(word) <= line_length:
            current_line.append(word)
        else:
            # Start a new line
            wrapped_lines.append(" ".join(current_line))
            current_line = [word]

    # Add the last line
    if current_line:
        wrapped_lines.append(" ".join(current_line))

    return "\n".join(wrapped_lines)


page = "Login"
env_file = "env_variables.txt"

# Initialize Pygame for playing sounds
pygame.mixer.init()

# Uptime variable
uptime_seconds = 0

def play_button_click_sound():
    try:
        sound_files = glob("sounds/ui/*.mp3")
        if sound_files:
            sound_to_play = random.choice(sound_files)
            sound = pygame.mixer.Sound(sound_to_play)
            sound.play()
        else:
            print("No sound files found in 'sounds/ui'.")
    except Exception as e:
        print(f"Error playing button click sound: {e}")



def create_buttons_from_folder(folder_path, parent_frame):
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        row, col = 0, 0
        button_size = 150
        
        for file in files:
            button = customtkinter.CTkButton(
                master=parent_frame, 
                text=file, 
                command=lambda f=file: open_script_page(f),
                width=button_size,
                height=button_size
            )
            button.grid(row=row, column=col, padx=20, pady=20, sticky="w")
            
            col += 1
            if col > 2:  # Adjust the number of columns per row
                col = 0
                row += 1


    except FileNotFoundError:
        print(f"The folder '{folder_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")





def open_script_page(script_name):
    play_button_click_sound()

    clear_ui()

    # Get the directory of the currently running script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    image_dir = os.path.join(script_dir, 'images', 'languages')

    # Define the file path for the script
    script_path = os.path.join(script_dir, 'scripts', script_name)

    frame = customtkinter.CTkScrollableFrame(master=root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    mf = customtkinter.CTkFrame(master=frame)
    mf.pack(pady=20, padx=20, fill="both")

    mf.grid_rowconfigure(0, weight=1)
    mf.grid_columnconfigure(0, weight=1)
    mf.grid_columnconfigure(1, weight=2)

    file_size = os.path.getsize(script_path) / (1024 * 1024)  # Convert bytes to MB

    # File information
    title_label = customtkinter.CTkLabel(master=mf, text=f"{script_name}", font=("Roboto", 24), anchor="w")
    title_label.grid(column=0, row=1)

    size_label = customtkinter.CTkLabel(master=mf, text=f"Size: {file_size:.2f} MB", font=("Roboto", 18))
    size_label.grid(row=1, column=1, sticky="w", padx=10)

    # Start/Stop toggle
    process = None

    def log_message(message):
        logtext.insert("end", f"{message}\n")
        logtext.see("end")


    def toggle_script():
        play_button_click_sound()

        nonlocal process

        print(toggle.get())

        if toggle.get() == 0:
            log_message(f"Stopping script: {script_name}")
        else:
            log_message(f"Starting script: {script_name}")
            log_message(f'Running: {script_name}')
            print(script_name)

            os.system(f'start scripts/{script_name}"')


    toggle = customtkinter.CTkSwitch(master=mf, text="Start/Stop", command=toggle_script)
    toggle.grid(row=1, column=2, sticky="w", padx=10)

    # Back button
    back_button = customtkinter.CTkButton(master=mf, text="Back", command=lambda: create_page("Home"))
    back_button.grid(row=1, column=3, sticky="w", padx=10)

    # Graph frames
    graphframeb = customtkinter.CTkFrame(master=frame, bg_color="transparent")
    graphframeb.pack(pady=20, padx=20, fill="both", expand=True)

    graphframeb.grid_columnconfigure(0, weight=1)
    graphframeb.grid_columnconfigure(1, weight=1)

    title_label3 = customtkinter.CTkLabel(master=graphframeb, text="Uptime Graph", font=("Roboto", 24))
    title_label3.grid(column=0, row=0, pady=20)

    title_label3 = customtkinter.CTkLabel(master=graphframeb, text="Activity Graph", font=("Roboto", 24))
    title_label3.grid(column=1, row=0, pady=20)

    uptimegragh = customtkinter.CTkFrame(master=graphframeb)
    uptimegragh.grid(column=0, row=1, padx=20, pady=20, sticky="nsew")

    activitygraph = customtkinter.CTkFrame(master=graphframeb)
    activitygraph.grid(column=1, row=1, padx=20, pady=20, sticky="nsew")

    # Log frame
    logframe = customtkinter.CTkFrame(master=frame)
    logframe.pack(pady=20, padx=20, fill="both", expand=True)

    logtext = customtkinter.CTkTextbox(master=logframe, font=("Roboto", 14), bg_color="transparent", wrap="word")
    logtext.pack(padx=10, pady=10, fill="both", expand=True)

    # Function to read the script's output
    def read_output(proc):
        try:
            while proc.poll() is None:
                line = proc.stdout.readline()
                if line:
                    log_message(line.strip())
            # Capture remaining output
            for line in proc.stdout:
                log_message(line.strip())
            for err_line in proc.stderr:
                log_message(f"ERROR: {err_line.strip()}")
        except Exception as e:
            log_message(f"Error while reading output: {e}")








uptime_seconds = 0

def update_uptime_label(label):
    global uptime_seconds
    def update_label():
        global uptime_seconds
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_text = f"{hours:02}:{minutes:02}:{seconds:02}"
        label.configure(text=f"Uptime   {uptime_text}")
        uptime_seconds += 1
        label.after(1000, update_label)
    update_label()

def update_time_label(label):
    def update_label():
        current_time = datetime.now().strftime("%I:%M %p")
        label.configure(text=current_time)
        label.after(1000, update_label)
    update_label()







def load_env_variables():
    global page
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                os.environ[key] = value
        if "serverpass" in os.environ:
            print("Environment Variable Successfully Loaded")
        else:
            page = "New Password"
    else:
        page = "New Password"

def save_env_variable(key, value):
    os.environ[key] = value
    with open(env_file, "a") as f:
        f.write(f"{key}={value}\n")

def clear_ui():
    for widget in root.winfo_children():
        widget.destroy()

def shake_widget(widget):
    original_x = widget.winfo_x()
    original_y = widget.winfo_y()
    parent = widget.master

    widget.place(x=original_x, y=original_y)
    offsets = [-5, 5] * 3 + [0]

    for offset in offsets:
        widget.place(x=original_x + offset, y=original_y)
        root.update()
        root.after(50)

    widget.place_forget()
    widget.pack_configure()

def create_page(type):

    play_button_click_sound()

    clear_ui()

    if type == "Home":
        # Top Home Bar
        frame = customtkinter.CTkFrame(master=root)
        frame.pack(pady=20, padx=20, fill="x")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        welcomelabel = customtkinter.CTkLabel(master=frame, text="Welcome!", font=("Roboto", 24))
        welcomelabel.grid(row=0, column=0, sticky="w", padx=10)

        timelabel = customtkinter.CTkLabel(master=frame, text="", font=("Roboto", 24))
        timelabel.grid(row=0, column=1, sticky="e", padx=10)

        # Start a thread to update the time label
        threading.Thread(target=update_time_label, args=(timelabel,), daemon=True).start()

        # Uptime Section
        frame = customtkinter.CTkFrame(master=root, height = 60)
        frame.pack(pady=20, padx=20, fill = "x",expand=True)

        uptime_label = customtkinter.CTkLabel(master=frame, text="Uptime   00:00:00", font=("Roboto", 24), anchor="s")
        uptime_label.pack(padx=10, pady=20, anchor="s")

        # Start a thread to update the uptime label
        threading.Thread(target=update_uptime_label, args=(uptime_label,), daemon=True).start()

        frame = customtkinter.CTkFrame(master = root)
        frame.pack(pady= 20, padx = 20, fill = "both", expand = True)

        create_buttons_from_folder('scripts', frame)

def adjust_ui_for_screen_size(root):
    # Adjust the base window size dynamically based on the screen resolution
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    window_width = int(screen_width * 0.6)  # 60% of screen width
    window_height = int(screen_height * 0.6)  # 60% of screen height
    
    root.geometry(f"{window_width}x{window_height}")

# Load environment variables
load_env_variables()

# CustomTkinter setup
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.title("Server")
root.resizable(True, True)  # Allow the window to be resized

# Adjust UI based on screen size
adjust_ui_for_screen_size(root)

signup_visible = False

def login():
    password = passentry.get()
    if password == os.getenv("serverpass"):
        print("Login successful!")
        create_page("Home")
    else:
        shake_widget(loginbutton)

# Define other functions as needed

if page == "Login":
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="Log Into Server", font=("Roboto", 24))
    label.pack(pady=30, padx=10)

    passentry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*", justify="center", width=150, height=35)
    passentry.pack(pady=20, padx=10)

    loginbutton = customtkinter.CTkButton(master=frame, text="Sign In", command=lambda: [login(), play_button_click_sound()])
    loginbutton.pack(pady=10, padx=10)

root.mainloop()
