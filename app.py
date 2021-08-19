from tkinter import *
from PIL import Image , ImageTk
import threading
import cv2

class Application():
    def __init__(self,master):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.finishe_app)

        self._DEFAULT_SIZE = 40
        self._ZOOM_SIZE = 60
        self._SHAPE = 'square'
        self._BORDER_COLOR = '#ffffff' 

        self.is_finished = False
        
        self.label_content = Label(self.master)
        self.label_content.pack()

        self.webcam_device = cv2.VideoCapture(0,cv2.CAP_DSHOW)

        self.reed_webcam_thread = threading.Thread(target=self.reed_webcam)  
        self.reed_webcam_thread.start()

    def reed_webcam(self):
        while (self.is_finished == False):
            status, frame = self.webcam_device.read()

            if status:
                frame = self.mirrored_frame(frame)
                frame = self.convert_frame_to_correct_color(frame)
                frame = self.convert_frame_array_to_image(frame)
                frame = self.resize_frame(frame,40)
                frmae = self.transform_shape(frame,self._SHAPE)
                frame = self.convert_image_to_tk_image(frame)

                self.label_content.configure(image=frame)
                self.label_content.image = frame         
        
        self.master.quit()

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
        mirrored_frame = cv2.flip(frame,1)
        return mirrored_frame
    
    def transform_shape(self,frame,shape):
        if shape == 'square':
            x,y = frame.size
            frame_square = frame.crop((int(x*self._DEFAULT_SIZE/100),0,int(x-(x*self._DEFAULT_SIZE/100)),y))

            return frame_square
        else:
            return frame

        
         

    def finishe_app(self):
        self.is_finished = True
    

if __name__ == "__main__":
    try:
        with open('config.txt') as f:
            print(f)
    except:
        pass

    
    
    root = Tk()
    app = Application(root)
    root.mainloop()