from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import os

class BloodGroupDetector(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.blood_results = [False] * 4
        self.images = [''] * 4
        self.preview_labels = [None] * 4
        self.setup_ui()

    def setup_ui(self):
        self.master.title("Blood Group Detection System")
        self.configure(bg='lightgreen')
        self.pack(fill=BOTH, expand=1)

        # Main container
        main_frame = Frame(self, bg='lightgreen')
        main_frame.pack(padx=20, pady=20)

        # Image selection frames
        labels = ["Anti-A", "Anti-B", "Anti-D", "Control"]
        for i, label in enumerate(labels):
            frame = Frame(main_frame, bg='lightgreen')
            frame.pack(side=LEFT, padx=30, pady=10)
            
            Label(frame, text=label, font=("Helvetica", 12, "bold"), 
                  bg='lightgreen').pack(pady=5)
            
            Button(frame, text="Choose Image",
                   width=15, height=2,
                   command=lambda x=i: self.select_image(x)).pack(pady=10)
            
            # Preview label
            preview = Label(frame, width=30, height=15, bg='white')
            preview.pack(pady=10)
            self.preview_labels[i] = preview

        # Process button
        self.process_btn = Button(self, text="Process Images",
                                state=DISABLED,
                                width=20, height=2,
                                font=("Helvetica", 12),
                                command=self.process_images)
        self.process_btn.pack(pady=30)

    def select_image(self, index):
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if path:
            self.images[index] = path
            self.show_preview(path, index)
            if all(self.images):
                self.process_btn.configure(state='normal')

    def show_preview(self, path, index):
        img = Image.open(path)
        img = img.resize((200, 200), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        self.preview_labels[index].configure(image=img)
        self.preview_labels[index].image = img

    def process_image(self, image_path):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
        return np.mean(thresh) < 127

    def process_images(self):
        try:
            for i, path in enumerate(self.images):
                self.blood_results[i] = self.process_image(path)
            self.determine_blood_group()
        except Exception as e:
            messagebox.showerror("Error", f"Error processing images: {str(e)}")

    def determine_blood_group(self):
        a, b, d, c = self.blood_results
        if c:
            result = "Invalid"
        elif a and b and d:
            result = "AB+"
        elif a and b:
            result = "AB-"
        elif a and d:
            result = "A+"
        elif a:
            result = "A-"
        elif b and d:
            result = "B+"
        elif b:
            result = "B-"
        elif d:
            result = "O+"
        else:
            result = "O-"
        messagebox.showinfo("Result", f"Blood Group: {result}")

def main():
    root = Tk()
    root.geometry("1200x800")
    app = BloodGroupDetector(root)
    root.mainloop()

if __name__ == "__main__":
    main()