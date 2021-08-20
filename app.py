from tkinter import *
from PIL import Image , ImageTk, ImageOps
import threading
import cv2
import json

class Application():
    def __init__(self, master, default_size, zoom_size, shape, border_color, border_size,mirrored):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.finished_app)
        self.master.overrideredirect(1)
        self.master.attributes('-topmost',1)
        self.master.attributes("-transparentcolor", "#2b2921")
        self.master.bind("<Control-X>",self.finished_app)
        self.master.bind("<=>",self.zoom_in)
        self.master.bind("<minus>",self.zoom_out)
        self.master.bind("<slash>",self.mirrored_frame)


        self._DEFAULT_SIZE = default_size
        self._ZOOM_SIZE = zoom_size
        self._SHAPE = shape
        self._BORDER_COLOR = border_color 
        self._BORDER_SIZE = border_size
        self._MIRRORED = mirrored
 
        self.frame_size = self._DEFAULT_SIZE
        self.is_finished = False
        self.is_mirrored = self._MIRRORED
        self.in_zoom = False
        
        self.label_content = Label(self.master,bg='#2b2921')
        self.label_content.bind("<ButtonPress-1>",self.start_move)
        self.label_content.bind("<ButtonRelease-1>",self.stop_move)
        self.label_content.bind("<B1-Motion>",self.do_move)
        self.label_content.bind("<Double-Button-1>",self.zoom_frame)
        self.label_content.pack()

        self.webcam_device = cv2.VideoCapture(0,cv2.CAP_DSHOW)

        self.reed_webcam_thread = threading.Thread(target=self.reed_webcam)  
        self.reed_webcam_thread.start()

    def reed_webcam(self):
        while (self.is_finished == False):
            status, frame = self.webcam_device.read()

            if status:
                frame = self.mirror_frame(frame)
                frame = self.convert_frame_to_correct_color(frame)
                frame = self.convert_frame_array_to_image(frame)
                frame = self.resize_frame(frame,self.frame_size)
                frame = self.transform_shape(frame,self._SHAPE)
                frame = self.set_border(frame)
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

    def mirror_frame(self,frame):
        if self.is_mirrored:
            mirrored_frame = cv2.flip(frame,1)
            return mirrored_frame
        else:
            return frame
    
    def mirrored_frame(self,event=None):
        if self.is_mirrored:
            self.is_mirrored = False
        else:
            self.is_mirrored = True


    def transform_shape(self,frame,shape):
        
        if shape =='square':
            distance_of_border = 15
            x,y = frame.size
            frame_square = frame.crop((int(x*distance_of_border/100),0,int(x-(x*distance_of_border/100)),y))
            return frame_square
        else:
            return frame

    def set_border(self,frame):

        border_frame =  ImageOps.expand(frame,border=self._BORDER_SIZE,fill=self._BORDER_COLOR)  
        return border_frame

    def zoom_frame(self,event=None):
        if self.in_zoom == False:
            self.frame_size = self._ZOOM_SIZE
            self.in_zoom = True
        else:
            self.frame_size = self._DEFAULT_SIZE
            self.in_zoom = False

    def zoom_in(self,event=None):
        self.frame_size += 5
    
    def zoom_out(self,event=None):
        self.frame_size -= 5

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        if self.x or self.y:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.master.winfo_x() + deltax
            y = self.master.winfo_y() + deltay

            self.master.geometry("+{}+{}".format(x, y))

    def finished_app(self,event=None):
        self.is_finished = True


    def key_teste(self,event):
        print(event)

if __name__ == "__main__":
    
    default_config = {
    'default_size':35,
    'zoom_size':70,
    'shape':'square',
    'border_color':'#7a0bbf',
    'border_size':6,
    'mirrored' : True
    }
    json_config = None
    
    try:
        with open('config.json','r', encoding='utf8') as file:
            json_config = json.load(file)
    except:
        with open('config.json','w', encoding='utf8') as file:
            json.dump(default_config,file,indent=2)
            json_config = default_config
            

    root = Tk()
    app = Application(
    master=root,
    default_size=json_config['default_size'],
    zoom_size=json_config['zoom_size'],
    shape=json_config['shape'],
    border_color=json_config['border_color'],
    border_size=json_config['border_size'],
    mirrored=json_config['mirrored']
    )
    root.mainloop()