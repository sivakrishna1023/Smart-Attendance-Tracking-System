import customtkinter
from PIL import Image
from Interface import InterfaceApp
from users import users

customtkinter.set_appearance_mode("dark")

class LoginApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set window to the screen's maximum dimensions
        self.default_width = screen_width
        self.default_height = screen_height

        # Set the window geometry to match the screen size
        self.geometry(f"{self.default_width}x{self.default_height}")
        self.minsize(self.default_width, self.default_height)
        self.maxsize(self.default_width, self.default_height)
        self.title("Login Screen")

        # Configure grid layout for dynamic resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Load the image for the login screen
        image = Image.open("logo.jpeg")
        self.img = customtkinter.CTkImage(light_image=image, dark_image=image, size=(450, 400))

        # Left image frame
        self.image_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.image_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)  # Make the frame expand
        self.image_frame.grid_propagate(False)

        self.image_label = customtkinter.CTkLabel(self.image_frame, image=self.img, text="")
        self.image_label.pack(expand=True)  # Center the image inside the frame

        # Form frame on the right
        self.form_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.form_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.form_frame.grid_propagate(False)

        # Add widgets to the form frame with dynamic padding
        self.heading = customtkinter.CTkLabel(self.form_frame, text="Welcome", font=("Arial", 36))
        self.heading.pack(pady=(200, 20), padx=10)

        self.gmail_label = customtkinter.CTkLabel(self.form_frame, text="Gmail:", font=("Arial", 18))
        self.gmail_label.pack(pady=5, padx=10)

        self.gmail_entry = customtkinter.CTkEntry(self.form_frame, placeholder_text="Enter your Gmail", width=270, height=38)
        self.gmail_entry.pack(pady=5, padx=10)

        self.password_label = customtkinter.CTkLabel(self.form_frame, text="Password:", font=("Arial", 18))
        self.password_label.pack(pady=5, padx=10)

        self.password_entry = customtkinter.CTkEntry(self.form_frame, placeholder_text="Enter your password", show="*", width=270, height=38)
        self.password_entry.pack(pady=5, padx=10)

        self.login_button = customtkinter.CTkButton(self.form_frame, text="Login", command=self.login_action, width=270, height=38)
        self.login_button.pack(pady=20, padx=10)

        self.error_label = customtkinter.CTkLabel(self.form_frame, text="", font=("Arial", 14), text_color="red")
        self.error_label.pack(pady=10, padx=10)

        self.gmail_entry.bind("<Key>", self.clear_error_message)
        self.password_entry.bind("<Key>", self.clear_error_message)

    def login_action(self):
        gmail=self.gmail_entry.get()
        password=self.password_entry.get()

        isValid=users.get(gmail)

        if(isValid!= None and isValid.get('password')==password):
            self.destroy()
            new_window = InterfaceApp()
            new_window.set_credentials(gmail, isValid.get('name'))
            new_window.mainloop()
        else:
            self.error_label.configure(text="Invalid Gmail or Password. Please try again.")

    def clear_error_message(self, event=None):
        self.error_label.configure(text="")
        

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
