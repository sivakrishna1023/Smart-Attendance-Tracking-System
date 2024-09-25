import customtkinter
import subprocess
import threading
import time
import os


customtkinter.set_appearance_mode("dark")

class InterfaceApp(customtkinter.CTk):
    tasks = ["System Cleanup", "Collecting Images", "Face Extraction", "Face Matching", "Attendance Submission"]
    program_list = ['Remove_folders.py', 'Get_class_images.py', 'Extraction_faces_classroom.py', 'Match_with_data.py', 'send_mail.py']

    def __init__(self):
        super().__init__()
        self.gmail = None
        self.name = None
        # Get screen dimensions and set the window size accordingly
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Set window size to match screen dimensions
        self.geometry(f"{screen_width}x{screen_height}")
        self.minsize(screen_width, screen_height)
        self.maxsize(screen_width, screen_height)
        self.title("Attendance")
        
        self.header_label = customtkinter.CTkLabel(self, text="Attendance Management System", font=("Arial", 24))
        self.header_label.grid(row=0, column=0, columnspan=3, padx=20, pady=15, sticky="n")

        self.message_frame = customtkinter.CTkFrame(self)
        self.message_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="n")

        # Label for static part of the message
        self.static_message_label = customtkinter.CTkLabel(self.message_frame, text="", font=("Arial", 18))
        self.static_message_label.pack(side="left")

        # Label for the email part (with blue color)
        self.gmail_label = customtkinter.CTkLabel(self.message_frame, text="", font=("Arial", 18), text_color="blue")
        self.gmail_label.pack(side="left")
        # Create start/stop and terminate buttons
        self.start_stop_button = customtkinter.CTkButton(self, text="Start", command=self.start_loading,font=("Arial", 18))
        self.start_stop_button.grid(row=1, column=0, padx=(250, 200), pady=15, sticky="w")

        self.terminate_button = customtkinter.CTkButton(self, text="Terminate", command=self.terminate_loading,font=("Arial", 18))
        self.terminate_button.grid(row=1, column=1, padx=20, pady=15, sticky="w")

        self.is_loading = False
        self.sections = []
        self.create_sections()
    
    def set_credentials(self, gmail, name):
        """Set the Gmail and name, and update the message label if both are provided."""
        self.gmail = gmail
        self.name = name
        
        # Check if both are set and not None
        if self.gmail and self.name:
            # Update the static part of the message and the email label
            static_message = f"Good Morning Professor {self.name}, sending attendance to "
            self.static_message_label.configure(text=static_message)

            # Update the email label in blue color
            self.gmail_label.configure(text=self.gmail)
        else:
            # Clear the labels if credentials are missing
            self.static_message_label.configure(text="")
            self.gmail_label.configure(text="")

    def create_sections(self):
        for i in range(len(self.tasks)):
            # Frame for each task section
            frame = customtkinter.CTkFrame(self, width=900, height=60)
            frame.grid(row=i + 2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
            frame.grid_propagate(False)  # Prevent the frame from resizing to fit its children

            # Configure frame grid layout
            frame.grid_columnconfigure(0, weight=1)  # Task label column
            frame.grid_columnconfigure(1, weight=2)  # Progress bar column
            frame.grid_columnconfigure(2, weight=1)  # Status label column
            frame.grid_rowconfigure(0, weight=1)  # Ensure row can expand vertically

            # Task label
            label = customtkinter.CTkLabel(frame, text=f"{self.tasks[i]}", font=("Arial", 17))
            label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            # Progress bar
            progress = customtkinter.CTkProgressBar(frame, width=150, height=10)
            progress.grid(row=0, column=1, padx=20, pady=23, sticky="nsew")
            progress.set(0)

            # Status label
            status_label = customtkinter.CTkLabel(frame, text="", font=("Arial", 17))
            status_label.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

            # Add this section's components to self.sections
            self.sections.append((progress, status_label))

        # Configure the rows and columns of the main grid
        for i in range(len(self.tasks) + 1):
            self.grid_rowconfigure(i + 1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def reset_progress_bars(self):
        for progress, status_label in self.sections:
            progress.set(0)  # Reset each progress bar to 0
            status_label.configure(text="")  

    def start_loading(self):
        if not self.is_loading:
            self.is_loading = True
            self.start_stop_button.configure(text="Re-Start")
            self.reset_progress_bars()
            # Run a list of programs sequentially
            # self.run_programs()
            threading.Thread(target=self.run_programs).start()    
        else:
            self.is_loading = False
 
    def terminate_loading(self):
        self.is_loading = False

    def run_single_program(self, program):
        try:
            # Run the program and wait for it to finish
            subprocess.run(['python', "Extraction_faces_classroom.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running {program}: {e}")
        
    def run_programs(self):
        for index, program in enumerate(self.program_list):
            try:
                self.after(0, self.update_status_label, index, "Running...")
                # Run each program and wait for it to finish
                subprocess.run(['python', program], check=True)
                self.after(0, self.update_status_label, index, "Completed")
            except subprocess.CalledProcessError as e:
                print(f"Error running {program}: {e}")
                self.after(0, self.update_status_label, index, "Failed")

    def update_status_label(self, index, status_text):
        progress, status_label = self.sections[index]
        status_label.configure(text=status_text)  # Update to show the current status
        if status_text == "Completed":
            progress.set(1)  # Set progress to 100% when completed
        elif status_text == "Running...":
            progress.set(0.5)
        elif status_text == "Failed":
            progress.set(0)

if __name__ == "__main__":
    app = InterfaceApp()
    app.mainloop()
