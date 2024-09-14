import customtkinter
from PIL import Image
from Interface import InterfaceApp

customtkinter.set_appearance_mode("dark")

class LoginApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Initial setup for windowed mode
        self.default_width = 1100
        self.default_height = 600
        
        # Set fixed window size initially
        self.geometry(f"{self.default_width}x{self.default_height}")
        self.minsize(self.default_width, self.default_height)
        self.maxsize(self.default_width,self.default_height)
        self.title("Login Screen")

        # Load the image for the login screen
        image = Image.open("logo.jpeg")
        self.img = customtkinter.CTkImage(light_image=image, dark_image=image, size=(450, 400))

        # Left image frame
        self.image_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.image_frame.pack(side="left", fill="y", padx=20, pady=20)

        self.image_label = customtkinter.CTkLabel(self.image_frame, image=self.img, text="")
        self.image_label.pack(pady=100, padx=30)

        # Form frame on the right
        self.form_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.form_frame.pack(side="left", fill="y", padx=20, pady=20)

        self.heading = customtkinter.CTkLabel(self.form_frame, text="Welcome", font=("Arial", 34))
        self.heading.pack(pady=(110, 20), padx=(90, 180))

        self.gmail_label = customtkinter.CTkLabel(self.form_frame, text="Gmail:", font=("Arial", 16))
        self.gmail_label.pack(pady=5, padx=(90, 180))

        self.gmail_entry = customtkinter.CTkEntry(self.form_frame, placeholder_text="Enter your Gmail", width=250, height=35)
        self.gmail_entry.pack(pady=5, padx=(90, 180))

        self.password_label = customtkinter.CTkLabel(self.form_frame, text="Password:", font=("Arial", 16))
        self.password_label.pack(pady=5, padx=(90, 180))

        self.password_entry = customtkinter.CTkEntry(self.form_frame, placeholder_text="Enter your password", show="*", width=250, height=35)
        self.password_entry.pack(pady=5, padx=(90, 180))

        self.login_button = customtkinter.CTkButton(self.form_frame, text="Login", command=self.login_action, width=250, height=35)
        self.login_button.pack(pady=20, padx=(90, 180))

    def login_action(self):
        print(self.gmail_entry.get())
        print(self.password_entry.get())
        self.destroy()
        new_window = InterfaceApp()
        new_window.mainloop()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()