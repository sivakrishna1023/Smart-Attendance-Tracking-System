import customtkinter
import subprocess
import threading
import time
import os

customtkinter.set_appearance_mode("dark")


class InterfaceApp(customtkinter.CTk):
    tasks = ["System Cleanup", "Collecting Images", "Face Extraction", "Face Matching", "Attendance Submission"]
    program_list = ['Remove_folders.py', 'Get_class_images.py', 'Extraction_faces_classroom.py', 'Match_with_data.py', 'send_mail.py']
    selected_time = None
    show_result=False
    
    def __init__(self):
        super().__init__()
        self.gmail = None
        self.name = None
        self.current_thread = None
        self.is_loading = False
        self.stop_thread_flag = threading.Event()
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

        # Time selection dropdown
        self.time_options = ["17 minutes","30 minutes","45 minutes", "1 hour", "2 hours"]
        switch_var = customtkinter.StringVar(value="off")

        def change_state():
            if switch_var.get() == "on":
                self.show_result=True
            else:
                self.show_result=False
        
        def on_time_selected(selected_value):
            if "hour" in selected_value:
                self.selected_time = int(selected_value.split()[0]) * 60
            else:
                self.selected_time = int(selected_value.split()[0])

            print(f"Selected time in minutes: {self.selected_time}")

        self.time_menu = customtkinter.CTkOptionMenu(self, values=self.time_options, command=on_time_selected)
        self.time_menu.set("Select Time Frame")  # Default value
        self.time_menu.grid(row=1, column=0, padx=20, pady=15, sticky="w")

        self.toggle_button = customtkinter.CTkSwitch(self, text="Show Detected Face's", variable=switch_var, onvalue="on", offvalue="off", command=change_state)
        self.toggle_button.grid(row=1, column=0, padx=20, pady=20)


        # Create start/stop and terminate buttons
        self.start_stop_button = customtkinter.CTkButton(self, text="Start", command=self.start_loading, font=("Arial", 18))
        self.start_stop_button.grid(row=1, column=0, padx=(250, 500), pady=15, sticky="w")

        self.terminate_button = customtkinter.CTkButton(self, text="Terminate", command=self.terminate_loading, font=("Arial", 18))
        self.terminate_button.grid(row=1, column=1, padx=35, pady=15, sticky="w")
        self.error_label = customtkinter.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky="w")

        self.is_loading = False
        self.sections = []
        self.create_sections()
    

    def set_credentials(self, gmail, name):
        """Set the Gmail and name, and update the message label if both are provided."""
        self.gmail = gmail
        self.name = name

        if self.gmail and self.name:
            static_message = f"Good Morning Professor {self.name}, sending attendance to "
            self.static_message_label.configure(text=static_message)
            self.gmail_label.configure(text=self.gmail)
        else:
            self.static_message_label.configure(text="")
            self.gmail_label.configure(text="")

    def create_sections(self):
        for i in range(len(self.tasks)):
            frame = customtkinter.CTkFrame(self, width=900, height=60)
            frame.grid(row=i + 2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
            frame.grid_propagate(False)

            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=2)
            frame.grid_columnconfigure(2, weight=1)
            frame.grid_rowconfigure(0, weight=1)

            label = customtkinter.CTkLabel(frame, text=f"{self.tasks[i]}", font=("Arial", 17))
            label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            progress = customtkinter.CTkProgressBar(frame, width=150, height=10)
            progress.grid(row=0, column=1, padx=20, pady=23, sticky="nsew")
            progress.set(0)

            status_label = customtkinter.CTkLabel(frame, text="", font=("Arial", 17))
            status_label.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

            self.sections.append((progress, status_label))

        for i in range(len(self.tasks) + 1):
            self.grid_rowconfigure(i + 1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def reset_progress_bars(self):
        for progress, status_label in self.sections:
            progress.set(0)
            status_label.configure(text="")

    def start_loading(self):
        print(self.selected_time,"By clicking start button")
        print(self.show_result,"This weather to show result or not")
        if self.selected_time is None:
            self.show_error("Please Select the Class Time Period")
            return
        self.error_label.configure(text="")
        if not self.is_loading:
            self.is_loading = True
            self.start_stop_button.configure(text="Re-Start")
            self.start_stop_button.configure(state='disabled')
            self.reset_progress_bars()
            self.stop_thread_flag.clear()
            self.current_thread=threading.Thread(target=self.run_programs)
            self.current_thread.start()
        else:
            self.is_loading = False
    def show_error(self, message):
        """Please Enter the Class Time."""
        print(message)
        self.error_label.configure(text=message)
        self.after(1000, self.clear_error)

    def clear_error(self):
        """Clear the error message from the label."""
        self.error_label.configure(text="")

        
    def terminate_loading(self):
        if self.current_thread is not None and self.current_thread.is_alive():
            self.stop_thread_flag.set()
            print("thread stopped")
        self.start_stop_button.configure(state="normal")
        self.is_loading = False

    def run_programs(self):
        for index, program in enumerate(self.program_list):
            try:
                self.after(0, self.update_status_label, index, "Running...")

                if index == 1: 
                    self.fill_collecting_images_bar()
                    subprocess.run(['python', program, str(self.selected_time)], check=True)
                elif index==2:
                    
                    if(self.show_result):
                        subprocess.run(['python', program, '--showpop'], check=True)
                    else:
                        subprocess.run(['python', program], check=True)
                else:
                    subprocess.run(['python', program], check=True)

                self.after(0, self.update_status_label, index, "Completed")
            except subprocess.CalledProcessError as e:
                print(f"Error running {program}: {e}")
                self.after(0, self.update_status_label, index, "Failed")
        self.start_stop_button.configure(state='normal')
    def fill_collecting_images_bar(self):
        
        if self.selected_time is None:
            print("No time selected. Please select a time.")
            return

        # Calculate the time for the progress bar to fill (selected_time - 16 minutes)
        filling_time = max(self.selected_time - 16, 0)
        if filling_time == 0:
            print("Selected time is less than or equal to 16 minutes, no progress to fill.")
            return

        filling_time_seconds = filling_time * 60
        progress_bar, status_label = self.sections[1]

        interval = 1  # Update every 1 second
        total_steps = filling_time_seconds // interval
        step_increment = 1 / total_steps

        def update_bar(step):
            if step <= total_steps:
                progress_bar.set(step * step_increment)
                self.after(interval * 1000, update_bar, step + 1)

        update_bar(1)

    def update_status_label(self, index, status_text):
        progress, status_label = self.sections[index]
        status_label.configure(text=status_text)
        if status_text == "Completed":
            progress.set(1)
        elif status_text == "Running...":
            progress.set(0.5)
        elif status_text == "Failed":
            progress.set(0)

if __name__ == "__main__":
    app = InterfaceApp()
    app.mainloop()


