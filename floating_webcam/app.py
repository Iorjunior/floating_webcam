from tkinter import Tk, Label
from PIL import Image , ImageTk, ImageOps
import threading
import cv2
import json
import tools

class Application():
    def __init__(self, master,*args):
       
        self._START_POS_X = args[0]['start_pos_x']
        self._START_POS_Y = args[0]['start_pos_y'] 
        self._DEFAULT_SIZE = args[0]['default_size']
        self._ZOOM_SIZE = args[0]['zoom_size']
        self._SHAPE = args[0]['shape']
        self._BORDER_COLOR = args[0]['border_color'] 
        self._BORDER_SIZE = args[0]['border_size']
        self._MIRRORED = args[0]['mirrored']

        self.master = master
        self.master.geometry("+{}+{}".format(self._START_POS_X, self._START_POS_Y))
        self.master.protocol("WM_DELETE_WINDOW", self.finished_app)
        self.master.overrideredirect(1)
        self.master.attributes('-topmost',1)
        self.master.attributes("-transparentcolor", "#2b2921")
        self.master.bind("<Control-X>",self.finished_app)
        self.master.bind("<=>",self.zoom_in)
        self.master.bind("<minus>",self.zoom_out)
        self.master.bind("<slash>",self.mirrored_frame)
                             
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
        if self.frame_size < 95:
            self.frame_size += 5
          
    def zoom_out(self,event=None):
        if self.frame_size > 15:
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
        if self.save_preferences():
            self.is_finished = True
        else:
            self.save_preferences()
    
    def save_preferences(self):
        preferences = {
        'start_pos_x' : self.master.winfo_x(),
        'start_pos_y' : self.master.winfo_y(),
        'default_size': self.frame_size,
        'zoom_size': self._ZOOM_SIZE,
        'shape': self._SHAPE,
        'border_color': self._BORDER_COLOR,
        'border_size': self._BORDER_SIZE,
        'mirrored' : self.is_mirrored
        }
        return tools.write_config_json(preferences)

    def key_teste(self,event):
        print(event)


if __name__ == "__main__":

    json_config = tools.reed_config_json()
    root = Tk()
    app = Application(root,json_config)
    root.mainloop()
    