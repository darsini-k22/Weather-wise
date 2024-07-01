import tkinter as tk
from PIL import Image,ImageTk
from helper import place_window,label_font,icon_map,close_page,set_icon
from datetime import datetime, timedelta


def convert_timezone(dtIn, timezoneIn):
    dateTime = datetime.utcfromtimestamp(dtIn)
    dateTime += timedelta(seconds=timezoneIn)
    ampm = 'PM' if dateTime.hour >= 12 else 'AM'
    hour_12 = dateTime.hour % 12
    hour_12 = 12 if hour_12 == 0 else hour_12
    return dateTime, hour_12, ampm

def simple_icon_selector(icon):
    return icon_map[icon]

def icon_selector(data):
    data_icon=data['weather'][0]['icon']
    time=data['timezone']
    dtIn=data['dt']
    dt_time,time_hr,ampm=convert_timezone(dtIn=dtIn,timezoneIn=time)
    if data_icon in icon_map.keys():
        icon=icon_map[data_icon]
    elif ampm=="AM":
        icon=icon_map['day']
    elif ampm=="PM":
        icon=icon_map['night']
    else:
        icon=icon_map['default']
    return icon

def resize_img(image_path, w, h):
    img = Image.open(image_path)
    resized_image = img.resize((w, h))
    return ImageTk.PhotoImage(resized_image)

    
def convert_to_localtime(timestamp, timezone_offset):
    utc_time = datetime.utcfromtimestamp(timestamp)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time

def update_time(data, time_label):
    local_time = convert_to_localtime(data['dt'], data['timezone'])
    current_utc_time = datetime.utcnow()
    elapsed_time = current_utc_time - datetime.utcfromtimestamp(data['dt'])
    current_local_time = local_time + elapsed_time
    time_label.config(text=current_local_time.strftime('%H:%M:%S'))
    time_label.after(1000, lambda: update_time(data, time_label))
    
def isDay(datetime):
    hour = datetime.hour
    if 6 <= hour < 18:
        return True
    else:
        return False
    
def weather_page(root,data):
    page=tk.Toplevel()
    set_icon(page)
    page.title("Weather Wise: Weather details 🌡")
    time=data['timezone']
    dtIn=data['dt']
    datetime,_,ampm=convert_timezone(dtIn=dtIn,timezoneIn=time)
    isday=isDay(datetime)
    day_or_night='🌔' if not isday else '☀'
    bgcolor="#3ABEF9" if isday else "#151515"
    fgcolor="white" if not isday else "black"
    page.configure(bg=bgcolor)
    place_window(page)
    #back button
    back_button=tk.Button(page,text="🔙",font=label_font(15),bg=bgcolor,fg=fgcolor,command=lambda:close_page(page,root))
    back_button.place(relx=0.1,rely=0.1,anchor=tk.CENTER)
    
    #City name 
    tk.Label(page,text=data['name'],font=label_font(15),bg=bgcolor,fg=fgcolor).place(relx=0.5,rely=0.05,anchor=tk.CENTER)
    long=str(data['coord']['lon']) if data else "-"
    lat=str(data['coord']['lat']) if data else "-"
    
    #Coordinates display
    coords_label=tk.Label(page,text="long: "+long+"  "+"lat: "+lat,font=label_font(12),bg=bgcolor,fg=fgcolor)
    coords_label.place(relx=0.5,rely=0.1,anchor=tk.CENTER)
    
    #Date display
    date_label = tk.Label(page, text=datetime.strftime("%d/%m/%Y"), font=label_font(14), bg=bgcolor, fg=fgcolor)
    date_label.place(relx=0.35, rely=0.15, anchor=tk.CENTER)
    #Time display
    time_label = tk.Label(page, font=label_font(14), bg=bgcolor, fg=fgcolor)
    time_label.place(relx=0.55, rely=0.15, anchor=tk.CENTER)
    update_time(data,time_label)
    #Day or night display
    date_time_label = tk.Label(page, text=day_or_night, font=label_font(14), bg=bgcolor, fg="yellow")
    date_time_label.place(relx=0.7, rely=0.15, anchor=tk.CENTER)
    
    icon_data=icon_selector(data)
    icon=resize_img(icon_data,w=200,h=200)
    icon_image=tk.Label(page,image=icon,bg=bgcolor,fg=fgcolor)
    icon_image.image = icon
    icon_image.place(relx=0.5, rely=0.38, anchor=tk.CENTER)
    
    weather_name_label=tk.Label(page,text=data['weather'][0]['main'],font=label_font(13),bg=bgcolor,fg=fgcolor)
    weather_name_label.place(relx=0.5, rely=0.56, anchor=tk.CENTER)
    
    weather_desc_label=tk.Label(page,text=data['weather'][0]['description'],font=label_font(9),bg=bgcolor,fg=fgcolor)
    weather_desc_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    
    temp_max=format(float(data['main']['temp_max'])-273.15,'.2f')
    temp_min=format(float(data['main']['temp_min'])-273.15,'.2f')
    temp_max_icon=simple_icon_selector("max temp")
    temp_max_icon=resize_img(temp_max_icon,w=50,h=50)
    temp_min_icon=simple_icon_selector("min temp")
    temp_min_icon=resize_img(temp_min_icon,w=50,h=50)
    
    timezone_offset=data['timezone']
    sunset_icon=simple_icon_selector("sunset")
    sunset_icon=resize_img(sunset_icon,w=50,h=50)
    sunrise_icon=simple_icon_selector("sunrise")
    sunrise_icon=resize_img(sunrise_icon,w=50,h=50)
    sunset,sunset_hour,sunset_ampm=convert_timezone(data['sys']['sunset'],timezone_offset)
    sunrise,sunrise_hour,sunrise_ampm=convert_timezone(data['sys']['sunrise'],timezone_offset)
    
    wind=data['wind']['speed']
    wind_icon=simple_icon_selector("wind")
    wind_icon=resize_img(wind_icon,w=50,h=50)
    
    feels_like=format(float(data['main']['feels_like'])-273.15,'.2f')
    feels_like_icon=simple_icon_selector("feels")
    feels_like_icon=resize_img(feels_like_icon,w=50,h=50)
    
    sunset_time = f"{sunset_hour}:{sunset.minute:02d} {sunset_ampm}"
    sunrise_time = f"{sunrise_hour}:{sunrise.minute:02d} {sunrise_ampm}"
    
    humidity=data['main']['humidity']
    humidity_icon=simple_icon_selector("humidity")
    humidity_icon=resize_img(humidity_icon,w=50,h=50)
    
    sea_level=data['main']['sea_level']
    sea_level_icon=simple_icon_selector("sea-level")
    sea_level_icon=resize_img(sea_level_icon,w=50,h=50)

    temp_max_icon_label=tk.Label(page,image=temp_max_icon,font=label_font(9),bg=bgcolor,fg=fgcolor)
    temp_max_icon_label.image = temp_max_icon
    temp_max_icon_label.place(relx=0.2, rely=0.7, anchor=tk.CENTER)
    
    temp_max_label=tk.Label(page,text=temp_max+" °C",font=label_font(9),bg=bgcolor,fg=fgcolor)
    temp_max_label.place(relx=0.2, rely=0.76, anchor=tk.CENTER)
    
    temp_min_icon_label=tk.Label(page,image=temp_min_icon,font=label_font(9),bg=bgcolor,fg=fgcolor)
    temp_min_icon_label.image = temp_min_icon
    temp_min_icon_label.place(relx=0.4, rely=0.7, anchor=tk.CENTER)
    
    temp_min_label=tk.Label(page,text=temp_min+" °C",font=label_font(9),bg=bgcolor,fg=fgcolor)
    temp_min_label.place(relx=0.4, rely=0.76, anchor=tk.CENTER)
    
    feels_like_icon_label=tk.Label(page,image=feels_like_icon,font=label_font(9),bg=bgcolor,fg=fgcolor)
    feels_like_icon_label.image = feels_like_icon
    feels_like_icon_label.place(relx=0.6, rely=0.7, anchor=tk.CENTER)
    
    feels_like_label=tk.Label(page,text=feels_like+" °C",font=label_font(9),bg=bgcolor,fg=fgcolor)
    feels_like_label.place(relx=0.6, rely=0.76, anchor=tk.CENTER)
    
    humidity_icon_label=tk.Label(page,image=humidity_icon,font=label_font(9),bg=bgcolor,fg=fgcolor)
    humidity_icon_label.image = humidity_icon
    humidity_icon_label.place(relx=0.8, rely=0.7, anchor=tk.CENTER)
    
    humidity_label=tk.Label(page,text=str(humidity)+" %",font=label_font(9),bg=bgcolor,fg=fgcolor)
    humidity_label.place(relx=0.8, rely=0.76, anchor=tk.CENTER)
    
    #row2=========================================
    
    wind_icon_label=tk.Label(page,image=wind_icon,font=label_font(9),bg=bgcolor,fg=fgcolor)
    wind_icon_label.image = wind_icon
    wind_icon_label.place(relx=0.2, rely=0.85, anchor=tk.CENTER)
    
    wind_label=tk.Label(page,text=str(wind)+" meter/sec",font=label_font(9),bg=bgcolor,fg=fgcolor)
    wind_label.place(relx=0.2, rely=0.92, anchor=tk.CENTER)
    
    sunset_icon_label=tk.Label(page,image=sunset_icon,font=label_font(9),bg=bgcolor,fg=fgcolor)
    sunset_icon_label.image = sunset_icon
    sunset_icon_label.place(relx=0.4, rely=0.85, anchor=tk.CENTER)
    
    sunset_label=tk.Label(page,text=sunset_time,font=label_font(9),bg=bgcolor,fg=fgcolor)
    sunset_label.place(relx=0.4, rely=0.92, anchor=tk.CENTER)
    
    sunrise_icon_label=tk.Label(page,image=sunrise_icon,font=label_font(9),bg=bgcolor,fg=fgcolor)
    sunrise_icon_label.image = sunrise_icon
    sunrise_icon_label.place(relx=0.6, rely=0.85, anchor=tk.CENTER)
    
    sunrise_label=tk.Label(page,text=sunrise_time,font=label_font(9),bg=bgcolor,fg=fgcolor)
    sunrise_label.place(relx=0.6, rely=0.92, anchor=tk.CENTER)
    
    sea_level_icon_label=tk.Label(page,image=sea_level_icon,font=label_font(9),bg=bgcolor,fg=fgcolor)
    sea_level_icon_label.image = sea_level_icon
    sea_level_icon_label.place(relx=0.8, rely=0.85, anchor=tk.CENTER)
    
    sea_level_label=tk.Label(page,text=str(sea_level)+" hPa",font=label_font(9),bg=bgcolor,fg=fgcolor)
    sea_level_label.place(relx=0.8, rely=0.92, anchor=tk.CENTER)
    
    update_time(data,time_label)

    page.mainloop()
