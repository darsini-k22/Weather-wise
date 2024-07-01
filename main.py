import tkinter as tk
import requests 
from PIL import Image
from helper import place_window,label_font,button_font,entry_font,set_icon
from weather import weather_page
from news import news_window
from map import map_window

def api_response():
    city=city_var.get()
    apikey='73555b92bfc93f94f21042d9b7a10285'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}"
    response = requests.get(url)
    if response.status_code!=200:
        city_name_error.set("Invalid City Name")
        raise Exception("Invalid City name")
    else:
        city_name_error.set("")
        data=response.json()
        print(data)
        root.withdraw()
        weather_page(root,data)
    return data


#==============================interface ==================================
root=tk.Tk()
root.title('Weather Wise')
set_icon(root)
place_window(root)

img = Image.open("images/sky.png")
resized_image = img.resize((400, 600))
resized_image.save("images/sky.png")
bg=tk.PhotoImage(file="images/sky.png")

label1 = tk.Label(root, image = bg) 
label1.place(x = -2, y = -2)

w=tk.Label(root,text="Enter city name",font=label_font(15),fg="white",bg="gray")
w.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

city_var=tk.StringVar()
city_input_box=tk.Entry(root,font=entry_font(12),textvariable=city_var).place(relx=0.5, rely=0.4+0.05, anchor=tk.CENTER)
city_submit_button=tk.Button(root,text="Submit",font=button_font(10),bg="green",fg="white",command=api_response).place(relx=0.5, rely=0.4+0.1, anchor=tk.CENTER)

city_name_error = tk.StringVar()
error_label = tk.Label(root, textvariable=city_name_error, fg="red", bg="gray",font=button_font(10))
error_label.place(relx=0.5, rely=0.4 + 0.2, anchor=tk.CENTER) 

news_view_button=tk.Button(text="Weather News",bg="blue",fg="white",font=button_font(12),command=lambda: news_window(root)).place(relx=0.3, rely=0.8, anchor=tk.CENTER)
map_choose_button=tk.Button(text="Choose From Map",bg="blue",fg="white",font=button_font(12),command=lambda: map_window(root)).place(relx=0.7, rely=0.8, anchor=tk.CENTER)

root.mainloop()

