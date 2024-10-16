import time
import tkinter as tk
from tkinter import messagebox

class TimerApp:
    def __init__(self, root):
        """
        Initialize the TimerApp.
        
        :param root: The root Tkinter window
        """
        self.root = root
        self.root.title("Timer")
        self.root.geometry("300x250")  # Set a default window size

        # StringVar objects to hold the input values
        self.hours_var = tk.StringVar(value="0")
        self.minutes_var = tk.StringVar(value="0")
        self.seconds_var = tk.StringVar(value="0")

        # Timer state variables
        self.is_running = False
        self.remaining_time = 0

        self.mode = "timer"  # Add this line to track the current mode
        self.stopwatch_time = 0  # Add this line for stopwatch functionality

        self.input_frame = None  # Add this line
        self.create_widgets()
    
    def create_widgets(self):
        """Create and arrange all the GUI widgets."""
        # Use a frame for better organization of input fields
        self.input_frame = tk.Frame(self.root)  # Change this line
        self.input_frame.pack(pady=10)

        # Create labels and entry fields for hours, minutes, and seconds
        tk.Label(self.input_frame, text="Hours:").grid(row=0, column=0, padx=5)
        tk.Entry(self.input_frame, textvariable=self.hours_var, width=5).grid(row=0, column=1)

        tk.Label(self.input_frame, text="Minutes:").grid(row=0, column=2, padx=5)
        tk.Entry(self.input_frame, textvariable=self.minutes_var, width=5).grid(row=0, column=3)

        tk.Label(self.input_frame, text="Seconds:").grid(row=0, column=4, padx=5)
        tk.Entry(self.input_frame, textvariable=self.seconds_var, width=5).grid(row=0, column=5)

        # Create the main timer display
        self.time_label = tk.Label(self.root, text="00:00:00", font=("Helvetica", 48))
        self.time_label.pack(pady=20)

        # Create a frame for the control buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Create Start, Stop, and Reset buttons
        self.start_button = tk.Button(button_frame, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Add a new frame for mode selection
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=10)

        self.timer_button = tk.Button(mode_frame, text="Timer", command=self.set_timer_mode)
        self.timer_button.pack(side=tk.LEFT, padx=5)

        self.stopwatch_button = tk.Button(mode_frame, text="Stopwatch", command=self.set_stopwatch_mode)
        self.stopwatch_button.pack(side=tk.LEFT, padx=5)

    def start_timer(self):
        """Start the timer if it's not already running."""
        if not self.is_running and self.mode == "timer":
            try:
                # Calculate total seconds from input
                total_seconds = int(self.hours_var.get()) * 3600 + int(self.minutes_var.get()) * 60 + int(self.seconds_var.get())
                if total_seconds <= 0:
                    raise ValueError("Timer must be greater than 0 seconds")
                
                # Set up the timer
                self.remaining_time = total_seconds
                self.is_running = True
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.run_timer()
            except ValueError as e:
                messagebox.showerror("Invalid input", str(e))

    def stop_timer(self):
        """Stop the timer."""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.mode == "stopwatch":
            self.start_button.config(text="Resume")

    def reset_timer(self):
        """Reset the timer and clear input fields."""
        self.stop_timer()
        self.remaining_time = 0
        self.stopwatch_time = 0
        self.time_label.config(text="00:00:00")
        self.hours_var.set("0")
        self.minutes_var.set("0")
        self.seconds_var.set("0")
    
    def run_timer(self):
        """Update the timer display and handle timer completion."""
        if not self.is_running:
            return

        if self.remaining_time <= 0:
            self.time_label.config(text="00:00:00")
            messagebox.showinfo("Time's up", "The timer has finished!")
            self.stop_timer()
            return

        # Calculate hours, minutes, and seconds from remaining time
        hours_left = self.remaining_time // 3600
        minutes_left = (self.remaining_time % 3600) // 60
        seconds_left = self.remaining_time % 60

        # Update the display
        self.time_label.config(text=f"{hours_left:02d}:{minutes_left:02d}:{seconds_left:02d}")
        self.remaining_time -= 1
        
        # Schedule the next update
        self.root.after(1000, self.run_timer)

    def set_timer_mode(self):
        self.mode = "timer"
        self.reset_timer()
        self.input_frame.pack(pady=10)
        self.start_button.config(text="Start", command=self.start_timer)

    def set_stopwatch_mode(self):
        self.mode = "stopwatch"
        self.reset_timer()
        self.input_frame.pack_forget()
        self.start_button.config(text="Start", command=self.start_stopwatch)

    def start_stopwatch(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.run_stopwatch()

    def run_stopwatch(self):
        if not self.is_running:
            return

        self.stopwatch_time += 1
        hours = self.stopwatch_time // 3600
        minutes = (self.stopwatch_time % 3600) // 60
        seconds = self.stopwatch_time % 60

        self.time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.run_stopwatch)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
