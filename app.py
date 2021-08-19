from tkinter import *
from PIL import Image , ImageTk
import threading
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
    
    def convert_frame_to_correct_color(self,frame):
        colored_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        return colored_frame

    def convert_frame_array_to_image(self,frame):
        imaged_frame = Image.fromarray(frame)
        return imaged_frame 

    def convert_image_to_tk_image(self,frame):
        tk_image = ImageTk.PhotoImage(frame)
        return tk_image

    def mirrored_frame(self,frame):
        mirrored_frame = cv2.flip(frame)
        return mirrored_frame


if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()