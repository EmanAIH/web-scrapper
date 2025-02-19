# import
import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import messagebox


# creating the  scrape headline Function

def scrapeheadline(url, pages=5):
    headlines =[]

    for page_num in range(1, pages+1): # Loop through the pages
        page_url = f"{url}/page/{page_num}"
        response = requests.get(page_url)

        if response.status_code ==200:
            soup = BeautifulSoup(response.content, 'html.parser')
            page_headlines = soup.find_all("h3", class_="card-title")

            for headline in page_headlines:
                headline_text = headline.get_text(strip=True)
                if headline_text:
                    headlines.append(headline_text)
        
        else:
            print(f"Error fetching page {page_num}: {response.status_code}")
   
    return headlines

# creating the  write_to_csv Function

def write_to_csv(headlines):
    with open("headlines.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['headline']) # it will write the header

        for headline in headlines:
            writer.writerow([headline])
    messagebox.showinfo("Scraping Complete", f"Scraping complete! Found {len(headlines)} headlines.")

# creating the  start scraping function

def start_scraping():
    url = url_entry.get()

    try:
        pages = int(pages_entry.get())  # Get number of pages to scrape
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid page number")
        return
    
    headlines = scrapeheadline(url, pages)
    write_to_csv(headlines)


# Designing the GUI

root = tk.Tk()
root.title("Web scrapper for Headline")

# Adding a label and input field for url

url_label = tk.Label(root, text="Enter Website URL (e.g., https://website.cnn.com)")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Adding a label and input field for number of pages
pages_label = tk.Label(root, text= "number of pages to scrape is?")
pages_label.pack()
pages_entry = tk.Entry(root, width=50)
pages_entry.pack()

# Adding a button to start scraping
scrape_button = tk.Button(root, text="Start Scraping", command=start_scraping)
scrape_button.pack()

root.mainloop() # Start the GUI event loop
