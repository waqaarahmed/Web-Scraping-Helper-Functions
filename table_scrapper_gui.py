import customtkinter as ctk



ctk.set_appearance_mode("dark")        
 

# Supported themes: green, dark-blue, blue
ctk.set_default_color_theme("green")    
 
appWidth, appHeight = 600, 700

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        self.title("GUI Application")
        self.geometry(f"{appWidth}x{appHeight}")
 
        # URL Label
        self.urlLabel = ctk.CTkLabel(self,
                                      text="URL")
        self.urlLabel.grid(row=0, column=0,
                            padx=20, pady=20,
                            sticky="ew")
 
        # URL Entry Field
        self.urlEntry = ctk.CTkEntry(self,
                         placeholder_text="https://www.example.com/")
        self.urlEntry.grid(row=0, column=1,
                            columnspan=3, padx=20,
                            pady=20, sticky="ew")
 
        # File Label
        self.fileLabel = ctk.CTkLabel(self,
                                     text="File Name")
        self.fileLabel.grid(row=1, column=0,
                           padx=20, pady=20,
                           sticky="ew")
 
        # File Entry Field
        self.fileEntry = ctk.CTkEntry(self,
                            placeholder_text="abc.csv")
        self.fileEntry.grid(row=1, column=1,
                           columnspan=3, padx=20,
                           pady=20, sticky="ew")
 
        # Scrape Button
        self.scrapeButton = ctk.CTkButton(self,
                                         text="Scrape")
        self.scrapeButton.grid(row=5, column=1,
                                        columnspan=2,
                                        padx=20, pady=20,
                                        sticky="ew")
 
        # Text Box
        self.displayBox = ctk.CTkTextbox(self, width=200,
                                         height=100)
        self.displayBox.grid(row=6, column=0, columnspan=4,
                             padx=20, pady=20, sticky="nsew")
 
if __name__ == "__main__":
    app = App()
    app.mainloop()