from geopy.geocoders import Nominatim
import folium
from selenium import webdriver
from PIL import Image
import os
import time
import tkinter as tk
from tkinter import messagebox

# Function to find the location coordinates and display the map as an image
def find_location_as_image(place):
    # Use Nominatim to get the location coordinates with a unique user_agent
    geolocator = Nominatim(user_agent="my_unique_app_123")
    location = geolocator.geocode(place)
    
    if location:
        print(f'Coordinates for {place} are: ({location.latitude}, {location.longitude})')
        
        # Create a map using the coordinates
        map_ = folium.Map(location=[location.latitude, location.longitude], zoom_start=12)
        
        # Add a marker on the map at the coordinates
        folium.Marker([location.latitude, location.longitude], popup=place).add_to(map_)
        
        # Save the map as a temporary HTML file
        map_.save('map_temp.html')
        
        # Use Selenium to open the HTML file and capture a screenshot
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode (no browser window)
        driver = webdriver.Chrome(options=options)  # Ensure chromedriver is correctly installed
        
        # Set the window size for the screenshot
        driver.set_window_size(800, 600)
        
        # Open the HTML file with the absolute path
        html_file_path = os.path.abspath('map_temp.html')
        driver.get('file://' + html_file_path)
        
        # Wait a bit to make sure the map is fully loaded
        time.sleep(5)
        
        # Take a screenshot and save it as an image
        driver.save_screenshot('map.png')
        driver.quit()
        
        # Open and display the image using PIL
        image = Image.open('map.png')
        image.show()

    else:
        # Show an error if the location is not found
        messagebox.showerror("Error", f'Place "{place}" not found.')

# Function to get input from the user through tkinter
def get_input():
    place = place_entry.get()
    if place:
        find_location_as_image(place)
    else:
        messagebox.showwarning("Warning", "Please enter a place name.")

# Function to refresh the input field (clear current input)
def refresh_input():
    place_entry.delete(0, tk.END)

# Creating the main tkinter window
root = tk.Tk()
root.title("Find Location and Show Map")
root.geometry("400x250")

# Label and entry field for the place name
place_label = tk.Label(root, text="Enter the place name:")
place_label.pack(pady=10)

place_entry = tk.Entry(root, width=40)
place_entry.pack(pady=5)

# Button to fetch the location and display the map
find_button = tk.Button(root, text="Find Place and Show Map", command=get_input)
find_button.pack(pady=10)

# Button to refresh (clear) the input field
refresh_button = tk.Button(root, text="Refresh", command=refresh_input)
refresh_button.pack(pady=10)

# Start the graphical user interface
root.mainloop()
