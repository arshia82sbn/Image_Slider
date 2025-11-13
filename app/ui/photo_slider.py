import os
from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageTk, UnidentifiedImageError
from tkinter import filedialog, messagebox
from app.utils.config import config
from typing import Optional
from app.controller.app_controller import AppController
from app.utils.log_manager import get_logger

logger = get_logger("PhotoSliderUI")

class SimpleObserver:
    """Simple observer: updates a status label when image changes."""
    def __init__(self, status_label: ctk.CTkLabel):
        self.status_label = status_label

    def update(self, current: int, total: int):
        try:
            self.status_label.configure(text=f"Image {current}/{total}")
        except Exception as e:
            logger.exception("Observer update failed: %s", e)

class PhotoSliderFrame(ctk.CTkFrame):
    """
    Connects to AppController.
    """
    def __init__(self, master=ctk.CTk, **kwargs):
        super().__init__(master, **kwargs)
        image_path = os.path.join(config.BASE_DIR,"..","assests","icons","images.png")
        image = ImageTk.PhotoImage(Image.open(image_path))
        master.iconphoto(False,image)
        master.after(250, lambda: master.iconphoto(False, image))
        self.controller = AppController()
        # Set callbacks
        self.controller.on_images_loaded = self._on_images_loaded
        self.controller.on_image_changed = self._on_image_changed
        self.controller.on_ocr_complete = self._on_ocr_complete
        self.controller.on_error = self._on_error

        # layout
        self.pack(fill="both", expand=True, padx=12, pady=12)

        # image display area
        self.image_label = ctk.CTkLabel(self, text="No image", width=500, height=350)
        self.image_label.pack(pady=(0, 8))

        # controls
        controls = ctk.CTkFrame(self)
        controls.pack(pady=6)

        self.load_btn = ctk.CTkButton(controls, text="Load Folder", command=self._on_load_clicked)
        self.load_btn.grid(row=0, column=0, padx=6)

        self.prev_btn = ctk.CTkButton(controls, text="Prev", command=self._on_prev_clicked)
        self.prev_btn.grid(row=0, column=1, padx=6)

        self.next_btn = ctk.CTkButton(controls, text="Next", command=self._on_next_clicked)
        self.next_btn.grid(row=0, column=2, padx=6)

        self.ocr_btn = ctk.CTkButton(controls, text="OCR (current)", command=self._on_ocr_clicked)
        self.ocr_btn.grid(row=0, column=3, padx=6)

        # status and output
        self.status_label = ctk.CTkLabel(self, text="No images loaded.")
        self.status_label.pack(pady=(6, 4))

        self.text_box = ctk.CTkTextbox(self, width=700, height=120)
        self.text_box.pack(pady=(4, 6))

        # simple observer
        self.observer = SimpleObserver(self.status_label)

    def _on_load_clicked(self):
        folder = filedialog.askdirectory(title="Select image folder")
        if not folder:
            return
        try:
            count = self.controller.load_folder(Path(folder))
            if count == 0:
                messagebox.showinfo("No images", "No images found in selected folder.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load images: {e}")

    def _on_prev_clicked(self):
        prev = self.controller.prev_image()
        if not prev:
            messagebox.showinfo("Info", "No previous image.")

    def _on_next_clicked(self):
        nxt = self.controller.next_image()
        if not nxt:
            messagebox.showinfo("Info", "No next image.")

    def _on_ocr_clicked(self):
        current = self.controller.current_image()
        if not current:
            messagebox.showinfo("Info", "No image to OCR.")
            return
        # clear prior text
        self._set_text("Processing OCR...")
        started = self.controller.extract_text_async(current, callback=self._set_text)
        if not started:
            self._set_text("OCR engine not available or already running.")

    def _on_images_loaded(self, count: int):
        self._set_text(f"Loaded {count} images.")
        # update observer display (1/total if available)
        if self.controller.current_image():
            total = len(self.controller.iterator)
            current_index = (self.controller.iterator._index + 1) if self.controller.iterator else 0
            self.observer.update(current_index, total)

    def _on_image_changed(self, path: Path):
        try:
            # load and show resized image
            pil = Image.open(path)
            pil = pil.resize((700, 450), Image.LANCZOS)
            photo = ImageTk.PhotoImage(pil)
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo  # keep ref
            # update observer label
            total = len(self.controller.iterator) if self.controller.iterator else 0
            cur = (self.controller.iterator._index + 1) if self.controller.iterator else 0
            self.observer.update(cur, total)
            # clear OCR box
            self._set_text("")
        except UnidentifiedImageError:
            self._set_text("Unable to open image (unidentified).")
        except Exception as e:
            logger.exception("Failed to display image: %s", e)
            self._set_text(f"Failed to display: {e}")

    def _on_ocr_complete(self, text: str):
        self._set_text(text or "No text found.")

    def _on_error(self, exc: Exception):
        logger.exception("Controller error: %s", exc)
        self._set_text(f"Error: {exc}")

    def _set_text(self, text: str):
        try:
            self.text_box.delete("1.0", "end")
            self.text_box.insert("1.0", text)
        except Exception as e:
            logger.exception("Failed to set text: %s", e)
