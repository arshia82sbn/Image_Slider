from app.controller.app_controller import AppController
from app.ui.photo_slider import PhotoSlider

if __name__ == "__main__":
    controller = AppController()
    app = PhotoSlider(controller)
    app.mainloop()
# some of the part fixed but we need to fixed other part to can complete them .
# add more detial in the compoments file and make complete the comment for the log_manager , and check the tesseract
# complete it!!!