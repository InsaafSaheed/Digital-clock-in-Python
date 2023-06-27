from time import strftime, sleep
from tkinter import Label, Tk, Entry, StringVar, Toplevel, Button, Frame
import threading
from playsound import playsound

# ======= Configuring the window =========
window = Tk()
window.title("")
window.geometry("200x150")
window.configure(bg="green")  # =======Background of the clock=====
window.resizable(False, False)  # =====setting a fixed window size =======

clock_label = Label(
    window, bg="black", fg="cyan", font=("Arial", 30, "bold"), relief="flat"
)
clock_label.place(x=20, y=20)

# Set up alarm time entry
alarm_hour = StringVar()
alarm_minute = StringVar()
alarm_second = StringVar()

# Create a frame to hold the alarm settings
alarm_frame = Frame(window)
alarm_frame.pack()

# Create the alarm setting fields
Label(alarm_frame, text="Hour:").pack(side="left")
Entry(alarm_frame, textvariable=alarm_hour, width=2).pack(side="left")
Label(alarm_frame, text="Minute:").pack(side="left")
Entry(alarm_frame, textvariable=alarm_minute, width=2).pack(side="left")
Label(alarm_frame, text="Second:").pack(side="left")
Entry(alarm_frame, textvariable=alarm_second, width=2).pack(side="left")

def play_alarm_sound(stop_event):
    # Loop the sound until the stop flag is set
    while not stop_event.is_set():
        #playsound('alarm_sound.mp3')
        print("Alarm!")
        sleep(1)

def stop_alarm(stop_event, alarm_window):
    # Set the stop flag
    stop_event.set()
    # Close the alarm window
    alarm_window.destroy()

def alarm_popup():
    # Create a top-level window
    alarm_window = Toplevel(window)
    alarm_window.title("Alarm")
    
    alarm_label = Label(alarm_window, text="Alarm!")
    alarm_label.pack()

    # Create a threading.Event object to signal stopping the sound
    stop_event = threading.Event()

    # Start the sound in a new thread
    threading.Thread(target=play_alarm_sound, args=(stop_event,)).start()

    # Create a button that stops the sound when clicked and closes the window
    stop_button = Button(alarm_window, text="Stop", command=lambda: stop_alarm(stop_event, alarm_window))
    stop_button.pack()

def update_label():
    """
    This function will update the clock

    every 1000 milliseconds
    """
    current_time = strftime("%H:%M:%S")
    clock_label.configure(text=current_time + "\n" + strftime("%d-%m-%Y"))
    clock_label.after(1000, update_label)
    
    # Check if current time matches alarm time
    alarm_time = "{}:{}:{}".format(alarm_hour.get(), alarm_minute.get(), alarm_second.get())
    if current_time == alarm_time:
        alarm_popup()
    
    clock_label.pack(anchor="center")

update_label()
window.mainloop()
