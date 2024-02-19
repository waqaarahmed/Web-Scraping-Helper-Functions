#To Download pdf file in selenium
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
"download.default_directory": "C:/Users/XXXX/Desktop", #Change default directory for downloads
"download.prompt_for_download": False, #To auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
})
self.driver = webdriver.Chrome(options=options)