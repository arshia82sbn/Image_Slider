# 🖼️ Image Slider App

A professional, pattern-driven Python application for managing and navigating image folders, performing OCR (text extraction), and providing a robust and extensible GUI architecture built with **CustomTkinter** and a **clean MVC design**.

---

## 🚀 Overview

**Image Slider** is a modular, production-ready image viewer and OCR utility built with scalability, maintainability, and clean architecture in mind. It combines a sleek graphical interface with advanced backend design principles such as:

- **Singleton Log Manager** — centralized, thread-safe logging for the entire application.
- **Abstract Factory & Strategy Patterns** — modular OCR engines (Tesseract and future integrations).
- **MVC / MVP Hybrid Architecture** — separation of logic, presentation, and data.
- **Exception Safety & Thread Isolation** — ensures stable async OCR execution.
- **Configurable Components** — each module is easily replaceable and reusable.

This app demonstrates **how to architect a complex Python GUI** with layered responsibility, extensibility, and minimal coupling.

---

## 🧩 Architecture Overview

```
app/
├── main.py                    # Entry point with logging and graceful lifecycle
├── controller/
│   └── app_controller.py      # Mediator between UI and core logic (Controller)
├── ui/
│   ├── photo_slider.py        # Main GUI logic with async image navigation (View)
│   ├── text_display.py        # Text output panel for OCR results
│   ├── styles.py              # Centralized theming and UI style management
│   └── __init__.py
├── core/
│   ├── ocr_engine.py          # OCR Engine (Tesseract + abstractions)
│   ├── image_loader.py        # Iterator for managing and navigating image folders
│   ├── file_operations.py     # Safe file I/O utilities
│   └── __init__.py
└── utils/
    ├── log_manager.py         # Singleton-based global logger
    ├── exceptions.py          # Application-wide structured exception classes
    └── config.py              # Configurations for OCR, UI, and file behavior
```

Each folder encapsulates a logical layer — **UI**, **Core**, **Controller**, **Utilities** — following a clear separation of concerns.

---

## 🧠 Design Patterns Used

### 🪞 Singleton
Used in **LogManager** to ensure consistent logging across threads.
```python
class LogManager:
    _instance = None
    _lock = Lock()
```

### 🏭 Factory + Strategy
OCR engine can switch dynamically between implementations without code rewrite.
```python
class OCREngine:
    def extract(self, image):
        raise NotImplementedError()
```

### 🧩 MVC / MVP Hybrid
- **Model**: Core logic (OCR, ImageLoader, FileOps)
- **View**: UI layer (PhotoSlider)
- **Controller**: AppController bridges them cleanly

---

## ⚙️ Key Features

✅ **Image Folder Navigation**  
Load entire folders and navigate smoothly between images with next/previous logic.

✅ **Asynchronous OCR Engine**  
Run OCR extraction without freezing the UI using thread-safe async operations.

✅ **CustomTkinter GUI**  
A dark-themed, modern interface leveraging `customtkinter` for visual polish.

✅ **Robust Exception Handling**  
Every module defines its own clear, hierarchical exception model.

✅ **Logging and Monitoring**  
All modules use the centralized, thread-safe logger with detailed file and line tracking.

✅ **Extensible Design**  
Add new OCR backends, UI components, or data processors without touching existing code.

---

## 🧰 Installation

### Prerequisites
- Python 3.9+
- Tesseract OCR (installed and available in PATH)
- Required libraries:
```bash
pip install customtkinter pillow pytesseract
```

### Run
```bash
python main.py
```

---

## 🧪 Example Use

1. Launch the app.
2. Select an image folder.
3. Use the **Next** / **Previous** buttons to navigate.
4. Trigger **OCR extraction** to read text from current image.
5. View extracted text in the side panel.

---

## 💡 Why This Project Stands Out

- Uses **thread-safe design** with minimal coupling.
- Built using **industry-grade patterns**.
- Easy to extend for machine learning OCR, language models, or translation layers.
- Maintains **full modular independence** between GUI and backend.
- A perfect educational example for learning **clean Python architecture**.

---

## 🔮 Future Enhancements

- [ ] Support for multi-language OCR dynamically.
- [ ] Drag-and-drop folder loading.
- [ ] PDF and document mode.
- [ ] Cloud OCR or GPT-based post-processing.
- [ ] Image preprocessing filters for better OCR accuracy.

---

## 🧑‍💻 Author
**Arshia Saberian**  
A passionate developer focused on Python software engineering, clean code, and scalable architectures.

---

## 🏁 License
MIT License — feel free to use, modify, and learn from this repository.

---

### ⭐ If you found this helpful, give the repo a star — it inspires continued open-source work!
