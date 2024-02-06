import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def split_image(image_path, x_divisions, y_divisions, output_folder):
    try:
        original_image = Image.open(image_path)
    except IOError as e:
        messagebox.showerror("Error", f"Could not open image: {e}")
        return
    
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    
    width, height = original_image.size
    sub_width = width // x_divisions
    sub_height = height // y_divisions
    
    for i in range(y_divisions):
        for j in range(x_divisions):
            left = j * sub_width
            top = i * sub_height
            right = (j + 1) * sub_width
            bottom = (i + 1) * sub_height
            sub_image = original_image.crop((left, top, right, bottom))
            sub_image_filename = f"{name}_{i * x_divisions + j + 1}{ext}"
            sub_image.save(os.path.join(output_folder, sub_image_filename))
    return True

def open_images():
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        listbox_images.delete(0, tk.END)
        for path in file_paths:
            listbox_images.insert(tk.END, path)

def open_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_output_path.delete(0, tk.END)
        entry_output_path.insert(0, folder_path)

def split_images_gui():
    output_folder = entry_output_path.get()
    try:
        x_divisions = int(entry_x_div.get())
        y_divisions = int(entry_y_div.get())
        all_success = True
        for image_path in listbox_images.get(0, tk.END):
            if not split_image(image_path, x_divisions, y_divisions, output_folder):
                all_success = False
        if all_success:
            messagebox.showinfo("成功啦！", "图都切好了，看看去吧!")
    except ValueError as e:
        messagebox.showerror("Value Error", "Please enter valid numbers for divisions.")

# Set up the GUI
root = tk.Tk()
root.title("PAseer的批量图片切割小程序")

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="你想切的图片就往里面放:").grid(row=0, column=0, sticky='e')
listbox_images = tk.Listbox(frame, width=50, height=6)
listbox_images.grid(row=0, column=1)
scrollbar_images = tk.Scrollbar(frame, orient="vertical")
scrollbar_images.config(command=listbox_images.yview)
scrollbar_images.grid(row=0, column=2, sticky='ns')
listbox_images.config(yscrollcommand=scrollbar_images.set)
btn_browse_images = tk.Button(frame, text="Browse", command=open_images)
btn_browse_images.grid(row=1, column=1)

tk.Label(frame, text="横向分几块？输入一下:").grid(row=2, column=0, sticky='e')
entry_x_div = tk.Entry(frame, width=10)
entry_x_div.grid(row=2, column=1, sticky='w')

tk.Label(frame, text="竖向分几块？输入一下:").grid(row=3, column=0, sticky='e')
entry_y_div = tk.Entry(frame, width=10)
entry_y_div.grid(row=3, column=1, sticky='w')

tk.Label(frame, text="你把切好的图放在这个目录哈:").grid(row=4, column=0, sticky='e')
entry_output_path = tk.Entry(frame, width=50)
entry_output_path.grid(row=4, column=1)
btn_browse_folder = tk.Button(frame, text="Browse", command=open_folder)
btn_browse_folder.grid(row=4, column=2)

btn_split = tk.Button(root, text="开始切割", command=split_images_gui)
btn_split.pack()

root.mainloop()
