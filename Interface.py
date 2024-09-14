import customtkinter
from PIL import Image

customtkinter.set_appearance_mode("dark")

class InterfaceApp(customtkinter.CTk):
    tasks = [ "System Cleanup", "System Diagnostics", "File Cleanup", "System Update","Face Extraction","Face Matching","Attendance Submission"]
    def __init__(self):
        super().__init__()

        self.geometry("1100x600")
        self.minsize(1100, 600)
        self.maxsize(1100, 600)
        self.title("Attendance")


        self.header_label = customtkinter.CTkLabel(self, text="Attendance Management System", font=("Arial", 24))
        self.header_label.grid(row=0, column=0, columnspan=3, padx=20, pady=10, sticky="n")


        # Create start/stop and terminate buttons
        self.start_stop_button = customtkinter.CTkButton(self, text="Start", command=self.toggle_loading)
        self.start_stop_button.grid(row=1, column=0, padx=(200,20), pady=10, sticky="w")

        self.terminate_button = customtkinter.CTkButton(self, text="Terminate", command=self.terminate_loading)
        self.terminate_button.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        self.is_loading = False
        self.sections = []
        self.create_sections()

    def create_sections(self):
        for i in range(7):
            frame = customtkinter.CTkFrame(self)
            frame.grid(row=i+2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

            label = customtkinter.CTkLabel(frame, text=f"{self.tasks[i]}")
            label.grid(row=0, column=0, padx=10, pady=10)

            progress = customtkinter.CTkProgressBar(frame)
            progress.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

            status_label = customtkinter.CTkLabel(frame, text="")
            status_label.grid(row=0, column=2, padx=10, pady=10)

            self.sections.append((progress, status_label))

        for i in range(7):
            self.grid_rowconfigure(i+1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def toggle_loading(self):
        if self.is_loading:
            self.is_loading = False
            self.start_stop_button.configure(text="Start")
            self.stop_loading()
        else:
            self.is_loading = True
            self.start_stop_button.configure(text="Re-Start")
            self.start_loading()

    def start_loading(self):
        for i, (progress, status_label) in enumerate(self.sections):
            if self.is_loading:
                self.after(i * 5000, self.simulate_loading, progress, status_label)

    def stop_loading(self):
        # Stop all ongoing loaders and reset the progress bars
        for progress, status_label in self.sections:
            progress.stop()
            status_label.configure(text="")

    def terminate_loading(self):
        self.is_loading = False
        self.start_stop_button.configure(text="Start")
        self.stop_loading()

    def simulate_loading(self, progress, status_label):
        if self.is_loading:
            progress.start()
            self.after(5000, self.finish_loading, progress, status_label)

    def finish_loading(self, progress, status_label):
        if self.is_loading:
            progress.stop()
            result = "Done" if self.is_loading and self.get_random_result() else "Rejected"
            status_label.configure(text=result)

    def get_random_result(self):
        import random
        return random.choice([True, False])

if __name__ == "__main__":
    app = InterfaceApp()
    app.mainloop()
