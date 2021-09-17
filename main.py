from tkinter import *
from tkinter.font import families
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import requests
from io import BytesIO

def get_url_img(url):
    global image
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        input_text()
    except:
        pass
    
def choose_image_func():
    global image
    image_dir = filedialog.askopenfilename(initialdir="/",
    title="Open File",
    filetypes=(("PNGs", "*.png"), ("GIFs", "*.gif"), ("JPGs", "*.jpg"), ("JPEGs", "*.jpeg"), ("All Files", "*.*")))

    image = Image.open(image_dir)
    input_text()
    
def choose_url():
    global main_frame
    main_frame.place_forget()

    main_frame = Frame(bg=background_color)
    main_frame.place(anchor="c", relx=.5, rely=.5)

    label = Label(main_frame, text="URL", font=current_font, bg=background_color, fg=foreground_color)
    label.pack()

    url_entry = Entry(main_frame, font=current_font, width=35)
    url_entry.pack()

    select_url = Button(main_frame, text="Choose URL", font=current_font, command=lambda: get_url_img(url_entry.get()))
    select_url.pack()


def link_or_url():
    global main_frame
    global image_button

    main_frame.place_forget()
    main_frame = Frame(bg=background_color)
    main_frame.place(anchor="c", relx=.5, rely=.5)

    label_frame = Frame(main_frame, bg=background_color)
    label_frame.pack()

    link_or_url_label = Label(label_frame, text="Online URL or Image File", bg=background_color, fg=foreground_color, font=current_font)
    link_or_url_label.pack()

    buttons_frame = Frame(main_frame, bg=background_color)
    buttons_frame.pack()

    link_button = Button(buttons_frame, text="URL", command=choose_url, font=current_font, width=5)
    link_button.grid()

    file_button = Button(buttons_frame, text="File", command=choose_image_func, font=current_font, width=5)
    file_button.grid(row=0, column=1)

def get_font(font_size):
    return ImageFont.truetype("Roboto-Black.ttf", font_size)

def input_text():
    def get_image():
        def max_font(text):
            if text == "": return

            font_size = 1
            while draw.textsize(text, get_font(font_size))[0] < new_image.width and draw.textsize(text, get_font(font_size))[1] < new_image.height / 2:
                font_size += 25

            while draw.textsize(text, get_font(font_size))[0] > new_image.width or draw.textsize(text, get_font(font_size))[1] > new_image.height / 2:
                font_size -= 5
            
            return get_font(font_size)

        if color_entry.get() == "":
            color = "black"
        else: color = color_entry.get()

        new_image = image.copy()
        draw = ImageDraw.Draw(new_image)

        top_fnt = max_font(top_entry.get())
        bottom_fnt = max_font(bottom_entry.get())

        topw, toph = draw.textsize(top_entry.get(), top_fnt)
        bottomw, bottomh = draw.textsize(bottom_entry.get(), bottom_fnt)

        try:
            draw.text((new_image.width / 2 - topw / 2, 10), top_entry.get(), color, top_fnt, anchor="lt")
            draw.text((new_image.width / 2 - bottomw / 2, new_image.height - bottomh - 10), bottom_entry.get(), color, bottom_fnt)
        except ValueError: 
            draw.text((new_image.width / 2 - topw / 2, 10), top_entry.get(), "black", top_fnt, anchor="lt")
            draw.text((new_image.width / 2 - bottomw / 2, new_image.height - bottomh - 10), bottom_entry.get(), "black", bottom_fnt)
        except Exception as e:
            print(e)

            
        return new_image

    def entry_input(_):
        new_image = get_image()
        new_image.thumbnail((300, 300))

        image_tk = ImageTk.PhotoImage(new_image)

        image_label.config(image=image_tk)
        image_label.image = image_tk

    global main_frame

    main_frame.place_forget()
    main_frame = Frame(bg=background_color)
    main_frame.place(anchor="c", relx=.5, rely=.5)

    entry_frame = Frame(main_frame, bg=background_color)
    entry_frame.pack()

    top_label = Label(entry_frame, text="Top Text: ", font=current_font, bg=background_color, fg=foreground_color)
    top_label.grid(row=0, column=0)

    top_entry = Entry(entry_frame, font=current_font)
    top_entry.grid(row=0, column=1)

    top_entry.bind("<KeyRelease>", entry_input)
    
    bottom_label = Label(entry_frame, text="Bottom Text: ", font=current_font, bg=background_color, fg=foreground_color)
    bottom_label.grid(row=1, column=0)
    
    bottom_entry = Entry(entry_frame, font=current_font)
    bottom_entry.grid(row=1, column=1)
    bottom_entry.bind("<KeyRelease>", entry_input)

    color_label = Label(entry_frame, text="Color: ", font=current_font, bg=background_color, fg=foreground_color)
    color_label.grid(row=2, column=0)
    
    color_entry = Entry(entry_frame, font=current_font)
    color_entry.grid(row=2, column=1)
    color_entry.bind("<KeyRelease>", entry_input)

    image_tk = image.copy()
    image_tk.thumbnail((300, 300))
    image_tk = ImageTk.PhotoImage(image_tk)
    image_label = Label(main_frame, bg=background_color, image=image_tk)
    image_label.image = image_tk
    image_label.pack()

    image_buttons = Frame(main_frame, bg=background_color)
    image_buttons.pack()

    save_image = Button(image_buttons, text="Save Image", font=current_font, command=lambda: get_image().save(filedialog.asksaveasfile(filetypes = image_files, defaultextension = image_files).name))
    save_image.grid()

    restart_button = Button(image_buttons, text="New Meme", font=current_font, command=start)
    restart_button.grid(row=0, column=1)

def start():
    global main_frame
    main_frame.place_forget()
    main_frame = Frame(bg=background_color)
    main_frame.place(anchor="c", relx=.5, rely=.5)

    choose_image = Button(main_frame, text="Choose Image", command=link_or_url, font=current_font)
    choose_image.grid(row=0, column=0)
       
background_color = "#0a56cf"
foreground_color = "white"
image_files = [('PNG', '*.png'),
              ('JPG', '*.jpg'),
              ('All Files', '*.*')]

root = Tk()
root.geometry("800x500")
root.config(bg=background_color)

current_font = ("Verdana", 15)

main_frame = Frame(bg=background_color)
main_frame.place(anchor="c", relx=.5, rely=.5)

start()

root.title("Meme Generator")
root.mainloop()