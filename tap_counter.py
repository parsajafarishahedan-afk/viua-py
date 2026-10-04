import sounddevice as sd
import numpy as np
import tkinter as tk
import time

count = 0
last_tap = 0
COOLDOWN = 0.12
THRESHOLD = 0.08

root = tk.Tk()
root.title("敲桌子计数器")
root.geometry("300x200")
root.configure(bg="#111")

label = tk.Label(root, text="0", font=("Arial", 80, "bold"), fg="#22d3ee", bg="#111")
label.pack(expand=True)

def reset():
    global count
    count = 0
    label.config(text="0")

tk.Button(root, text="重置", command=reset).pack(pady=10)

def callback(indata, frames, time_info, status):
    global count, last_tap
    rms = np.sqrt(np.mean(indata ** 2))
    now = time.time()
    if rms > THRESHOLD and (now - last_tap) > COOLDOWN:
        last_tap = now
        count += 1
        root.after(0, lambda: label.config(text=str(count)))

with sd.InputStream(callback=callback, channels=1, samplerate=44100, blocksize=1024):
    root.mainloop()