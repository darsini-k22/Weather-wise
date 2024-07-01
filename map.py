import tkinter as tk
from tkintermapview import TkinterMapView
from helper import place_window
from weather import weather_page
import requests
from helper import close_page,label_font,set_icon

def api_response(root,coords):
    apikey='73555b92bfc93f94f21042d9b7a10285'
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={coords[0]}&lon={coords[1]}&appid={apikey}"
    response = requests.get(url)
    if response.status_code!=200:
        raise Exception("Error while getting coordinated")
    else:
        data=response.json()
        print(data)
        root.withdraw()
        weather_page(root,data)
    return data

def del_marker():
    if len(marks)>1:
        marks[0].delete()
        marks.remove(marks[0])
marks=[]
def map_window(root):
    root.withdraw()
    page=tk.Toplevel()
    set_icon(page)

    del_marker()
    page.title("Weather Wise: Map View")
    place_window(page)
    
    back_button = tk.Button(page, text="🔙", command=lambda: close_page(page, root),font=label_font())
    back_button.pack(side="top", anchor="nw")
    back_button.lift()

    map_widget = TkinterMapView(page, width=1000, height=700, corner_radius=0)
    map_widget.pack(fill="both", expand=True)
        
    def add_marker_event(coords):
        x,y=format(float(coords[0]),'.6f'),format(float(coords[1]),'.6f')
        print("Add marker:", x,y)
        marker=map_widget.set_marker(coords[0], coords[1], text='('+str(x)+','+str(y)+')')
        marks.append(marker)
        del_marker()
        print(len(marks))
        api_response(page,coords)
        
    map_widget.add_left_click_map_command(add_marker_event) 
    page.mainloop()
