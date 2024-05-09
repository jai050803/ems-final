import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
import pandas as pd
import openpyxl
from docx import Document
from scipy.stats import mode as scipy_mode
from pandasgui import show
import matplotlib.pyplot as plt 
import seaborn as sns
import textwrap
import numpy as np
import pymysql
from tkinter import Scrollbar
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor, plot_tree
# from sklearn.preprocessing import MinMaxScaler

class EmployeeManagementSystem:
    def __init__(self, root=None):
        if root is None:
            root = tk.Tk()
        self.root = root
        root.title("EMS - A Business Intelligence Tool")
        self.root.state('zoomed')
        self.theme = "light"  # Default theme
        self.status_frame = None  # Initialize status_frame attribute
        # Example data (you will need to replace this with your actual data)
        self.data = None


        # Add file_path attribute
        self.file_path = None
        self.current_data = None
        self.menu_frame=None

        # Header Frame
        self.header_frame = tk.Frame(root, bg="#273746", height=70, bd=1, relief=tk.SOLID)
        self.header_frame.pack(fill=tk.X)

        header_label = tk.Label(self.header_frame, text="EMS - A Business Intelligence Tool", font=("Arial", 20, "bold"), bg="#273746", fg="white")
        header_label.pack(pady=15)

        # Main Part Frame
        self.main_frame = tk.Frame(root, bg="#ecf0f1", height=250, bd=1, relief=tk.SOLID)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Skyblue Left Frame
        self.menu_frame = tk.Frame(self.main_frame, bg="darkgrey", width=150, bd=1, relief=tk.SOLID)
        self.menu_frame.pack(fill=tk.Y, side=tk.LEFT)

        # Bottom Frame
        self.bottom_frame = tk.Frame(self.main_frame, bg="#ecf0f1", bd=1, relief=tk.SOLID)
        self.bottom_frame.pack(fill=tk.X)

        # Buttons for Data Operations
        data_operations = ["DATA CLEANING", "DATA INFORMATION", "DATA VISUALIZATION", "FORECAST"]
        for operation in data_operations:
            if operation == "DATA INFORMATION":
                operation_button = tk.Button(self.bottom_frame, text=operation, command=self.show_data_info, bg="#273746", fg="#ecf0f1", width=17, bd=1, relief=tk.RAISED)
            else:
                operation_button = tk.Button(self.bottom_frame, text=operation, command=lambda op=operation: self.perform_operation(op),
                                            bg="#273746", fg="#ecf0f1", width=17, bd=1, relief=tk.RAISED)
            operation_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Download Button
        download_button = tk.Button(self.bottom_frame, text="Download Data", command=self.download_data, bg="#273746", fg="#ecf0f1", width=15, bd=1, relief=tk.RAISED)
        download_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Heading for File Upload
        file_heading = tk.Label(self.menu_frame, text="Upload File", font=("Arial", 14, "bold"), bg="darkgrey", fg="white")
        file_heading.pack(pady=10)

        # Buttons for Different File Types
        file_types = ["CSV", "Text", "Excel", "Word","MySQL Server"]
        for file_type in file_types:
            button = tk.Button(self.menu_frame, text=f"Open {file_type}", command=lambda ft=file_type: self.open_file(ft),
                               bg="#273746", fg="#ecf0f1", width=15, bd=1, relief=tk.RAISED)
            button.pack(pady=5)

        # Main Content Frame (2/3 of Main Part Frame)
        self.content_frame = ttk.Frame(self.main_frame, style="Light.TFrame")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview widget for tabular and non-tabular display
        self.treeview_frame = ttk.Frame(self.content_frame, style="Light.TFrame")
        self.treeview_frame.pack(expand=True, fill=tk.BOTH)

        self.treeview_style = ttk.Style()
        self.treeview_style.configure("Treeview", font=("Arial", 10), background="#ecf0f1", fieldbackground="#ecf0f1", foreground="#17202a")

        # Configure styles for Light and Dark themes
        self.treeview_style.configure("Light.TFrame", background="#ecf0f1")
        self.treeview_style.configure("Dark.TFrame", background="#2c3e50")

        self.treeview = ttk.Treeview(self.treeview_frame, show="headings", style="Treeview")
        self.treeview["columns"] = tuple()
        self.treeview.pack(expand=True, fill=tk.BOTH)

        y_scrollbar = ttk.Scrollbar(self.treeview_frame, orient="vertical", command=self.treeview.yview)
        y_scrollbar.pack(side="right", fill="y")
        self.treeview.configure(yscrollcommand=y_scrollbar.set)

        x_scrollbar = ttk.Scrollbar(self.treeview_frame, orient="horizontal", command=self.treeview.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        self.treeview.configure(xscrollcommand=x_scrollbar.set)

        # Footer Frame
        self.footer_frame = tk.Frame(root, bg="#273746", height=30, bd=1, relief=tk.SOLID)
        self.footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        footer_label = tk.Label(self.footer_frame, text="© 2024 EMS - A Business Intelligence Tool", font=("Arial", 8), bg="#273746", fg="white")
        footer_label.pack(pady=5)

        # Toggle Theme Button with Image
        toggle_image_light = Image.open("files/images/light.png")  # Replace with your light theme icon
        toggle_image_dark = Image.open("files/images/dark.png")  # Replace with your dark theme icon
        light_icon_resized = toggle_image_light.resize((20, 20))
        dark_icon_resized = toggle_image_dark.resize((20, 20))
        self.light_icon = ImageTk.PhotoImage(light_icon_resized)
        self.dark_icon = ImageTk.PhotoImage(dark_icon_resized)

        self.toggle_theme_button = tk.Button(self.menu_frame, image=self.light_icon, command=self.toggle_theme, bd=0)
        self.toggle_theme_button.pack(side=tk.BOTTOM, padx=10, pady=5, anchor='w')

        self.set_theme()

    def apply_function(self, func):
        if func:
            try:
                self.current_data = func(self.current_data)  # Apply the function to modify the data
                self.update_main_window_data()  # Update main window data
                self.update_data_cleaning_window_data()  # Update data cleaning window data
                messagebox.showinfo("Success", "Function applied successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "No function selected!")


    def update_main_window_data(self):
        self.display_in_treeview(self.current_data)

    def dashboard(self):
        selected_graphs = []
        selected_columns = []

        graph_options = ["Bar Plot", "Histogram", "Scatter Plot", "Box Plot", "Pie Chart", "Line Plot", "Area Plot", "Violin Plot"]

        def add_graph():
            selected_graph = graph_listbox.curselection()
            if selected_graph:
                selected_graph_index = selected_graph[0]
                selected_graph_name = graph_options[selected_graph_index]
                selected_graphs.append(selected_graph_name)

                selected_column1 = entry1.get()
                selected_column2 = entry2.get()
                selected_columns.append((selected_column1, selected_column2))

                graph_display_label.config(text=f"Graphs Selected: {', '.join(selected_graphs)}")

        def generate_dashboard():
            dashboard_figure, dashboard_axes = plt.subplots(len(selected_graphs), figsize=(10, 6 * len(selected_graphs)))
            for i, (graph_name, (column1, column2)) in enumerate(zip(selected_graphs, selected_columns)):
                ax = dashboard_axes[i] if len(selected_graphs) > 1 else dashboard_axes
                self.generate_graph(graph_name, column1, column2, ax)
            plt.tight_layout()
            plt.savefig("dashboard.png")  # Save dashboard image
            plt.show()

        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title("Dashboard")

        graph_listbox = tk.Listbox(dashboard_window, selectmode="multiple", height=len(graph_options), font=("Arial", 12))
        for option in graph_options:
            graph_listbox.insert(tk.END, option)
        graph_listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        label1 = tk.Label(dashboard_window, text="Enter Measured Column Name", font=("Arial", 12))
        label1.pack()
        entry1 = tk.Entry(dashboard_window, font=("Arial", 12))
        entry1.pack(fill=tk.X, padx=5, pady=5)

        label2 = tk.Label(dashboard_window, text="Enter Dimension Column Name", font=("Arial", 12))
        label2.pack()
        entry2 = tk.Entry(dashboard_window, font=("Arial", 12))
        entry2.pack(fill=tk.X, padx=5, pady=5)

        add_button = tk.Button(dashboard_window, text="Add Graph", font=("Arial", 10, "bold"), command=add_graph)
        add_button.pack(pady=10, padx=10)

        graph_display_label = tk.Label(dashboard_window, text="", font=("Arial", 12))
        graph_display_label.pack(pady=5)

        generate_button = tk.Button(dashboard_window, text="Generate Dashboard", font=("Arial", 10, "bold"), command=generate_dashboard)
        generate_button.pack(pady=10, padx=10)

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.set_theme()

    def set_theme(self):
        if self.theme == "light":
            self.root.configure(bg="#17202a")
            self.header_frame.configure(bg="#273746")
            self.menu_frame.configure(bg="darkgrey")
            self.main_frame.configure(bg="#ecf0f1")
            self.content_frame.configure(style="Light.TFrame")
            self.treeview_frame.configure(style="Light.TFrame")
            self.footer_frame.configure(bg="#273746")
            self.toggle_theme_button.configure(image=self.light_icon)
        else:
            self.root.configure(bg="black")
            self.header_frame.configure(bg="#001f3f")
            self.menu_frame.configure(bg="#1a1a1a")
            self.main_frame.configure(bg="#2c3e50")
            self.content_frame.configure(style="Dark.TFrame")
            self.treeview_frame.configure(style="Dark.TFrame")
            self.footer_frame.configure(bg="#001f3f")
            self.toggle_theme_button.configure(image=self.dark_icon)

    def download_data(self):
        if self.current_data is not None and isinstance(self.current_data, pd.DataFrame):
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

            if file_path:
                try:
                    self.current_data.to_csv(file_path, index=False)
                    messagebox.showinfo("Download Successful", f"Data has been successfully downloaded to:\n{file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error while saving data: {e}")
        else:
            messagebox.showwarning("No Data", "Please open a file first to load data.")


    def perform_operation(self, operation):
        if operation == "DATA CLEANING":
            self.data_cleaning(self.current_data)
        elif operation == "DATA INFORMATION":
            self.data_information()
        elif operation == "DATA VISUALIZATION":
            self.data_visualization_window()
        elif operation == "STATISTIC OF DATA":
            self.statistic_of_data(self.current_data)
        elif operation == "FORECAST":
            if self.current_data is not None:  # Check if data is loaded
                self.data_forecast_window(self.current_data)  # Pass the current_data to the forecast window
            else:
                messagebox.showerror("Error", "No data loaded. Please open a file first.")

    def statistic_of_data(self,data):
        statistics_window = tk.Toplevel(self.root)
        statistics_window.state('zoomed')
        statistics_window.title("Data Cleaning - Dealing with Empty Cells and Duplicates")
        statistics_window.configure(bg="#ecf0f1")
        
        # Header Frame of data_cleaning
        header_frame3 = tk.Frame(statistics_window, bg="#273746", height=70, bd=1, relief=tk.SOLID)
        header_frame3.pack(fill=tk.X)

        header_label = tk.Label(header_frame3, text="DATA CLEANING", font=("Arial", 20, "bold"), bg="#273746", fg="white")
        header_label.pack(pady=15)

        # Main Part Frame of data_cleaning
        main_frame3 = tk.Frame(statistics_window, bg="#ecf0f1", height=600, bd=1, relief=tk.SOLID)
        main_frame3.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Skyblue Left Frame of data_cleaning
        menu_frame3 = tk.Frame(main_frame3, bg="darkgrey", width=250, bd=1, relief=tk.SOLID)
        menu_frame3.pack(fill=tk.Y, side=tk.LEFT)
        
        # Heading for File Upload
        file_heading = tk.Label(menu_frame3, text="Functions", font=("Arial", 16, "bold"), bg="darkgrey", fg="white")
        file_heading.pack(pady=10)
        
         # Define common button style parameters
        button_bg = "#273746"
        button_fg = "#ecf0f1"
        button_width = 25
        button_height = 2
        button_padx = 10
        button_pady = 5
        
        # Add a frame to contain rows and columns labels
        status_frame = tk.Frame(statistics_window, bg="#ecf0f1")
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Add labels for total number of rows and columns
        rows_label = tk.Label(status_frame, text="Rows: {}".format(data.shape[0]), font=("Arial", 10), bg="#ecf0f1", fg="#273746")
        rows_label.pack(side=tk.LEFT, padx=10)

        columns_label = tk.Label(status_frame, text="Columns: {}".format(data.shape[1]), font=("Arial", 10), bg="#ecf0f1", fg="#273746")
        columns_label.pack(side=tk.LEFT, padx=10)
        
        # Download Button
        download_button = tk.Button(status_frame, text="Download Data", command=self.download_data, bg="#273746", fg="#ecf0f1", width=15, bd=1, relief=tk.RAISED)
        download_button.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Create buttons with the same style as the main software window buttons

        correlation_button = tk.Button(menu_frame3, text="correlation_data", command=self.correlation, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        correlation_button.pack(pady=(10, 5), padx=button_padx)

        analytics_button = tk.Button(menu_frame3, text="Replace Empty Values", command=self.replace_empty_values, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        analytics_button.pack(pady=5, padx=button_padx)

        operation3_button = tk.Button(menu_frame3, text="Replace Empty Cells Using Mean", command=self.replace_using_mean, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        operation3_button.pack(pady=5, padx=button_padx)

        operation4_button = tk.Button(menu_frame3, text="Replace Empty Cells Using Median", command=self.replace_using_median, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        operation4_button.pack(pady=5, padx=button_padx)

        operation5_button = tk.Button(menu_frame3, text="Replace Empty Cells Using Mode", command=self.replace_using_mode, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        operation5_button.pack(pady=5, padx=button_padx)

        operation6_button = tk.Button(menu_frame3, text="Remove Duplicates", command=self.remove_duplicates, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        operation6_button.pack(pady=5, padx=button_padx)

        operation7_button = tk.Button(menu_frame3, text="Correct Wrong Formats", command=self.correct_wrong_formats, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        operation7_button.pack(pady=5, padx=button_padx)
        
        operation8_button = tk.Button(menu_frame3, text="Delete Specific Column", command=self.delete_specific_column, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        operation8_button.pack(pady=5, padx=button_padx)
        
        operation9_button = tk.Button(menu_frame3, text="Add Column with Formula", command=self.add_column_with_formula, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        operation9_button.pack(pady=5, padx=button_padx)
        
        # Main Content Frame (2/3 of Main Part Frame)
        content_frame = ttk.Frame(main_frame3, style="Light.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview widget for tabular and non-tabular display
        treeview_frame = ttk.Frame(content_frame, style="Light.TFrame")
        treeview_frame.pack(expand=True, fill=tk.BOTH)

        treeview_style = ttk.Style()
        treeview_style.configure("Treeview", font=("Arial", 10), background="#ecf0f1", fieldbackground="#ecf0f1", foreground="#17202a")

        # Configure styles for Light and Dark themes
        treeview_style.configure("Light.TFrame", background="#ecf0f1")
        treeview_style.configure("Dark.TFrame", background="#2c3e50")

        treeview = ttk.Treeview(treeview_frame, show="headings", style="Treeview")
        treeview.pack(expand=True, fill=tk.BOTH)

        y_scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=treeview.yview)
        y_scrollbar.pack(side="right", fill="y")
        treeview.configure(yscrollcommand=y_scrollbar.set)

        x_scrollbar = ttk.Scrollbar(treeview_frame, orient="horizontal", command=treeview.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        treeview.configure(xscrollcommand=x_scrollbar.set)

        # Display the data in the Treeview widget
        self.display_data_in_treeview(treeview, data)
        self.treeview.bind("<Double-1>", self.on_item_double_click)

        # Footer Frame
        footer_frame = tk.Frame(statistics_window, bg="#273746", height=30, bd=1, relief=tk.SOLID)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Footer Label
        footer_label = tk.Label(footer_frame, text="© 2024 EMS - A Business Intelligence Tool", font=("Arial", 8), bg="#273746", fg="white")
        footer_label.pack(pady=5)
    
    def correlation(self):
        # Calculate the correlation matrix
        corr_matrix = self.current_data.corr()

        # Create a new Tkinter window
        correlation_window = tk.Toplevel(self.root)
        correlation_window.title("Correlation Matrix")
        correlation_window.geometry("600x400")  # Adjust size as needed

        # Create a Treeview widget in the new window
        treeview = ttk.Treeview(correlation_window, show="headings", columns=list(corr_matrix.columns))
        treeview.pack(expand=True, fill='both')

        # Define the column headings
        for col in corr_matrix.columns:
            treeview.heading(col, text=col)
            treeview.column(col, anchor="center")

        # Adding the data rows to the Treeview
        for row in corr_matrix.itertuples(index=True, name='Pandas'):
            row_data = tuple([getattr(row, col) for col in corr_matrix.columns])
            treeview.insert('', 'end', values=row_data)

        # Scrollbars for the Treeview
        scrollbar_vertical = ttk.Scrollbar(correlation_window, orient="vertical", command=treeview.yview)
        scrollbar_vertical.pack(side='right', fill='y')

        scrollbar_horizontal = ttk.Scrollbar(correlation_window, orient="horizontal", command=treeview.xview)
        scrollbar_horizontal.pack(side='bottom', fill='x')

        treeview.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)


    def data_cleaning(self, data):
        cleaning_window = tk.Toplevel(self.root)
        cleaning_window.state('zoomed')
        cleaning_window.title("Data Cleaning - Dealing with Empty Cells and Duplicates")
        cleaning_window.configure(bg="#ecf0f1")  # Background color for the cleaning window
        

        # Header Frame of data_cleaning
        header_frame2 = tk.Frame(cleaning_window, bg="#273746", height=70, bd=1, relief=tk.SOLID)
        header_frame2.pack(fill=tk.X)

        header_label = tk.Label(header_frame2, text="DATA_CLEANING", font=("Arial", 20, "bold"), bg="#273746", fg="white")
        header_label.pack(pady=15)

        # Main Part Frame of data_cleaning
        main_frame2 = tk.Frame(cleaning_window, bg="#ecf0f1", height=600, bd=1, relief=tk.SOLID)
        main_frame2.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Skyblue Left Frame of data_cleaning
        menu_frame2 = tk.Frame(main_frame2, bg="darkgrey", width=250, bd=1, relief=tk.SOLID)
        menu_frame2.pack(fill=tk.Y, side=tk.LEFT)

        # Heading for File Upload
        file_heading = tk.Label(menu_frame2, text="Functions", font=("Arial", 16, "bold"), bg="darkgrey", fg="white")
        file_heading.pack(pady=10)

        # Define common button style parameters
        button_bg = "#273746"
        button_fg = "#ecf0f1"
        button_width = 25
        button_height = 2
        button_padx = 10
        button_pady = 5

        
        # Add a frame to contain rows and columns labels
        status_frame = tk.Frame(cleaning_window, bg="#ecf0f1")
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Add labels for total number of rows and columns
        rows_label = tk.Label(status_frame, text="Rows: {}".format(data.shape[0]), font=("Arial", 10), bg="#ecf0f1", fg="#273746")
        rows_label.pack(side=tk.LEFT, padx=10)

        columns_label = tk.Label(status_frame, text="Columns: {}".format(data.shape[1]), font=("Arial", 10), bg="#ecf0f1", fg="#273746")
        columns_label.pack(side=tk.LEFT, padx=10)

        # Download Button
        download_button = tk.Button(status_frame, text="Download Data", command=self.download_data, bg="#273746", fg="#ecf0f1", width=15, bd=1, relief=tk.RAISED)
        download_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Create buttons with the same style as the main software window buttons

        remove_empty_cells_button = tk.Button(menu_frame2, text="Removing Rows of Empty Cells", command=self.remove_empty_cells, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        remove_empty_cells_button.pack(pady=(10, 5), padx=button_padx)

        replace_empty_values_button = tk.Button(menu_frame2, text="Replace Empty Values", command=self.replace_empty_values, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        replace_empty_values_button.pack(pady=5, padx=button_padx)

        replace_using_mean_button = tk.Button(menu_frame2, text="Replace Empty Cells Using Mean", command=self.replace_using_mean, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        replace_using_mean_button.pack(pady=5, padx=button_padx)

        replace_using_median_button = tk.Button(menu_frame2, text="Replace Empty Cells Using Median", command=self.replace_using_median, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        replace_using_median_button.pack(pady=5, padx=button_padx)

        replace_using_mode_button = tk.Button(menu_frame2, text="Replace Empty Cells Using Mode", command=self.replace_using_mode, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        replace_using_mode_button.pack(pady=5, padx=button_padx)

        remove_duplicates_button = tk.Button(menu_frame2, text="Remove Duplicates", command=self.remove_duplicates, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        remove_duplicates_button.pack(pady=5, padx=button_padx)

        correct_formats_button = tk.Button(menu_frame2, text="Correct Wrong Formats", command=self.correct_wrong_formats, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        correct_formats_button.pack(pady=5, padx=button_padx)

        delete_column_button = tk.Button(menu_frame2, text="Delete Specific Column", command=self.delete_specific_column, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        delete_column_button.pack(pady=5, padx=button_padx)
        
        add_column_button = tk.Button(menu_frame2, text="Add Column with Formula", command=self.add_column_with_formula, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        add_column_button.pack(pady=5, padx=button_padx)
        
        filter_button = tk.Button(menu_frame2, text="Show Numerical Columns", command=self.filter_numerical_columns, bg=button_bg, fg=button_fg, width=button_width, height=button_height)
        filter_button.pack(pady=5, padx=button_padx)


        # Main Content Frame (2/3 of Main Part Frame)
        content_frame = ttk.Frame(main_frame2, style="Light.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview widget for tabular and non-tabular display
        treeview_frame = ttk.Frame(content_frame, style="Light.TFrame")
        treeview_frame.pack(expand=True, fill=tk.BOTH)

        treeview_style = ttk.Style()
        treeview_style.configure("Treeview", font=("Arial", 10), background="#ecf0f1", fieldbackground="#ecf0f1", foreground="#17202a")

        # Configure styles for Light and Dark themes
        treeview_style.configure("Light.TFrame", background="#ecf0f1")
        treeview_style.configure("Dark.TFrame", background="#2c3e50")

        treeview = ttk.Treeview(treeview_frame, show="headings", style="Treeview")
        treeview.pack(expand=True, fill=tk.BOTH)

        y_scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=treeview.yview)
        y_scrollbar.pack(side="right", fill="y")
        treeview.configure(yscrollcommand=y_scrollbar.set)

        x_scrollbar = ttk.Scrollbar(treeview_frame, orient="horizontal", command=treeview.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        treeview.configure(xscrollcommand=x_scrollbar.set)

        # Display the data in the Treeview widget
        self.display_data_in_treeview(treeview, data)
        self.treeview.bind("<Double-1>", self.on_item_double_click)


        # Footer Frame
        footer_frame = tk.Frame(cleaning_window, bg="#273746", height=30, bd=1, relief=tk.SOLID)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Footer Label
        footer_label = tk.Label(footer_frame, text="© 2024 EMS - A Business Intelligence Tool", font=("Arial", 8), bg="#273746", fg="white")
        footer_label.pack(pady=5)


    def display_data_in_treeview(self, treeview, data):
        if data is not None and isinstance(data, pd.DataFrame):
            columns = list(data.columns)
            treeview["columns"] = columns
            for col in columns:
                treeview.heading(col, text=col)
            for index, row in data.iterrows():
                treeview.insert("", "end", values=list(row))

    def delete_specific_column(self):
        if self.current_data is not None and isinstance(self.current_data, pd.DataFrame):
            column_name = simpledialog.askstring("Delete Column", "Enter the column name to delete:")
            if column_name in self.current_data.columns:
                try:
                    self.current_data.drop(column_name, axis=1, inplace=True)
                    self.display_in_treeview(self.current_data)
                    messagebox.showinfo("Delete Column", f"Column '{column_name}' deleted successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error deleting column: {e}")
            else:
                messagebox.showwarning("Column Not Found", f"Column '{column_name}' not found.")
        else:
            messagebox.showwarning("No Data", "Please open a file first to load data.")
    
    def filter_numerical_columns(self):
        # Assuming 'data' is your DataFrame
        numerical_data = self.current_data.select_dtypes(include=['int64', 'float64'])
        # Clear the existing data in the Treeview
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        self.current_data = numerical_data
        self.display_in_treeview(self.current_data)
        
    def on_item_double_click(self, event):
        # Get the item clicked
        selected_item = self.treeview.identify_row(event.y)
        if not selected_item:
            # In case the click didn't happen on an item
            return
        
        # Get the column clicked
        column_id = self.treeview.identify_column(event.x)
        
        column_index = int(column_id.strip('#')) - 1  # Convert to 0-based index
        
        # Get the old value from the clicked cell
        old_value = self.treeview.item(selected_item, 'values')[column_index]
        
        # Create the pop-up window (your existing code, adjusted for column_index)
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Cell (Column: {column_index + 1})")
        edit_window.geometry("300x100")
        
        new_value_entry = tk.Entry(edit_window)
        new_value_entry.pack(pady=10)
        new_value_entry.insert(0, old_value)
        
        def save_new_value(event=None):  # Allow optional event argument
            new_value = new_value_entry.get()
            row_index = self.treeview.index(selected_item)
            self.current_data.iloc[row_index, column_index] = new_value  # Update DataFrame
            current_values = list(self.treeview.item(selected_item, 'values'))
            current_values[column_index] = new_value  # Update the specific cell in the values list
            self.treeview.item(selected_item, values=current_values)  # Update Treeview
            edit_window.destroy()
            
        save_button = tk.Button(edit_window, text="Save", command=save_new_value)
        save_button.pack(pady=10)
        new_value_entry.bind("<Return>", save_new_value)



    def add_column_with_formula(self):
        if self.current_data is not None and isinstance(self.current_data, pd.DataFrame):
            formula = simpledialog.askstring("Add Column", "Enter the formula to calculate new column values:\nExample: col1 + col2 * col3")
            new_column_name = simpledialog.askstring("Add Column", "Enter the name for the new column:")
            if formula and new_column_name:
                try:
                    # Use DataFrame.eval() to evaluate the formula
                    self.current_data[new_column_name] = self.current_data.eval(formula)
                    messagebox.showinfo("Add Column", f"New column '{new_column_name}' added successfully.")
                    self.display_in_treeview(self.current_data)
                except Exception as e:
                    messagebox.showerror("Error", f"Error adding new column: {e}")
        else:
            messagebox.showwarning("No Data", "Please open a file first to load data.")

    def remove_duplicates(self):
        if self.current_data is not None and isinstance(self.current_data, pd.DataFrame):
            try:
                # Remove duplicates
                self.current_data = self.current_data.drop_duplicates()

                # Refresh the Treeview
                self.display_in_treeview(self.current_data)

                messagebox.showinfo("Remove Duplicates", "Duplicate rows removed successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error removing duplicates: {e}")
        else:
            messagebox.showwarning("No Data", "Please open a file first to load data.")


    def correct_wrong_formats(self):
        if self.current_data is not None and isinstance(self.current_data, pd.DataFrame):
            try:
                # Specify the columns you want to correct (modify this based on your requirements)
                date_columns = ["DateColumn1", "DateColumn2"]

                # Correct the format of date columns
                for column in date_columns:
                    if column in self.current_data.columns:
                        self.current_data[column] = pd.to_datetime(self.current_data[column], errors='coerce').dt.strftime('%d-%b-%y')

                # Update the Treeview
                self.display_in_treeview(self.current_data)

                messagebox.showinfo("Correct Formats", "Wrong formats corrected successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error correcting formats: {e}")
        else:
            messagebox.showwarning("No Data", "Please open a file first to load data.")

        
    def remove_empty_cells(self):
        if self.current_data is not None and isinstance(self.current_data, pd.DataFrame):
            # Ask the user for the column name
            column_name = askstring("Column Name", "Enter the column name:")

            if column_name is not None:
                try:
                    # Remove rows with empty cells or cells containing any value
                    self.current_data = self.current_data.dropna(subset=[column_name], how='any')
                
                    self.display_in_treeview(self.current_data)
                    messagebox.showinfo("Remove Cells", f"All rows with empty cells in column '{column_name}' removed successfully.")
                except KeyError:
                    messagebox.showwarning("Column Not Found", f"Column '{column_name}' not found.")
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid column name.")
        else:
            messagebox.showwarning("No Data", "Please open a file first to load data.")

    def replace_empty_values(self):
        if self.current_data is not None and isinstance(self.current_data, pd.DataFrame):
            # Ask the user for the column name
            column_name = askstring("Column Name", "Enter the column name:")

            if column_name is not None:
                try:
                    # Ask the user for the row number (if any)
                    row_number_input = askstring("Row Number", "Enter the row number (leave blank to replace all):")
                
                    if row_number_input:
                        row_number = int(row_number_input) - 1  # Adjust for zero-based indexing
                        if row_number < 0 or row_number >= len(self.current_data):
                            raise ValueError("Invalid row number.")
                    else:
                        row_number = None

                    # Ask the user for the value to replace NaN
                    replacement_value = askstring("Replacement Value", "Enter the value to replace NaN:")

                    if row_number is not None:
                        # Replace NaN in a specific row
                        self.current_data.at[row_number, column_name] = replacement_value
                        messagebox.showinfo("Replace Value", f"Value in row {row_number + 1}, column '{column_name}' replaced successfully.")
                    else:
                        # Replace all NaN values in the specified column
                        self.current_data[column_name].fillna(replacement_value, inplace=True)
                        messagebox.showinfo("Replace Value", f"All NaN values in column '{column_name}' replaced successfully.")

                    # Refresh the Treeview
                    self.display_in_treeview(self.current_data)

                except ValueError as e:
                    messagebox.showwarning("Invalid Input", str(e))
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid column name.")
        else:
            messagebox.showwarning("No Data", "Please open a file first to load data.")


    def download_data(self):
        if self.current_data is not None and isinstance(self.current_data, pd.DataFrame):
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

            if file_path:
                try:
                    self.current_data.to_csv(file_path, index=False)
                    messagebox.showinfo("Download Successful", f"Data has been successfully downloaded to:\n{file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error while saving data: {e}")
        else:
            messagebox.showwarning("No Data", "Please open a file first to load data.")
            
    def replace_using_mean(self):
        if self.current_data is not None and isinstance(self.current_data, pd.DataFrame):
            # Ask the user for the column name
            column_name = askstring("Column Name", "Enter the column name:")

            if column_name is not None:
                try:
                    # Ask the user for the row number (if any)
                    row_number_input = askstring("Row Number", "Enter the row number (leave blank to replace all):")

                    if row_number_input:
                        row_number = int(row_number_input) - 1  # Adjust for zero-based indexing
                        if row_number < 0 or row_number >= len(self.current_data):
                            raise ValueError("Invalid row number.")
                    else:
                        row_number = None

                    # Calculate the mean of the specified column
                    column_mean = self.current_data[column_name].mean()

                    if row_number is not None:
                        # Replace NaN in a specific row with the mean
                        self.current_data.at[row_number, column_name] = column_mean
                        messagebox.showinfo("Replace Value", f"Value in row {row_number + 1}, column '{column_name}' replaced with the mean: {column_mean}")
                    else:
                        # Replace all NaN values in the specified column with the mean
                        self.current_data[column_name].fillna(column_mean, inplace=True)
                        messagebox.showinfo("Replace Value", f"All NaN values in column '{column_name}' replaced with the mean: {column_mean}")
                    
                    # Refresh the Treeview
                    self.display_in_treeview(self.current_data)

                except ValueError as e:
                    messagebox.showwarning("Invalid Input", str(e))
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid column name.")
        else:
            messagebox.showwarning("No Data", "Please open a file first to load data.")
    
    def replace_using_median(self):
        if self.current_data is not None and isinstance(self.current_data, pd.DataFrame):
            # Ask the user for the column name
            column_name = askstring("Column Name", "Enter the column name:")

            if column_name is not None:
                try:
                    # Convert the column to numeric type
                    self.current_data[column_name] = pd.to_numeric(self.current_data[column_name], errors='coerce')

                    # Ask the user for the row number (if any)
                    row_number_input = askstring("Row Number", "Enter the row number (leave blank to replace all):")

                    if row_number_input:
                        row_number = int(row_number_input) - 1  # Adjust for zero-based indexing
                        if row_number < 0 or row_number >= len(self.current_data):
                            raise ValueError("Invalid row number.")
                    else:
                        row_number = None

                    # Calculate the median of the specified column
                    column_median = self.current_data[column_name].median()

                    if row_number is not None:
                        # Replace NaN in a specific row with the median
                        self.current_data.at[row_number, column_name] = column_median
                        messagebox.showinfo("Replace Value", f"Value in row {row_number + 1}, column '{column_name}' replaced with the median: {column_median}")
                    else:
                        # Replace all NaN values in the specified column with the median
                        self.current_data[column_name].fillna(column_median, inplace=True)
                        messagebox.showinfo("Replace Value", f"All NaN values in column '{column_name}' replaced with the median: {column_median}")

                    # Refresh the Treeview
                    self.display_in_treeview(self.current_data)

                except ValueError as e:
                    messagebox.showwarning("Invalid Input", str(e))
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid column name.")
        else:
            messagebox.showwarning("No Data", "Please open a file first to load data.")


    def replace_using_mode(self):
        if self.current_data is not None and isinstance(self.current_data, pd.DataFrame):
            # Ask the user for the column name
            column_name = askstring("Column Name", "Enter the column name:")

            if column_name is not None:
                try:
                    # Convert the column to numeric type
                    self.current_data[column_name] = pd.to_numeric(self.current_data[column_name], errors='coerce')

                    # Ask the user for the row number (if any)
                    row_number_input = askstring("Row Number", "Enter the row number (leave blank to replace all):")

                    if row_number_input:
                        row_number = int(row_number_input) - 1  # Adjust for zero-based indexing
                        if row_number < 0 or row_number >= len(self.current_data):
                            raise ValueError("Invalid row number.")
                    else:
                        row_number = None

                    # Calculate the mode of the specified column
                    column_mode = float(scipy_mode(self.current_data[column_name].dropna()).mode)

                    if row_number is not None:
                        # Replace NaN in a specific row with the mode
                        self.current_data.at[row_number, column_name] = column_mode
                        messagebox.showinfo("Replace Value", f"Value in row {row_number + 1}, column '{column_name}' replaced with the mode: {column_mode}")
                    else:
                        # Replace all NaN values in the specified column with the mode
                        self.current_data[column_name].fillna(column_mode, inplace=True)
                        messagebox.showinfo("Replace Value", f"All NaN values in column '{column_name}' replaced with the mode: {column_mode}")

                    # Refresh the Treeview
                    self.display_in_treeview(self.current_data)

                except ValueError as e:
                    messagebox.showwarning("Invalid Input", str(e))
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid column name.")
        else:
            messagebox.showwarning("No Data", "Please open a file first to load data.")

    def update_data_cleaning_window_data(self):
        if self.data_cleaning_window and self.cleaning_window_data is not None:
            self.display_data_in_treeview(self.treeview, self.cleaning_window_data)  # Update data in the cleaning window
            
    def initialize_data_cleaning_window(self):
        self.data_cleaning_window = tk.Toplevel(self.root)
        self.data_cleaning_window.title("Data Cleaning")

    def show_data_info(self):
        if self.current_data is not None and isinstance(self.current_data, pd.DataFrame):
            information_window = tk.Toplevel(self.root)
            information_window.title("Data Information - Displaying Data Information")
            information_window.configure(bg="#ecf0f1")
            information_window.state("zoomed")  # Open the window in maximized size

            # Footer Frame
            footer_frame = tk.Frame(information_window, bg="#273746", height=30, bd=1, relief=tk.SOLID)
            footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

            # Footer Label
            footer_label = tk.Label(footer_frame, text="© 2024 EMS - A Business Intelligence Tool", font=("Arial", 8), bg="#273746", fg="white")
            footer_label.pack(pady=5)

            # Header Frame of data_information
            header_frame_info_data = tk.Frame(
                information_window,
                bg="#273746",
                height=70,
                bd=1,
                relief=tk.SOLID
            )
            header_frame_info_data.pack(fill=tk.X)

            header_label_info_data = tk.Label(
                header_frame_info_data,
                text="DATA INFORMATION",
                font=("Arial", 20, "bold"),
                bg="#273746",
                fg="white"
            )
            header_label_info_data.pack(pady=15)

            # Display dataset information in a Treeview
            info_treeview = ttk.Treeview(
                information_window,
                columns=("Column", "Data Type", "Unique Values", "Missing Values"),
                show="headings",
                selectmode="browse"
            )
            info_treeview.heading("Column", text="Column")
            info_treeview.heading("Data Type", text="Data Type")
            info_treeview.heading("Unique Values", text="Unique Values")
            info_treeview.heading("Missing Values", text="Missing Values")

            for col in self.current_data.columns:
                data_type = str(self.current_data[col].dtype)
                unique_values = len(self.current_data[col].unique())
                missing_values = self.current_data[col].isnull().sum()

                info_treeview.insert("", "end", values=(col, data_type, unique_values, missing_values))

            info_treeview.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            # Bind cursor to the first treeview
            info_treeview.bind("<Enter>", lambda event: information_window.config(cursor="hand2"))
            info_treeview.bind("<Leave>", lambda event: information_window.config(cursor=""))

            # Display dataset information in a Treeview
            info_treeview_summary = ttk.Treeview(
                information_window,
                columns=("Info", "Value"),
                show="headings",
                selectmode="browse"
            )
            info_treeview_summary.heading("Info", text="Info")
            info_treeview_summary.heading("Value", text="Value")

            # Add rows for each piece of information
            info_treeview_summary.insert("", "end", values=("Number of Rows", len(self.current_data)))
            info_treeview_summary.insert("", "end", values=("Number of Columns", len(self.current_data.columns)))
            info_treeview_summary.insert("", "end", values=("Column Names", ", ".join(self.current_data.columns)))
            info_treeview_summary.insert("", "end", values=("Data Types", "\n".join([f"{col}: {dtype}" for col, dtype in zip(self.current_data.columns, self.current_data.dtypes)])))
            info_treeview_summary.insert("", "end", values=("Summary Statistics", ""))

            for col in self.current_data.columns:
                summary_stats = self.current_data[col].describe().to_dict()
                for stat, value in summary_stats.items():
                    info_treeview_summary.insert("", "end", values=(f"{col} - {stat.capitalize()}", value))

            info_treeview_summary.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            # Bind cursor to the second treeview
            info_treeview_summary.bind("<Enter>", lambda event: information_window.config(cursor="hand2"))
            info_treeview_summary.bind("<Leave>", lambda event: information_window.config(cursor=""))

        else:
            messagebox.showwarning("No Data", "Please open a file first to load data.")



    def data_visualization_window(self):
        graph_options = ["Bar Plot", "Histogram", "Scatter Plot", "Box Plot", "Pie Chart", "Line Plot", "Area Plot", "Violin Plot"]
        def update_graph_and_description():
            selected_graphs = graph_listbox.curselection()
            if selected_graphs:
                description_text.delete("1.0", tk.END)
                for index in selected_graphs:
                    selected_graph_index = index
                    graph_name = graph_options[selected_graph_index]
                    column1 = entry1.get()
                    column2 = entry2.get()
                if graph_name == "Bar Plot":
                    description_text.insert(tk.END, "This is a bar plot.\n\n")
                    description_text.insert(tk.END, "A bar plot represents categorical data with rectangular bars. "
                                                    "The height of the bars indicates the frequency or value of each category.\n")
                elif graph_name == "Histogram":
                    description_text.insert(tk.END, "This is a histogram.\n\n")
                    description_text.insert(tk.END, "A histogram is used to visualize the distribution of numerical data. "
                                                    "It consists of bins along the x-axis and the frequency or density of "
                                                    "observations in each bin on the y-axis.\n")
                elif graph_name == "Scatter Plot":
                    description_text.insert(tk.END, "This is a scatter plot.\n\n")
                    description_text.insert(tk.END, "A scatter plot is used to visualize the relationship between two numerical "
                                                    "variables. Each point represents an observation, with the x-coordinate "
                                                    "representing one variable and the y-coordinate representing the other.\n")
                elif graph_name == "Box Plot":
                    description_text.insert(tk.END, "This is a box plot.\n\n")
                    description_text.insert(tk.END, "A box plot displays the distribution of numerical data and identifies outliers. "
                                                    "The box represents the interquartile range (IQR), with the median marked by "
                                                    "a line inside the box. The whiskers extend to the minimum and maximum values, "
                                                    "excluding outliers.\n")
                elif graph_name == "Pie Chart":
                    description_text.insert(tk.END, "This is a pie chart.\n\n")
                    description_text.insert(tk.END, "A pie chart is used to show the proportion of different categories in a dataset. "
                                                    "Each slice of the pie represents a category, and the size of the slice corresponds "
                                                    "to the proportion of the category in the dataset.\n")
                elif graph_name == "Line Plot":
                    description_text.insert(tk.END, "This is a line plot.\n\n")
                    description_text.insert(tk.END, "A line plot is used to visualize the trend of numerical data over time or "
                                                    "another continuous variable. It connects data points with straight lines, "
                                                    "emphasizing the relationship between successive data points.\n")
                elif graph_name == "Area Plot":
                    description_text.insert(tk.END, "This is an area plot.\n\n")
                    description_text.insert(tk.END, "An area plot is similar to a line plot but fills the area under the line. "
                                                    "It is useful for visualizing cumulative totals or proportions over time or "
                                                    "another continuous variable.\n")
                elif graph_name == "Violin Plot":
                    description_text.insert(tk.END, "This is a violin plot.\n\n")
                    description_text.insert(tk.END, "A violin plot combines the features of a box plot and a kernel density plot. "
                                                    "It displays the distribution of numerical data and provides insights into the "
                                                    "probability density of the data at different values.\n")
                self.generate_graph(graph_name, column1, column2)

        # Create a new Toplevel window
        visualization_window = tk.Toplevel(self.root)
        visualization_window.title("Data Visualization")
        

        # Apply the same theme as the parent window
        if self.theme == "light":
            visualization_window.configure(bg="#ecf0f1")
        else:
            visualization_window.configure(bg="#2c3e50")

        visualization_window.state("zoomed")
        
        # Header Frame of data_visualization_window
        header_frame_visualization = tk.Frame(visualization_window, bg="#273746", height=70, bd=1, relief=tk.SOLID)
        header_frame_visualization.pack(fill=tk.X)

        header_label_visualization = tk.Label(header_frame_visualization, text="Graphs and Plots", font=("Arial", 20, "bold"), bg="#273746", fg="white")
        header_label_visualization.pack(pady=15)

        # Main Part Frame of data_visualization_window
        main_frame_visualization = tk.Frame(visualization_window, bg="#ecf0f1", bd=1, relief=tk.SOLID)
        main_frame_visualization.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Frame for displaying column names
        left_frame = tk.Frame(main_frame_visualization, bg="#d5dbdb", bd=1, relief=tk.SOLID)
        left_frame.pack(fill=tk.Y, side=tk.LEFT, padx=(10, 5), pady=10)

        # Get column names and their data types
        measured_columns = []  # For columns with numeric data types
        dimension_columns = []  # For columns with non-numeric data types

        for column in self.current_data.columns:
            if pd.api.types.is_numeric_dtype(self.current_data[column]):
                measured_columns.append(column)
            else:
                dimension_columns.append(column)

        # List of all possible measured columns
        measured_columns = [col for col in self.current_data.columns if pd.api.types.is_numeric_dtype(self.current_data[col])]
        
        # Measured column box
        measured_frame = tk.Frame(left_frame, bg="#d5dbdb")
        measured_frame.pack(pady=(5, 10), padx=10, fill=tk.BOTH, expand=True)

        measured_label = tk.Label(measured_frame, text="Measured Columns", font=("Arial", 12, "bold"), bg="#d5dbdb", bd=1, relief=tk.SOLID, padx=10, pady=5)
        measured_label.pack(padx=10, anchor=tk.W)

        measured_scrollbar = Scrollbar(measured_frame, orient="vertical")
        measured_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        measured_listbox = tk.Listbox(measured_frame, selectmode="browse", font=("Arial", 10), bd=1, width=20, relief=tk.SOLID, yscrollcommand=measured_scrollbar.set)
        for column in measured_columns:
            measured_listbox.insert(tk.END, column)
        measured_listbox.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        measured_scrollbar.config(command=measured_listbox.yview)

        # List of all possible dimension columns
        dimension_columns = [col for col in self.current_data.columns if not pd.api.types.is_numeric_dtype(self.current_data[col])]
        
        # Dimension column box
        dimension_frame = tk.Frame(left_frame, bg="#d5dbdb")
        dimension_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        dimension_label = tk.Label(dimension_frame, text="Dimension Columns", font=("Arial", 12, "bold"), bg="#d5dbdb", bd=1, relief=tk.SOLID, padx=10, pady=5)
        dimension_label.pack(padx=10, anchor=tk.W)

        dimension_scrollbar = Scrollbar(dimension_frame, orient="vertical")
        dimension_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        dimension_listbox = tk.Listbox(dimension_frame, selectmode="browse", width=25, font=("Arial", 10), bd=1, relief=tk.SOLID, yscrollcommand=dimension_scrollbar.set)
        for column in dimension_columns:
            dimension_listbox.insert(tk.END, column)
        dimension_listbox.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        dimension_scrollbar.config(command=dimension_listbox.yview)

        # Middle Frame for graph options
        middle_frame = tk.Frame(main_frame_visualization, bg="#ecf0f1", bd=1, relief=tk.SOLID)
        middle_frame.pack(fill=tk.Y, side=tk.LEFT, padx=10, pady=10)
        
        # Create the left box for Entry 1
        left_box = tk.Frame(middle_frame, bg="#f0f0f0", padx=20, pady=20, bd=2, relief=tk.RAISED)
        left_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)
        label1 = tk.Label(left_box, text="Enter Measured Column Name", font=("Arial", 12))
        label1.pack()
        entry1 = tk.Entry(left_box, font=("Arial", 12), bd=2, relief=tk.SOLID)
        entry1.pack(fill=tk.X, padx=5, pady=5)

        # Create the right box for Entry 2
        right_box = tk.Frame(middle_frame, bg="#f0f0f0", padx=20, pady=20, bd=2, relief=tk.RAISED)
        right_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)
        label2 = tk.Label(right_box, text="Enter Dimension Column Name", font=("Arial", 12))
        label2.pack()
        entry2 = tk.Entry(right_box, font=("Arial", 12), bd=2, relief=tk.SOLID)
        entry2.pack(fill=tk.X, padx=5, pady=5)

        def fill_measured_column(event):
            selected_measure = measured_listbox.curselection()
            if selected_measure:
                selected_measure_index = selected_measure[0]
                selected_measure_name = measured_columns[selected_measure_index]
                entry1.delete(0, tk.END)
                entry1.insert(tk.END, selected_measure_name)

        def fill_dimension_column(event):
            selected_dimension = dimension_listbox.curselection()
            if selected_dimension:
                selected_dimension_index = selected_dimension[0]
                selected_dimension_name = dimension_columns[selected_dimension_index]
                entry2.delete(0, tk.END)
                entry2.insert(tk.END, selected_dimension_name)

        entry1.bind("<Return>", fill_measured_column)
        entry2.bind("<Return>", fill_dimension_column)

        # List of all possible graphs and plots
        graph_options = ["Bar Plot", "Histogram", "Scatter Plot", "Box Plot", "Pie Chart", "Line Plot", "Area Plot", "Violin Plot"]


        # Graph options label and listbox
        graph_label = tk.Label(left_frame, text="Graph Options...", font=("Arial", 12, "bold"), bg="#d5dbdb", bd=1, relief=tk.SOLID, padx=10, pady=5)
        graph_label.pack(pady=10, anchor=tk.W)

        graph_scrollbar = Scrollbar(left_frame, orient="vertical")
        graph_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        graph_listbox = tk.Listbox(left_frame, selectmode="browse", height=len(graph_options), font=("Arial", 12), width=20, bd=1, relief=tk.SOLID, yscrollcommand=graph_scrollbar.set)
        for option in graph_options:
            graph_listbox.insert(tk.END, option)
        graph_listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        graph_scrollbar.config(command=graph_listbox.yview)
        graph_listbox.configure(cursor="hand2")  # Set cursor here


        # Right Frame for displaying graph description
        right_frame = tk.Frame(main_frame_visualization, bg="#ecf0f1", bd=1, relief=tk.SOLID)
        right_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT, padx=10, pady=10)

        # Description label for the selected graph
        description_label = tk.Label(right_frame, text="Graph Description", font=("Arial", 12, "bold"), bg="#ecf0f1")
        description_label.pack(pady=10, padx=10, anchor=tk.W)

        description_text = tk.Text(right_frame, height=2, wrap="word",  bd=1, relief=tk.SOLID)
        description_text.pack(pady=5, padx=10,  fill=tk.BOTH, expand=True)

        # Add Dashboard Button next to Generate Graph Button
        dashboard_button = tk.Button(right_frame, text="Dashboard", font=("Arial", 10, "bold"), bd=2, relief=tk.SOLID, command=self.dashboard)
        dashboard_button.pack(pady=10, padx=10, anchor=tk.E)

        # Button to generate the graph
        generate_button = tk.Button(right_frame, text="Generate Graph", font=("Arial", 12, "bold"), command=update_graph_and_description, bd=2, relief=tk.SOLID)
        generate_button.pack(pady=10, padx=10, fill=tk.X, anchor=tk.E) 

        # Footer Frame
        footer_frame = tk.Frame(visualization_window, bg="#273746", height=30, bd=1, relief=tk.SOLID)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        footer_label = tk.Label(footer_frame, text="© 2024 EMS - A Business Intelligence Tool", font=("Arial", 8), bg="#273746", fg="white")
        footer_label.pack(pady=5)

        # Ensure the window remains open
        visualization_window.mainloop()

    def generate_graph(self, graph_name, column1, column2, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))  # Increase figure size

        # Custom color palettes for each plot type
        if graph_name == "Bar Plot":
            sns.set_palette("pastel")
        elif graph_name == "Histogram":
            sns.set_palette("deep")
        elif graph_name == "Scatter Plot":
            sns.set_palette("bright")
        elif graph_name == "Box Plot":
            sns.set_palette("colorblind")
        elif graph_name == "Pie Chart":
            sns.set_palette("husl")
        elif graph_name == "Line Plot":
            sns.set_palette("muted")
        elif graph_name == "Area Plot":
            sns.set_palette("dark")
        elif graph_name == "Violin Plot":
            sns.set_palette("Set3")


        if graph_name == "Pie Chart":
            filtered_data = self.current_data[[column1, column2]].dropna()

            total_count = filtered_data[column1].sum()
            labels = [textwrap.fill(str(label), width=15) for label in filtered_data[column2] if not pd.isna(label)]
            sizes = filtered_data[column1]
            threshold = 5  

            # Sort sizes and labels in descending order
            sorted_sizes, sorted_labels = zip(*sorted(zip(sizes, labels), reverse=True))

            # Keep the first 4 values with their labels
            main_sizes = list(sorted_sizes[:4])
            main_labels = list(sorted_labels[:4])

            # Calculate the sum of the remaining sizes
            other_percentage = sum(sorted_sizes[4:]) / total_count * 100
            other_label = 'Other'

            # Add the aggregate percentage of smaller values to the main sizes
            main_sizes.append(other_percentage)
            main_labels.append(other_label)

            # Define colors for each section of the pie chart
            colors = sns.color_palette('pastel', len(main_sizes))

            # Set a different color for the "Other" category
            colors[-1] = 'grey'

            ax.pie(main_sizes, labels=main_labels, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 10}, colors=colors)
            ax.set_title("Pie Chart", fontsize=16, fontweight='bold')
            ax.axis('equal')  
            ax.legend(loc="center left", fontsize=10, bbox_to_anchor=(1, 0, 0.5, 1))  
 

        elif graph_name == "Bar Plot":
            sns.barplot(x=column1, y=column2, data=self.current_data, ax=ax)
            ax.set_title("Bar Plot", fontsize=16, fontweight='bold')
            ax.set_xlabel(column1, fontsize=14, fontweight='bold')
            ax.set_ylabel(column2, fontsize=14, fontweight='bold')
        elif graph_name == "Histogram":
            sns.histplot(data=self.current_data[column1], kde=True, ax=ax)
            ax.set_title("Histogram", fontsize=16, fontweight='bold')
            ax.set_xlabel(column1, fontsize=14, fontweight='bold')
            ax.set_ylabel(column2, fontsize=14, fontweight='bold')
        elif graph_name == "Scatter Plot":
            sns.scatterplot(x=column1, y=column2, data=self.current_data, ax=ax, s=50, marker='o')
            ax.set_title("Scatter Plot", fontsize=16, fontweight='bold')
            ax.set_xlabel(column1, fontsize=14, fontweight='bold')
            ax.set_ylabel(column2, fontsize=14, fontweight='bold')
        elif graph_name == "Box Plot":
            sns.boxplot(x=column1, y=column2, data=self.current_data, ax=ax)
            ax.set_title("Box Plot", fontsize=16, fontweight='bold')
            ax.set_xlabel(column1, fontsize=14, fontweight='bold')
            ax.set_ylabel(column2, fontsize=14, fontweight='bold')
            ax.legend([column2], fontsize=12)
        elif graph_name == "Line Plot":
            sns.lineplot(x=column1, y=column2, data=self.current_data, ax=ax, marker='o')
            ax.set_title("Line Plot", fontsize=16, fontweight='bold')
            ax.set_xlabel(column1, fontsize=14, fontweight='bold')
            ax.set_ylabel(column2, fontsize=14, fontweight='bold')
        elif graph_name == "Area Plot":
            sns.lineplot(x=column1, y=column2, data=self.current_data, color='skyblue', ax=ax, marker='o')
            ax.fill_between(self.current_data[column1], self.current_data[column2], color="skyblue", alpha=0.4)
            ax.set_title("Area Plot", fontsize=16, fontweight='bold')
            ax.set_xlabel(column1, fontsize=14, fontweight='bold')
            ax.set_ylabel(column2, fontsize=14, fontweight='bold')
        elif graph_name == "Violin Plot":
            sns.violinplot(x=column1, y=column2, data=self.current_data, ax=ax)
            ax.set_title("Violin Plot", fontsize=16, fontweight='bold')
            ax.set_xlabel(column1, fontsize=14, fontweight='bold')
            ax.set_ylabel(column2, fontsize=14, fontweight='bold')

        ax.grid(True, linestyle=':', linewidth=0.5, color='gray', alpha=0.5)  # Add grid lines with dotted pattern
        plt.tight_layout()  # Adjust layout for better spacing
        plt.show()



    def data_forecast_window(self, data):
        # Create a new Toplevel window
        forecast_window = tk.Toplevel(self.root)
        forecast_window.title("Data Forecast")

        # Apply the same theme as the parent window
        if self.theme == "light":
            forecast_window.configure(bg="#ecf0f1")
        else:
            forecast_window.configure(bg="#2c3e50")

        forecast_window.state("zoomed")  # Maximize the window

        # Header Frame of data_forecast_window
        header_frame_forecast = tk.Frame(forecast_window, bg="#273746", height=70, bd=1, relief=tk.SOLID)
        header_frame_forecast.pack(fill=tk.X)

        header_label_forecast = tk.Label(header_frame_forecast, text="Data Forecasting", font=("Arial", 20, "bold"), bg="#273746", fg="white")
        header_label_forecast.pack(pady=15)

        # Main Part Frame of data_forecast_window
        main_frame_forecast = tk.Frame(forecast_window, bg="#ecf0f1", bd=1, relief=tk.SOLID)
        main_frame_forecast.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Skyblue Left Frame of data_forecast_window
        menu_frame_forecast = tk.Frame(main_frame_forecast, bg="darkgrey", width=250, bd=1, relief=tk.SOLID)
        menu_frame_forecast.pack(fill=tk.Y, side=tk.LEFT)

        # Treeview widget to display data
        treeview = ttk.Treeview(main_frame_forecast, show="headings", style="Treeview")
        treeview["columns"] = tuple(data.columns)

        # Configure styles for Light and Dark themes
        treeview_style = ttk.Style()
        treeview_style.configure("Treeview", font=("Arial", 10), background="#ecf0f1", fieldbackground="#ecf0f1", foreground="#17202a")
        treeview_style.configure("Light.TFrame", background="#ecf0f1")
        treeview_style.configure("Dark.TFrame", background="#2c3e50")

        # Add columns to the Treeview
        for col in data.columns:
            treeview.heading(col, text=col)
            treeview.column(col, anchor="center")

        treeview.pack(expand=True, fill=tk.BOTH)

        # Insert data rows
        for index, row in data.iterrows():
            treeview.insert("", tk.END, values=tuple(row))

        # Scrollbars for Treeview
        y_scrollbar = ttk.Scrollbar(main_frame_forecast, orient="vertical", command=treeview.yview)
        y_scrollbar.pack(side="right", fill="y")
        treeview.configure(yscrollcommand=y_scrollbar.set)

        x_scrollbar = ttk.Scrollbar(main_frame_forecast, orient="horizontal", command=treeview.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        treeview.configure(xscrollcommand=x_scrollbar.set)


        # Heading for Functions
        functions_heading = tk.Label(menu_frame_forecast, text="Functions", font=("Arial", 16, "bold"), bg="darkgrey", fg="white")
        functions_heading.pack(pady=10)

        # Define common button style parameters
        button_bg = "#273746"
        button_fg = "#ecf0f1"
        button_width = 25
        button_height = 2
        button_padx = 10
        button_pady = 5

        # Add machine learning buttons
        machine_learning_buttons = tk.Frame(menu_frame_forecast, bg="#ecf0f1")
        machine_learning_buttons.pack(fill=tk.X, padx=10, pady=10)

        # Add button for linear regression
        linear_regression_button = tk.Button(menu_frame_forecast, text="Apply Linear Regression", command=self.apply_linear_regression, bg="#273746", fg="#ecf0f1", width=25, height=2)
        linear_regression_button.pack(pady=5)

        # Add button for Multiple regression
        Multiple_regression_button = tk.Button(menu_frame_forecast, text="Apply Multiple Regression", command=self.apply_multiple_regression, bg="#273746", fg="#ecf0f1", width=25, height=2)
        Multiple_regression_button.pack(pady=5)

        # Add button for Polynomial regression
        Polynomial_regression_button = tk.Button(menu_frame_forecast, text="Apply Polynomial Regression", command=self.apply_polynomial_regression, bg="#273746", fg="#ecf0f1", width=25, height=2)
        Polynomial_regression_button.pack(pady=5)

        # Add button for Scalling
        Scalling_button = tk.Button(menu_frame_forecast, text="Apply Scale", command=lambda: self.update_forecast_window(data), bg="#273746", fg="#ecf0f1", width=25, height=2)
        Scalling_button.pack(pady=5)

        # Add button for Decision Tree regression
        decision_tree_button = tk.Button(menu_frame_forecast, text="Apply Decision Tree", command=self.apply_decision_tree, bg="#273746", fg="#ecf0f1", width=25, height=2)
        decision_tree_button.pack(pady=5)


        # Footer Frame
        footer_frame_forecast = tk.Frame(forecast_window, bg="#273746", height=30, bd=1, relief=tk.SOLID)
        footer_frame_forecast.pack(fill=tk.X, side=tk.BOTTOM)

        # Footer Label
        footer_label_forecast = tk.Label(footer_frame_forecast, text="© 2024 EMS - A Business Intelligence Tool", font=("Arial", 8), bg="#273746", fg="white")
        footer_label_forecast.pack(pady=5)

        # Ensure the window remains open
        forecast_window.mainloop()

    def apply_linear_regression(self):
        # Check if data is available
        if self.current_data is None:
            messagebox.showerror("Error", "No data available for linear regression.")
            return

        # Get the target variable from the user
        target_variable = simpledialog.askstring("Select Variable", "Enter name of the target variable:")
        if target_variable is None:
            messagebox.showerror("Error", "Please specify the target variable.")
            return

        # Check if the target variable exists in the DataFrame
        if target_variable not in self.current_data.columns:
            messagebox.showerror("Error", "Selected target variable not found in data.")
            return

        # Get the independent variable (only one column)
        independent_variable = simpledialog.askstring("Select Variable", "Enter name of the independent variable:")
        if independent_variable is None:
            messagebox.showerror("Error", "Please specify the independent variable.")
            return

        # Check if the independent variable exists in the DataFrame
        if independent_variable not in self.current_data.columns:
            messagebox.showerror("Error", "Selected independent variable not found in data.")
            return

        # Convert categorical columns to numerical values
        data = self.current_data.copy()  # Create a copy to avoid modifying the original data
        categorical_cols = data.select_dtypes(include=['object']).columns
        label_encoders = {}
        for col in categorical_cols:
            label_encoders[col] = LabelEncoder()
            data[col] = label_encoders[col].fit_transform(data[col])

        # Prepare the independent and dependent variables
        X = data[[independent_variable]]
        y = data[target_variable]

        # Perform simple linear regression
        model = LinearRegression()
        model.fit(X, y)

        # Make predictions
        y_pred = model.predict(X)

        # Display regression coefficients and R-squared score
        intercept = model.intercept_
        coefficient = model.coef_[0]  # Extract the coefficient since there's only one independent variable
        r_squared = r2_score(y, y_pred)
        messagebox.showinfo("Linear Regression Results",
                            f"Intercept: {intercept}\nCoefficient: {coefficient}\nR-squared: {r_squared}")

        # Plot actual vs. predicted values
        plt.figure(figsize=(8, 6))
        plt.scatter(X, y, color='blue', label='Actual')
        plt.plot(X, y_pred, color='red', label='Predicted')
        plt.xlabel(independent_variable)
        plt.ylabel(target_variable)
        plt.title('Actual vs. Predicted Values (Linear Regression)')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Optionally, you can return the model if you want to use it for predictions later
        return model

    
    def apply_multiple_regression(self):
        # Check if data is available
        if self.current_data is None:
            messagebox.showerror("Error", "No data available for multiple regression.")
            return

        # Get the target variable from the user
        target_variable = simpledialog.askstring("Select Variable", "Enter name of the target variable:")
        if target_variable is None:
            messagebox.showerror("Error", "Please specify the target variable.")
            return

        # Check if the target variable exists in the DataFrame
        if target_variable not in self.current_data.columns:
            messagebox.showerror("Error", "Selected target variable not found in data.")
            return

        # Get the independent variables (all columns except the target variable)
        independent_variables = [col for col in self.current_data.columns if col != target_variable]

        # Convert categorical columns to numerical values
        data = self.current_data.copy()  # Create a copy to avoid modifying the original data
        categorical_cols = data.select_dtypes(include=['object']).columns
        label_encoders = {}
        for col in categorical_cols:
            label_encoders[col] = LabelEncoder()
            data[col] = label_encoders[col].fit_transform(data[col])

        # Prepare the independent and dependent variables
        X = data[independent_variables]
        y = data[target_variable]

        # Perform multiple linear regression
        model = LinearRegression()
        model.fit(X, y)

        # Make predictions
        y_pred = model.predict(X)

        # Display regression coefficients and R-squared score
        intercept = model.intercept_
        coefficients = model.coef_
        r_squared = r2_score(y, y_pred)
        messagebox.showinfo("Multiple Regression Results",
                            f"Intercept: {intercept}\nCoefficients: {coefficients}\nR-squared: {r_squared}")

        # Plot actual vs. predicted values
        plt.figure(figsize=(8, 6))
        plt.scatter(y, y_pred, color='blue', label='Actual vs. Predicted')
        plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2, label='Perfect Prediction')
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title('Actual vs. Predicted Values (Multiple Regression)')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Optionally, you can return the model if you want to use it for predictions later
        return model
    
    def apply_polynomial_regression(self, degree=2):
        # Check if data is available
        if self.current_data is None:
            messagebox.showerror("Error", "No data available for polynomial regression.")
            return

        # Get the target variable from the user
        target_variable = simpledialog.askstring("Select Variable", "Enter name of the target variable:")
        if target_variable is None:
            messagebox.showerror("Error", "Please specify the target variable.")
            return

        # Check if the target variable exists in the DataFrame
        if target_variable not in self.current_data.columns:
            messagebox.showerror("Error", "Selected target variable not found in data.")
            return

        # Get the independent variables (all columns except the target variable)
        independent_variables = [col for col in self.current_data.columns if col != target_variable]

        # Convert categorical columns to numerical values
        data = self.current_data.copy()  # Create a copy to avoid modifying the original data
        categorical_cols = data.select_dtypes(include=['object']).columns
        label_encoders = {}
        for col in categorical_cols:
            label_encoders[col] = LabelEncoder()
            data[col] = label_encoders[col].fit_transform(data[col])

        # Prepare the independent and dependent variables
        X = data[independent_variables]
        y = data[target_variable]

        # Perform polynomial regression
        model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
        model.fit(X, y)

        # Make predictions
        y_pred = model.predict(X)

        # Display R-squared score
        r_squared = r2_score(y, y_pred)
        messagebox.showinfo("Polynomial Regression Results", f"Degree: {degree}\nR-squared: {r_squared}")

        # Plot actual vs. predicted values
        plt.figure(figsize=(8, 6))
        plt.scatter(y, y_pred, color='blue', label='Actual vs. Predicted')
        plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2, label='Perfect Prediction')
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title('Actual vs. Predicted Values (Polynomial Regression)')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Optionally, you can return the model if you want to use it for predictions later
        return model


    def update_forecast_window(self, data):
        scaled_data = self.scale_data(data)
        self.data_forecast_window(scaled_data)


    def scale_data(self, data):
        """
        Scale the data using StandardScaler.

        Parameters:
        - data: DataFrame, the data to be scaled

        Returns:
        - scaled_data: DataFrame, the scaled data
        """
        # Convert categorical columns to numerical values
        data_copy = data.copy()  # Create a copy to avoid modifying the original data
        categorical_cols = data_copy.select_dtypes(include=['object']).columns
        label_encoders = {}
        for col in categorical_cols:
            label_encoders[col] = LabelEncoder()
            data_copy[col] = label_encoders[col].fit_transform(data_copy[col])

        # Scale the numerical columns
        numerical_cols = data_copy.select_dtypes(include=['float64', 'int64']).columns
        scaler = StandardScaler()
        data_copy[numerical_cols] = scaler.fit_transform(data_copy[numerical_cols])

        # Display the updated data in the Treeview widget
        self.display_in_treeview(data_copy)

        return data_copy


    def apply_decision_tree(self):
        # Check if data is available
        if self.current_data is None:
            messagebox.showerror("Error", "No data available for decision tree.")
            return

        # Get the target variable from the user
        target_variable = simpledialog.askstring("Select Variable", "Enter name of the target variable:")
        if target_variable is None:
            messagebox.showerror("Error", "Please specify the target variable.")
            return

        # Check if the target variable exists in the DataFrame
        if target_variable not in self.current_data.columns:
            messagebox.showerror("Error", "Selected target variable not found in data.")
            return

        # Convert categorical columns to numerical values
        data = self.current_data.copy()  # Create a copy to avoid modifying the original data
        categorical_cols = data.select_dtypes(include=['object']).columns
        label_encoders = {}
        for col in categorical_cols:
            label_encoders[col] = LabelEncoder()
            data[col] = label_encoders[col].fit_transform(data[col])

        # Prepare the independent and dependent variables
        X = data.drop(columns=[target_variable])
        y = data[target_variable]

        # Perform Decision Tree regression
        model = DecisionTreeRegressor()
        model.fit(X, y)

        # Make predictions
        y_pred = model.predict(X)

        # Display R-squared score
        r_squared = r2_score(y, y_pred)
        messagebox.showinfo("Decision Tree Regression Results", f"R-squared: {r_squared}")

        # Plot Decision Tree
        plt.figure(figsize=(12, 8), dpi=130)
        plot_tree(model, filled=True, feature_names=X.columns)
        plt.title("Decision Tree Plot")
        plt.show()
    
        
    def open_file(self, file_type):
        if file_type != "MySQL Server":
            file_extension = file_type.lower()
            file_path = filedialog.askopenfilename(title=f"Select {file_type} File", filetypes=[(f"{file_type} files", f"*.{file_extension}")])
            if file_path:
                print(f"Opening {file_type} file: {file_path}")
                try:
                    self.display_data(file_path, file_type)
                except Exception as e:
                    messagebox.showerror("Error", f"Error reading {file_type} file: {e}")
        else:
            try:
                self.mysql_connection_dialog()
            except:
                messagebox.showerror("Error", "Error connecting to MySQL Server.")
    
    def mysql_connection_dialog(self):
        # Dialog for MySQL connection details
        host = simpledialog.askstring("MySQL Connection", "Enter Host:")
        user = simpledialog.askstring("MySQL Connection", "Enter User:")
        password = simpledialog.askstring("MySQL Connection", "Enter Password:", show="*")
        database = simpledialog.askstring("MySQL Connection", "Enter Database:")

        if host and user and password and database:
            # Attempt to establish a MySQL connection
            try:
                self.mysql_conn = pymysql.connect(host=host, user=user, password=password, database=database)
                self.select_mysql_table()
            except pymysql.MySQLError as e:
                messagebox.showerror("MySQL Connection Error", f"Error connecting to MySQL Server: {e}")
        else:
            messagebox.showwarning("MySQL Connection", "Connection details are incomplete.")

    def select_mysql_table(self):
        cursor = self.mysql_conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = [table[0] for table in cursor.fetchall()]
        
        # Ask user to select a table
        table = simpledialog.askstring("Select Table", f"Enter table name from list: {', '.join(tables)}")
        if table in tables:
            # Fetching the data from the selected table
            query = f"SELECT * FROM {table}"
            cursor.execute(query)
            data = cursor.fetchall()
            
            # Fetching column names
            columns = [desc[0] for desc in cursor.description]
            
            # Converting the data into a Pandas DataFrame
            df = pd.DataFrame(data, columns=columns)
            
            # Displaying the data using the existing display_in_treeview method
            self.display_in_treeview(df)
        else:
            messagebox.showerror("Table Selection", "Invalid table name or table does not exist.")


    def display_data(self, file_path, file_type):
        if file_type.lower() == 'csv':
            self.current_data = pd.read_csv(file_path)
        elif file_type.lower() == 'text':
            with open(file_path, 'r') as file:
                text_data = file.read()
            self.current_data = pd.DataFrame({"Text Data": [text_data]})
        elif file_type.lower() == 'excel':
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active
            data = []
            for row in sheet.iter_rows(min_row=1, values_only=True):
                data.append(row)
            workbook.close()
            self.current_data = pd.DataFrame(data, columns=sheet[1])
        elif file_type.lower() == 'word':
            document = Document(file_path)
            text_data = ""
            for paragraph in document.paragraphs:
                text_data += paragraph.text + "\n"
            self.current_data = pd.DataFrame({"Text Data": [text_data]})

        self.display_in_treeview(self.current_data)

        # Update file_path attribute
        self.file_path = file_path


    def display_in_treeview(self, df):
            # Clear existing data
            for item in self.treeview.get_children():
                self.treeview.delete(item)

            # Update treeview columns
            columns = ['Row No.'] + list(df.columns)
            self.treeview["columns"] = columns

            # Configure column headings and widths
            for col in columns:
                self.treeview.heading(col, text=col, anchor=tk.CENTER)
                self.treeview.column(col, minwidth=150, anchor=tk.CENTER)

            # Insert data rows
            for index, row in df.iterrows():
                values = [index + 1] + list(row)
                self.treeview.insert("", index, values=values)

            # Add a frame to contain rows and columns labels
            if self.status_frame is not None:
                self.status_frame.pack_forget()  # Remove the status frame from view

            # Create and pack the status frame
            self.status_frame = tk.Frame(bg="white")
            self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)

            # Add labels for total number of rows and columns
            rows_label = tk.Label(self.status_frame, text="Rows: {}".format(df.shape[0]), font=("Arial", 10), bg="white", fg="#273746")
            rows_label.pack(side=tk.LEFT, padx=10)

            columns_label = tk.Label(self.status_frame, text="Columns: {}".format(df.shape[1]), font=("Arial", 10), bg="white", fg="#273746")
            columns_label.pack(side=tk.LEFT, padx=10)



if __name__ == "__main__":
    app = EmployeeManagementSystem()
    app.root.mainloop()