import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests
import csv


def get_links(url):
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
    response = requests.get(url, headers=headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    links = []
    link_elements = soup.find_all('a')
    for link_element in link_elements:
        links.append(link_element.get('href'))

    return links

class LinkExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Link Extractor")

        self.url_label = ttk.Label(root, text="Enter URL:")
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.insert(0, "https://example.com")  # Default URL

        self.file_label = ttk.Label(root, text="File Name:")
        self.file_entry = ttk.Entry(root, width=40)
        self.file_button = ttk.Button(root, text="Save to File", command=self.save_to_file)

        # Grid layout
        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E)
        self.file_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.file_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W + tk.E)
        self.file_button.grid(row=2, column=0, columnspan=3, pady=10)

    def save_to_file(self):
        url = self.url_entry.get()
        file_name = self.file_entry.get()
        file_format = self.file_format.get()

        if not url or not file_name:
            tk.messagebox.showwarning("Error", "Please enter a valid URL and file name.")
            return

        try:
            links = get_links(url)

            if file_format == "CSV":
                self.save_to_csv(file_name, links)
            elif file_format == "DOCX":
                self.save_to_docx(file_name, links)
            elif file_format == "XLSX":
                self.save_to_xlsx(file_name, links)
            elif file_format == "PDF":
                self.save_to_pdf(file_name, links)

            tk.messagebox.showinfo("Success", f"Links extracted and saved to {file_format} successfully.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def save_to_csv(self):
        url = self.url_entry.get()
        file_name = self.file_entry.get()

        if not url or not file_name:
            messagebox.showwarning("Error", "Please enter a valid URL and file name.")
            return

        try:
            get_table(url, file_name)
            messagebox.showinfo("Success", "Links extracted and saved to CSV successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")



if __name__ == "__main__":
    root = tk.Tk()
    app = LinkExtractorApp(root)
    root.geometry("400x200")
    root['background']='#856ff8'
    root.mainloop()
