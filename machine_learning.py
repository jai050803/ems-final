import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")])
    if file_path:
        try:
            # Load the file with pandas
            df = pd.read_excel(file_path) if file_path.endswith(('.xlsx', '.xls')) else pd.read_csv(file_path)
            clear_data()
            tree["column"] = list(df.columns)
            tree["show"] = "headings"
            # Define headings and column width
            for column in tree["column"]:
                tree.heading(column, text=column)
                tree.column(column, width=100)
            
            # Inserting each row's data into the treeview
            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                tree.insert("", "end", values=row)
                
            messagebox.showinfo("Information", "File loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", "Failed to load the file!\n" + str(e))
    else:
        messagebox.showinfo("Information", "No file selected")

def clear_data():
    tree.delete(*tree.get_children())

root = tk.Tk()
root.title("Data Upload and Display GUI")

frame = tk.Frame(root)
frame.pack(pady=20)

upload_btn = tk.Button(frame, text="Upload CSV/Excel File", command=upload_file)
upload_btn.pack()

# Treeview Widget
tree_frame = tk.Frame(root)
tree_frame.pack(pady=20)

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
tree.pack()

tree_scroll.config(command=tree.yview)

root.mainloop()
