import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

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
        self.label_icon.pack(side="left", padx=(10, 0))

        self.label_text = ttk.Label(self, text=self.text, style="Sidebar.TLabel", anchor="w")
        self.label_text.pack(side="left")

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", lambda e: self.command() if self.command else None)
        self.label_icon.bind("<Enter>", lambda e: self.on_enter(e))
        self.label_icon.bind("<Leave>", lambda e: self.on_leave(e))
        self.label_icon.bind("<Button-1>", lambda e: self.command() if self.command else None)
        self.label_text.bind("<Enter>", lambda e: self.on_enter(e))
        self.label_text.bind("<Leave>", lambda e: self.on_leave(e))
        self.label_text.bind("<Button-1>", lambda e: self.command() if self.command else None)

    def on_enter(self, event):
        self.configure(style="SidebarHighlight.TFrame")
        self.label_icon.configure(style="SidebarHighlight.TLabel")
        self.label_text.configure(style="SidebarHighlight.TLabel")
        self.parent.expand()

    def on_leave(self, event):
        self.configure(style="Sidebar.TFrame")
        self.label_icon.configure(style="Sidebar.TLabel")
        self.label_text.configure(style="Sidebar.TLabel")

class HoverSidebar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.collapsed = True
        self.configure(width=50, bg="#34495E")  # Dark shade for sidebar

        self.style = ttk.Style()
        self.style.configure("Sidebar.TFrame", background="#34495E")
        self.style.configure("Sidebar.TLabel", background="#34495E", foreground="#ecf0f1")
        self.style.configure("SidebarHighlight.TFrame", background="#1ABC9C")
        self.style.configure("SidebarHighlight.TLabel", background="#1ABC9C", foreground="#ecf0f1")

        # Load default user photo
        self.user_photo_image = Image.open("icons/user.png")
        self.user_photo_image = ImageTk.PhotoImage(self.user_photo_image.resize((40, 40), Image.Resampling.LANCZOS))
        self.user_photo = ttk.Label(self, image=self.user_photo_image, background="#34495E")
        self.user_photo.pack(padx=5, pady=5)
        self.user_photo.bind("<Button-1>", self.update_user_photo)

        self.icons = {
            "home": ("Home", "icons/home.png"),
            "settings": ("Settings", "icons/settings.png"),
            "dashboard": ("Dashboard", "icons/dashboard.png"),
            "help": ("Help", "icons/help.png"),
            "community": ("Community", "icons/community.png"),
        }

        for name, (text, icon_path) in self.icons.items():
            icon_image = Image.open(icon_path)
            icon_image = ImageTk.PhotoImage(icon_image.resize((20, 20), Image.Resampling.LANCZOS))
            icon_label = SidebarIcon(self, image=icon_image, text=text)
            icon_label.pack(fill="x", padx=5, pady=2)

        self.bind("<Enter>", lambda e: self.expand())
        self.bind("<Leave>", lambda e: self.collapse())

    def expand(self):
        if self.collapsed:
            self.configure(width=200)
            for child in self.winfo_children():
                child.pack_configure(fill="x", padx=5, pady=2)
            self.collapsed = False

    def collapse(self):
        if not self.collapsed:
            self.after(500, self.check_mouse)

    def check_mouse(self):
        if not str(self.winfo_containing(self.winfo_pointerx(), self.winfo_pointery())) == str(self):
            self.configure(width=50)
            for child in self.winfo_children():
                child.pack_configure(padx=5, pady=2)
            self.collapsed = True

    def update_user_photo(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            updated_photo = Image.open(file_path)
            updated_photo = ImageTk.PhotoImage(updated_photo.resize((200, 200),Image.Resampling.LANCZOS))
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

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
