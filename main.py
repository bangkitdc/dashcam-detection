import tkinter as tk
from tkinter import ttk
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Dashcam Detection")
        self.geometry(f"{720}x{480}")
        self.resizable(False, False)

        self.grid_columnconfigure(2, weight=1)

        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=0, column=0, pady=20, padx=20, sticky="nsew", columnspan=2)

        self.label = customtkinter.CTkLabel(
            self.frame, text="Dashcam Detection", fg_color="transparent", font=("Arial", 16))
        self.label.grid(row=0, column=0, pady=20, columnspan=2)
        
        # label
        self.label1 = customtkinter.CTkLabel(self.frame, text="Insert Your Data Here", fg_color="transparent", font=("Arial", 14))
        self.label1.grid(row=1, column=0, padx=20, sticky="w")
        
        # create label and button
        self.btn_file = customtkinter.CTkButton(self.frame, text="Choose File", command=self.button_event, width=120)
        self.btn_file.grid(row=2, column=0, padx=(20, 0), pady=(10, 20), sticky="w")
        
        self.label2 = customtkinter.CTkLabel(self.frame, text="", fg_color="#0E4C78", width=120, corner_radius=5)
        self.label2.grid(row=2, column=1, padx=0, pady=(10, 20), sticky="w")
        
        # label
        self.label1 = customtkinter.CTkLabel(self.frame, text="Insert Your Video Here", fg_color="transparent", font=("Arial", 14))
        self.label1.grid(row=3, column=0, padx=20, sticky="w")
        
        # create label and button
        self.btn_file = customtkinter.CTkButton(self.frame, text="Choose File", command=self.button_event, width=120)
        self.btn_file.grid(row=4, column=0, padx=(20, 0), pady=(10, 20), sticky="w")
        
        self.label2 = customtkinter.CTkLabel(self.frame, text="", fg_color="#0E4C78", width=120, corner_radius=5)
        self.label2.grid(row=4, column=1, padx=0, pady=(10, 20), sticky="w")
        
        # create label and entry
        self.label3 = customtkinter.CTkLabel(self.frame, text="Threshold Distance :", fg_color="transparent")
        self.label3.grid(row=5, column=0, padx=(20, 0), pady=10, sticky="w")
        
        self.entry1 = customtkinter.CTkEntry(self.frame, placeholder_text="Enter here...", width=120)
        self.entry1.grid(row=5, column=1, padx=(0, 20), pady=10, sticky="w")
                
        # create label and entry
        self.label4 = customtkinter.CTkLabel(self.frame, text="Threshold Speed :", fg_color="transparent")
        self.label4.grid(row=6, column=0, padx=(20, 0), pady=10, sticky="w")
        
        self.entry2 = customtkinter.CTkEntry(self.frame, placeholder_text="Enter here...", width=120)
        self.entry2.grid(row=6, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # button
        self.btn_submit = customtkinter.CTkButton(self.frame, text="Submit", command=self.button_event, width=120)
        self.btn_submit.grid(row=7, column=0, padx=20, pady=20, columnspan=2)
    
        self.frame2 = customtkinter.CTkFrame(self)
        self.frame2.grid(row=0, column=2, pady=20, padx=20, sticky="nsew", columnspan=2)
        
        # Configure row and column weights
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.rowconfigure(0, weight=1)
        
        # Create a Treeview widget
        tree = ttk.Treeview(self.frame2)

        # Define columns
        tree["columns"] = ("1", "2", "3", "4")

        # Defining heading
        tree['show'] = 'headings'

        # width of columns and alignment 
        tree.column("1", width = 40, anchor ='c')
        tree.column("2", width = 160, anchor ='c')
        tree.column("3", width = 75, anchor ='c')
        tree.column("4", width = 160, anchor ='c')
        
        # Headings  
        # respective columns
        tree.heading("1", text ="No")
        tree.heading("2", text ="Timestamp")
        tree.heading("3", text ="Speed")
        tree.heading("4", text ="Category")
        
        # Insert sample data
        tree.insert("", "end", values=(1, "06.00 | 28 May 2023", 60, "Normal"))
        tree.insert("", "end", values=(2, "07.00 | 28 May 2023", 90, "Near Crash"))
        tree.insert("", "end", values=(3, "16.00 | 28 May 2023", 80, "Crash"))

        # Place the Treeview widget
        tree.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")
            
    def button_event(self):
        print("button pressed")

if __name__ == "__main__":
    app = App()
    app.mainloop()
