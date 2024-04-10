import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from PIL import ImageGrab, ImageTk
import os
import tempfile

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rajzoló Program")
        self.root.resizable(False, False)  # A méretezés letiltása

        # A Canvas létrehozása fehér alaprajzszínnel
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

        # A gombok és vezérlők hozzáadása
        self.copy_button = ttk.Button(self.root, text="Másolás", command=self.copy)
        self.copy_button.grid(row=1, column=0, padx=5, pady=5)

        self.reset_button = ttk.Button(self.root, text="Törlés", command=self.reset)
        self.reset_button.grid(row=1, column=1, padx=5, pady=5)

        self.color_button = ttk.Button(self.root, text="Szín", command=self.choose_color)
        self.color_button.grid(row=1, column=2, padx=5, pady=5)

        self.thickness_label = ttk.Label(self.root, text="Vastagság:")
        self.thickness_label.grid(row=1, column=3, padx=5, pady=5)

        self.thickness_var = tk.StringVar()
        self.thickness_entry = ttk.Entry(self.root, textvariable=self.thickness_var, width=5)
        self.thickness_entry.grid(row=1, column=4, padx=5, pady=5)
        self.thickness_var.set("2")

        self.thickness_scale = ttk.Scale(self.root, from_=1, to=10, orient=tk.HORIZONTAL, command=self.update_thickness)
        self.thickness_scale.grid(row=2, column=0, columnspan=5, padx=10, pady=5)

        self.old_x = None
        self.old_y = None
        self.color = 'black'
        self.thickness = 2
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset_coords)

    def update_thickness(self, value):
        try:
            self.thickness = int(float(value))
            self.thickness_var.set(str(self.thickness))
        except ValueError:
            pass

    def paint(self, event):
        x, y = event.x, event.y
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, x, y, width=self.thickness, fill=self.color)
        self.old_x = x
        self.old_y = y

    def reset_coords(self, event):
        self.old_x = None
        self.old_y = None

    def choose_color(self):
        color = colorchooser.askcolor(title="Szín választása")
        if color:
            self.color = color[1]

    def copy(self):
        if messagebox.askyesno("Másolás", "Biztosan másolni szeretnéd a rajzot?"):
            x0 = self.root.winfo_rootx() + self.canvas.winfo_x()
            y0 = self.root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x0 + self.canvas.winfo_width()
            y1 = y0 + self.canvas.winfo_height()

            img = ImageGrab.grab().crop((x0, y0, x1, y1))
            
            if not os.path.exists("Rajzok"):
                os.makedirs("Rajzok")
            
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_img_file:
                temp_img_file_path = temp_img_file.name
                img.save(temp_img_file_path, format='PNG')
            
            final_path = os.path.join("Rajzok", os.path.basename(temp_img_file_path))
            os.replace(temp_img_file_path, final_path)

            self.root.clipboard_clear()
            self.root.clipboard_append(final_path)
            messagebox.showinfo("Másolás", "A rajz másolva és a vágólapra helyezve!")

    def reset(self):
        if messagebox.askyesno("Törlés", "Biztosan törölni szeretnéd a rajzot?"):
            self.canvas.delete("all")
            messagebox.showinfo("Törlés", "A rajz törölve!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    ttk.Label(root, text="InfinityVerse Games 2023-2024").grid(row=3, column=0, columnspan=5)
    root.mainloop()
