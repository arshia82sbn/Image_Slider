from app.utils.config import config
import customtkinter as ctk
from app.ui.photo_slider import PhotoSliderFrame

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    app.title("Photo Slider Test")
    frame = PhotoSliderFrame(master=app)
    app.geometry(config.WINDOW_SIZE)
    app.mainloop()