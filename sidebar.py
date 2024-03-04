import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from PIL import Image, ImageTk, ImageDraw
from correct import EmployeeManagementSystem
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SidebarIcon(ttk.Frame):
    def __init__(self, parent, image, text, command=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.image = image
        self.text = text
        self.command = command
        self.init_ui()

    def init_ui(self):
        self.configure(style="Sidebar.TFrame")
        self.label_icon = ttk.Label(self, image=self.image, style="Sidebar.TLabel")
        self.label_icon.pack(side="top", pady=(10, 0))

        self.label_text = ttk.Label(self, text=self.text, style="Sidebar.TLabel")
        self.label_text.pack(side="top")

        if self.command:
            self.bind("<Button-1>", lambda e: self.command())
            self.label_icon.bind("<Button-1>", lambda e: self.command())
            self.label_text.bind("<Button-1>", lambda e: self.command())

class HoverSidebar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.configure(bg="#34495E", width=200)
        self.pack_propagate(False)
        self.style = ttk.Style()
        self.style.configure("Sidebar.TFrame", background="#34495E")
        self.style.configure("Sidebar.TLabel", background="#34495E", foreground="#ecf0f1")

        # Load and process default user photo for circular display
        self.user_photo_image = Image.open("icons/user.png")
        self.user_photo_image = self.user_photo_image.resize((100, 100), Image.Resampling.LANCZOS)
        self.user_photo_image = self.make_circle(self.user_photo_image)
        self.user_photo_image = ImageTk.PhotoImage(self.user_photo_image)
        
        self.user_photo = ttk.Label(self, image=self.user_photo_image, background="#34495E")
        self.user_photo.pack(pady=20)
        self.user_photo.bind("<Button-1>", self.update_user_photo)

        self.icons = {
            "home": ("Home", "icons/home.png", self.open_employee_management_system),
            "settings": ("Settings", "icons/settings.png", None),  # Assuming no command for now
            "dashboard": ("Dashboard", "icons/dashboard.png", None),
            "help": ("Help", "icons/help.png", None),
            "community": ("Community", "icons/community.png", None),
        }

        y_position = 150
        for name, (text, icon_path, command) in self.icons.items():
            icon_image = Image.open(icon_path)
            icon_image = ImageTk.PhotoImage(icon_image.resize((20, 20), Image.Resampling.LANCZOS))
            
            button = tk.Button(self, image=icon_image, bg="#34495E",border=0, command=command)
            button.image = icon_image  # Keep a reference
            button.place(x=40, y=y_position)
            
            text_label = tk.Label(self, text=text, bg="#34495E", fg="#FFFFFF")
            text_label.place(x=70, y=y_position + 5) 
            
            y_position += 40

    def open_employee_management_system(self):
        self.emp_management_system_window = EmployeeManagementSystem()


    def make_circle(self, image):
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + image.size, fill=255)
        result = Image.new('RGBA', image.size, (0, 0, 0, 0))
        result.paste(image, (0, 0), mask)
        return result

    def update_user_photo(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            updated_photo = Image.open(file_path)
            updated_photo = updated_photo.resize((100, 100), Image.Resampling.LANCZOS)
            updated_photo = self.make_circle(updated_photo)
            updated_photo = ImageTk.PhotoImage(updated_photo)
            self.user_photo.configure(image=updated_photo)
            self.user_photo.image = updated_photo  # Keep a reference.

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Sidebar Example")
        self.state('zoomed')  # Start the window in zoomed state

        self.sidebar = HoverSidebar(self, bg="#34495E")
        self.sidebar.pack(side="left", fill="y")

        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(side="right", expand=True, fill="both")
        
        self.create_header_frame()
        self.create_main_feature_frame()
        self.create_sliders()
        
        self.video_frame = ttk.Frame(self.content_frame)
        self.video_frame.pack(expand=True, fill="both")
        
        

    def create_header_frame(self):
        # Create a header frame with a specific height and full width relative to the content_frame
        header_frame = ttk.Frame(self.content_frame, height=100, style="Header.TFrame")
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)  # Prevents the frame from shrinking to fit its contents

        # Style configuration for the header
        style = ttk.Style()
        style.configure("Header.TFrame", background="#2c3e50")  # Dark shade of blue
        style.configure("Header.TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Arial", 24, "bold"))

        # Adding a label to the header frame
        header_label = ttk.Label(header_frame, text="EMS - A Business Intelligence Tool", style="Header.TLabel")
        header_label.pack(pady=30)
    
    def create_main_feature_frame(self):
        main_feature_frame = ttk.Frame(self.content_frame, height=300)
        main_feature_frame.pack(side="top", fill="x", padx=10, pady=(10, 0))
        main_feature_frame.pack_propagate(False)

        # Task List Frame
        self.task_frame = ttk.Frame(main_feature_frame)
        self.task_frame.pack(side="left", fill="both", expand=True)

        self.task_label = ttk.Label(self.task_frame, text="Tasks")
        self.task_label.pack()

        self.task_listbox = tk.Listbox(self.task_frame)
        self.task_listbox.pack(expand=True, fill="both")

        self.add_task_button = ttk.Button(self.task_frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack()

        # Chart Frame
        self.chart_frame = ttk.Frame(main_feature_frame)
        self.chart_frame.pack(side="right", fill="both", expand=True)

        self.figure, self.ax = plt.subplots(figsize=(3, 2), dpi=100)
        self.chart = FigureCanvasTkAgg(self.figure, self.chart_frame)
        self.chart.get_tk_widget().pack(fill="both", expand=True)

        self.update_chart(0)

    def add_task(self):
        task = simpledialog.askstring("Task", "Describe the task:")
        if task:
            self.task_listbox.insert(tk.END, task)
            self.task_listbox.itemconfig(tk.END, {'bg':'lightgray'})

    def update_chart(self, progress):
        self.ax.clear()
        self.ax.barh(["Task Progress"], [progress], color='skyblue')
        self.ax.set_xlim(0, 100)
        self.chart.draw()


    def create_sliders(self):
    # The container for sliders
        sliders_frame = ttk.Frame(self.content_frame)
        sliders_frame.pack(side="top", fill="x", padx=10, pady=10)

        images_info = [
            ("Data Analysis", "./icons/analytics.png"),
            ("Data Visualization", "./icons/visualization.png"),
            ("Machine Learning", "./icons/settings.png"),
        ]

        for text, image_path in images_info:
            img = Image.open(image_path).resize((50, 50), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            button = ttk.Button(sliders_frame, text=text, image=photo, compound="top", style="Slider.TButton")
            button.image = photo  # Keep a reference
            button.pack(side="left", expand=True, fill="both", padx=5, pady=5)

        # Style for the sliders
        button = tk.Button(sliders_frame, text=text, image=photo, compound="top", bg="#D35400", fg="white", font=("Arial", 10))
        button.config(height=100, width=200)
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
