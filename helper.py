
from PIL import Image,ImageTk
from tkinter import font

def place_window(root,width=400,height=600):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    

#does not work
def set_bg(tk,image,root):
    img = Image.open(image)
    resized_image = img.resize((400, 600))
    resized_image.save(image)
    bg=tk.PhotoImage(file=image)

    label1 = tk.Label(root, image = bg) 
    label1.place(x = -2, y = -2) 

label_font = lambda size=15:font.Font(family='Times New Roman', size=size, weight='normal')
entry_font=lambda size=12:font.Font(family='Times New Roman', size=size, weight='normal')
button_font=lambda size:font.Font(family='Times New Roman', size=size, weight='normal')


icon_map={
    '01d':'images/sun.png',
    '02d':'images/few_clouds.png',
    '03d':"images/broken_clouds.png",
    '04d':'images/broken_clouds.png',
    '09d':'images/drizzle.png',
    '10d':'images/rain.png',
    '11d':'images/thunder_strong.png',
    '13d':'images/snow.png',
    '50d':'images/mist.png',
    '01n':'images/sun.png',
    '02n':'images/few_clouds.png',
    '03n':"images/broken_clouds.png",
    '04n':'images/broken_clouds.png',
    '09n':'images/drizzle.png',
    '10n':'images/rain.png',
    '11n':'images/thunder_strong.png',
    '13n':'images/snow.png',
    '50n':'images/mist.png',
    'max temp':'images/max_temp.png',
    'min temp':'images/min_temp.png',
    'feels':'images/feels_like.png',
    'wind':'images/wind.png',
    'night':'images/moon.png',
    'day':'images/sun.png',
    'sunset':'images/sunset.png',
    'sunrise':'images/sunrise.png',
    'humidity':'images/humidity.png',
    'sea-level':'images/sea-level.png',
    'default':'images/sun.png'
}

def close_page(page,root):
    page.withdraw()
    root.deiconify()
    
    
def set_icon(root):
    ico = Image.open('images/weather-news.png')
    photo = ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False, photo)
