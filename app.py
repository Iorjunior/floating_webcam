import threading
from tkinter import *
from threading import Thread
import cv2

class Application():
    def __init__(self,master):
        self.master = master
        
        self.label_content = Label(self.master)
        self.label_content.pack()

        self.webcam_device = cv2.VideoCapture(0,cv2.CAP_DSHOW)

        self.reed_webcam_thread = threading.Thread(target=self.reed_webcam)  
        self.reed_webcam_thread.start()

    def reed_webcam(self):
        while True:
            status, frame = self.webcam_device.read()

            if status:
                pass            



if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()