import customtkinter as ctk
from PIL import Image, ImageTk
import os
from tkinter import filedialog
import pytesseract

class PhotoSlider(ctk.CTk):
    def __init__(self):
        super().__init__()
        # =======================
        # Window Configuration
        # =======================
        self.title("Photo Slider with OCR")
        self.geometry("800x600")
        self.resizable(False, False)

        # =======================
        # Icon Paths (Update with your actual icon paths)
        # =======================
        logo_path = os.path.join(os.path.dirname(__file__), 'images.png')
        logo_icon = ImageTk.PhotoImage(Image.open(logo_path))
        self.iconphoto(False, logo_icon)
        self.after(250, lambda: self.iconphoto(False, logo_icon))

        forward_path = os.path.join(os.path.dirname(__file__),"forward.png")
        back_path = os.path.join(os.path.dirname(__file__),"back.png")

        # =======================
        # Load Navigation Icons
        # =======================
        self.back_photo = ctk.CTkImage(Image.open(back_path), size=(100, 100))
        self.forward_photo = ctk.CTkImage(Image.open(forward_path), size=(100, 100))

        # =======================
        # Navigation Buttons
        # =======================
        self.back_btn = ctk.CTkButton(self, image=self.back_photo, text=" ", command=self.prev_image)
        self.back_btn.place(x=30, y=300)

        self.forward_btn = ctk.CTkButton(self, image=self.forward_photo, text=" ", command=self.next_image)
        self.forward_btn.place(x=650, y=300)

        # =======================
        # Image Display Label
        # =======================
        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.place(x=175, y=50)

        # =======================
        # Folder Selection Button
        # =======================
        self.select_folder_btn = ctk.CTkButton(
            self, text="Select Folder", command=self.select_folder, font=("Roboto", 16)
        )
        self.select_folder_btn.place(x=350, y=450)

        # =======================
        # OCR Trigger Button
        # =======================
        self.ocr_btn = ctk.CTkButton(
            self, text="Extract Text", command=self.extract_text, font=("Roboto", 16)
        )
        self.ocr_btn.place(x=350, y=400)

        # =======================
        # Output Text Box
        # =======================
        self.text_box = ctk.CTkTextbox(self, width=500, height=100, font=("Roboto", 14))
        self.text_box.place(x=175, y=500)

        # =======================
        # Initialize Image State
        # =======================
        self.image_list = []
        self.current_image_index = 0

        # Uncomment and update if Tesseract is not in your PATH
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def select_folder(self):
        """Open a folder dialog, scan for images, and load them."""
        folder_path = filedialog.askdirectory()
        if folder_path:
            # Filter and load image files
            self.image_list = [
                os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
            ]
            if self.image_list:
                self.current_image_index = 0
                self.display_image()
                self.text_box.delete("1.0", "end")
                self.text_box.insert("1.0", f"Folder selected: {folder_path}")
            else:
                self.image_label.configure(text="Selected folder does not contain images.")
                self.text_box.delete("1.0", "end")
                self.text_box.insert("1.0", "Selected folder does not contain images.")

    def display_image(self):
        """Display the current image in the label widget."""
        if self.image_list:
            image_path = self.image_list[self.current_image_index]
            image = Image.open(image_path)
            image = image.resize((500, 400), Image.LANCZOS)  # Resize for display
            photo = ImageTk.PhotoImage(image)

            # Show image
            self.image_label.configure(image=photo)
            self.image_label.image = photo  # Prevent garbage collection

            # Clear the OCR text box
            self.text_box.delete("1.0", "end")

    def next_image(self):
        """Move to the next image in the list."""
        if self.image_list and self.current_image_index < len(self.image_list) - 1:
            self.current_image_index += 1
            self.display_image()

    def prev_image(self):
        """Move to the previous image in the list."""
        if self.image_list and self.current_image_index > 0:
            self.current_image_index -= 1
            self.display_image()

    def extract_text(self):
        """Use Tesseract OCR to extract and display text from the current image."""
        if self.image_list:
            image_path = self.image_list[self.current_image_index]
            try:
                image = Image.open(image_path)
                text = pytesseract.image_to_string(image, lang='fas+eng')  # Persian + English
                self.text_box.delete("1.0", "end")
                self.text_box.insert("1.0", text if text.strip() else "No text found in the image.")
            except Exception as e:
                self.text_box.delete("1.0", "end")
                self.text_box.insert("1.0", f"Error extracting text: {str(e)}")
        else:
            self.text_box.delete("1.0", "end")
            self.text_box.insert("1.0", "Please select a folder with images first.")

if __name__ == "__main__":
    app = PhotoSlider()
    app.mainloop()
