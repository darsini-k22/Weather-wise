import tkinter as tk
from helper import place_window,label_font,close_page,set_icon
from bs4 import BeautifulSoup
import requests
from tkinter import font

def get_headlines(bs):
    headline = bs.find('h1', {'id': "maincontent"})
    return headline.get_text() if headline else ""

def get_paragraph(bs):
    para = bs.find('p', {'class': "paragraph inline-placeholder vossi-paragraph-primary-core-light"})
    return para.get_text() if para else ""

def get_news(bs, base_url, headers):
    links = bs.find_all('a', attrs={'class': "container__link container__link--type-article container_lead-plus-headlines-with-images__link"},limit=5)
    links.extend(bs.find_all('a', attrs={'class': "container__link container__link--type-article container_vertical-strip__link"},limit=5))
    link_set=set(links[:10])
    news = []
    for l in link_set:
        url = l.get('href')
        if url.startswith('/'): 
            url = base_url + url
        pbs = get_content(url, headers)
        headline = get_headlines(pbs)
        para = get_paragraph(pbs).strip('\n').strip(' ')
        news.append({'title': headline.strip("\n").strip(" "), 'link': url, 'paragraph': para})
    
    return news

def get_content(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    bs = BeautifulSoup(response.content, "html.parser")
    return bs

def main(base_url, path, headers):
    url = str(base_url) + str(path)
    bs = get_content(url, headers)
    news = get_news(bs, base_url, headers)
    return news

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Accept-Language': 'da, en-gb, en',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        }


def open_link(url):
    import webbrowser
    webbrowser.open(url)
    
def headline_labels(page, headlines,root):
    text_widget = tk.Text(page, wrap=tk.WORD)
    text_widget.pack(fill=tk.BOTH,expand=True)
    

    scroll_bar = tk.Scrollbar(text_widget)
    text_widget.config(yscrollcommand=scroll_bar.set)
    scroll_bar.config(command=text_widget.yview)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    
    headline_font=lambda size=15:font.Font(family='Times New Roman', size=size, weight="bold")
    
    # back_button = tk.Button(text_widget, text="🔙", font=label_font(15), command=lambda: close_page(page, root),cursor="hand2")
    # text_widget.window_create(tk.END, window=back_button)
    # text_widget.insert(tk.END, "\n\n")
    
    for head in headlines:
        text_widget.insert(tk.END, "\n\n"+head['title'] + "\n",'headline')
        text_widget.insert(tk.END, "\n" + head['paragraph'] + "\n", 'paragraph')
        label = tk.Label(text_widget, text="Read more", fg="blue", cursor="hand2", font=headline_font(8))
        label.bind("<Button-1>", lambda e, url=head['link']: open_link(url))
        text_widget.window_create(tk.END, window=label)

    text_widget.config(state=tk.DISABLED)
    text_widget.tag_configure('headline', font=headline_font(12))
    text_widget.tag_configure('paragraph', font=headline_font(10))


def news_window(root):
    root.withdraw()
    page=tk.Toplevel()
    set_icon(page)
    page.title("Weather Wise: 🌏 Climatic News")
    place_window(page)
    back_button = tk.Button(page, text="🔙", font=label_font(15), command=lambda: close_page(page, root),cursor="hand2")
    back_button.place(relx=0.02,rely=0.0)
    loading_label = tk.Label(page, text="Climate News", font=label_font(13))
    loading_label.pack(pady=20)
    
    url="https://edition.cnn.com"
    headlines = main(url,"/climate",headers)
    
    headline_labels(page,headlines,root)
    
    page.mainloop()

    