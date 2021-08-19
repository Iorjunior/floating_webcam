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
                frame = self.convert_frame_to_correct_color(frame)
                frame = self.convert_frame_array_to_image(frame)
                frame = self.resize_frame(frame,40)
                frame = self.convert_image_to_tk_image(frame)

                self.label_content.configure(image=frame)
                self.label_content.image = frame         
    
    def resize_frame(self,frame,porcent):
        
        x = int(frame.size[0] * porcent / 100)
        y = int(frame.size[1] * porcent / 100)
        new_size = (x,y)

        resized_frame = frame.resize(new_size, Image.BILINEAR)
        
        return resized_frame

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