import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests
import csv


def get_table(url, file_name):
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
    response = requests.get(url, headers=headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = []
    table_elements = soup.find_all('table')
    
    for table_element in table_elements:
        table = []
        rows = table_element.find_all('tr')
        
        for row in rows:
            cells = row.find_all(['th', 'td'])
            row_data = [cell.get_text(strip=True) for cell in cells]
            table.append(row_data)
        
        tables.append(table)
    
    with open(file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for table in tables:
            csv_writer.writerows(table)

class TableExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Table Extractor")

        self.url_label = ttk.Label(root, text="Enter URL:")
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.insert(0, "https://example.com")  # Default URL

        self.file_label = ttk.Label(root, text="File Name:")
        self.file_entry = ttk.Entry(root, width=40)
        self.file_button = ttk.Button(root, text="Save to CSV", command=self.save_to_csv)

        # Grid layout
        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E)
        self.file_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.file_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W + tk.E)
        self.file_button.grid(row=2, column=0, columnspan=3, pady=10)

    def save_to_csv(self):
        url = self.url_entry.get()
        file_name = self.file_entry.get()

        if not url or not file_name:
            messagebox.showwarning("Error", "Please enter a valid URL and file name.")
            return

        try:
            get_table(url, file_name)
            messagebox.showinfo("Success", "Tables extracted and saved to CSV successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TableExtractorApp(root)
    root.geometry("400x200")
    root['background']='#856ff8'
    root.mainloop()
