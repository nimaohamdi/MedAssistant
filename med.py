import tkinter as tk
from tkinter import messagebox, ttk
import speech_recognition as sr
import pyttsx3
import datetime
import json
import os
import threading
import time

FILE_NAME = "medications.json"

# --------------------------- 
#       TTS ENGINE 
# ---------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---------------------------
#   Medication File Manager
# ---------------------------
def load_medications():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    default = [
        {"name": "Paracetamol", "time": "08:00", "dose": "1 tablet"},
        {"name": "Ibuprofen", "time": "14:00", "dose": "2 tablets"}
    ]
    save_medications(default)
    return default

def save_medications(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)

# ---------------------------
#    Check Medication Time
# ---------------------------
def check_medication_due():
    now = datetime.datetime.now().strftime("%H:%M")
    meds = load_medications()

    for med in meds:
        if med["time"] == now:
            return f"Reminder: Take {med['dose']} of {med['name']} now."

    return None

# ---------------------------
#       Voice Listening
# ---------------------------
def listen_voice():
    recog = sr.Recognizer()

    with sr.Microphone() as source:
        speak("Listening...")
        try:
            audio = recog.listen(source, timeout=5, phrase_time_limit=5)
            text = recog.recognize_google(audio)
            return text.lower()
        except:
            speak("Sorry, I could not understand.")
            return ""

# ---------------------------
#      GUI Application
# ---------------------------
class MedicalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Voice Assistant")
        self.root.geometry("620x420")
        self.root.resizable(False, False)

        self.create_widgets()
        self.start_medication_checker()

    # ---------------------------
    #        MAIN UI
    # ---------------------------
    def create_widgets(self):

        title = tk.Label(self.root, text="Medical Assistant", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Table
        self.tree = ttk.Treeview(frame, columns=("time", "dose"), show="headings", height=10)
        self.tree.heading("time", text="Time")
        self.tree.heading("dose", text="Dose")

        self.tree.column("time", width=120)
        self.tree.column("dose", width=250)

        self.tree.pack(side="left")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.load_table()

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Add Medication", width=18, command=self.add_med_window).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Remove Selected", width=18, command=self.remove_selected).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Voice Command", width=18, command=self.run_voice_command).grid(row=0, column=2, padx=5)

    # ---------------------------
    #       Load Table Data
    # ---------------------------
    def load_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        meds = load_medications()
        for m in meds:
            self.tree.insert("", "end", values=(m["time"], f"{m['name']} ({m['dose']})"))

    # ---------------------------
    #      Add Medication Window
    # ---------------------------
    def add_med_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Medicine")
        win.geometry("300x250")

        tk.Label(win, text="Medicine Name:").pack(pady=5)
        name_entry = tk.Entry(win)
        name_entry.pack()

        tk.Label(win, text="Time (HH:MM):").pack(pady=5)
        time_entry = tk.Entry(win)
        time_entry.pack()

        tk.Label(win, text="Dose:").pack(pady=5)
        dose_entry = tk.Entry(win)
        dose_entry.pack()

        def save_new():
            name = name_entry.get()
            time_val = time_entry.get()
            dose = dose_entry.get()

            if not name or not time_val or not dose:
                messagebox.showerror("Error", "All fields required!")
                return

            meds = load_medications()
            meds.append({"name": name, "time": time_val, "dose": dose})
            save_medications(meds)

            self.load_table()
            speak("New medicine added.")
            win.destroy()

        tk.Button(win, text="Save", command=save_new).pack(pady=10)

    # ---------------------------
    #       Remove Medication
    # ---------------------------
    def remove_selected(self):
        try:
            selected = self.tree.selection()[0]
            values = self.tree.item(selected)["values"]
            time = values[0]
            name = values[1].split("(")[0].strip()

            meds = load_medications()
            meds = [m for m in meds if not (m["time"] == time and m["name"] == name)]
            save_medications(meds)

            self.load_table()
            speak("Medication removed.")

        except:
            messagebox.showerror("Error", "Select a row first!")

    # ---------------------------
    #       Voice Command Mode
    # ---------------------------
    def run_voice_command(self):
        threading.Thread(target=self.process_voice_logic).start()

    def process_voice_logic(self):
        cmd = listen_voice()

        if "medicine" in cmd:
            reminder = check_medication_due()
            speak(reminder if reminder else "No medicine due now.")

        elif "add" in cmd:
            speak("Adding default medicine aspirin.")
            meds = load_medications()
            meds.append({"name": "Aspirin", "time": "18:00", "dose": "1 tablet"})
            save_medications(meds)
            self.load_table()

        elif "time" in cmd:
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {now}.")

        elif "doctor" in cmd:
            speak("Do you want me to call the doctor?")

        else:
            speak("Command not recognized.")

    # ---------------------------
    #  Background Medication Check
    # ---------------------------
    def start_medication_checker(self):
        def check_loop():
            while True:
                reminder = check_medication_due()
                if reminder:
                    speak(reminder)
                time.sleep(60)

        thread = threading.Thread(target=check_loop, daemon=True)
        thread.start()


# ---------------------------
#     RUN THE GUI APP
# ---------------------------
root = tk.Tk()
app = MedicalApp(root)
root.mainloop()
