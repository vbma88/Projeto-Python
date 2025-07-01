import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import io
import threading
import itertools
import os

API_KEY = '4ff2112d30faa9a24dbd006b44158745'

# Mapear categorias de clima para imagens locais
BACKGROUND_IMAGES = {
    'clear': 'backgrounds/clear.jpg',
    'clouds': 'backgrounds/clouds.jpg',
    'rain': 'backgrounds/rain.jpg',
    'snow': 'backgrounds/snow.jpg',
    'mist': 'backgrounds/mist.jpg',
    'thunderstorm': 'backgrounds/thunderstorm.jpg',
}

def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/forecast'
    params = {'q': city, 'appid': API_KEY, 'units': 'metric', 'lang': 'pt_br', 'cnt': 24}
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(e)
        return None

def load_local_image(filepath):
    try:
        image = Image.open(filepath)
        return ImageTk.PhotoImage(image.resize((420, 400)))
    except:
        return None

def set_background(weather_main):
    weather_main = weather_main.lower()
    if 'cloud' in weather_main:
        key = 'clouds'
    elif 'rain' in weather_main or 'drizzle' in weather_main:
        key = 'rain'
    elif 'snow' in weather_main:
        key = 'snow'
    elif 'mist' in weather_main or 'fog' in weather_main:
        key = 'mist'
    elif 'thunder' in weather_main:
        key = 'thunderstorm'
    elif 'clear' in weather_main:
        key = 'clear'
    else:
        key = 'clouds'

    filepath = BACKGROUND_IMAGES.get(key)
    bg_image = load_local_image(filepath)
    if bg_image:
        background_label.config(image=bg_image)
        background_label.image = bg_image

def show_weather():
    city = city_entry.get().strip()
    city_entry.delete(0, tk.END)
    if not city:
        messagebox.showwarning("Aviso", "Por favor, digite uma cidade")
        return

    data = get_weather(city)
    if data and 'list' in data:
        forecast = data['list'][:3]
        results = []
        icons = []

        weather_main = data['list'][0]['weather'][0]['main']
        set_background(weather_main)

        for entry in forecast:
            desc = entry['weather'][0]['description'].capitalize()
            temp = entry['main']['temp']
            humidity = entry['main']['humidity']
            wind = entry['wind']['speed']
            icon_code = entry['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_data = requests.get(icon_url).content
            image = Image.open(io.BytesIO(icon_data)).resize((50, 50))
            photo = ImageTk.PhotoImage(image)
            icons.append(photo)
            result = f"Clima: {desc}\nTemp: {temp:.1f} °C\nUmidade: {humidity}%\nVento: {wind} m/s"
            results.append(result)

        for widget in forecast_frame.winfo_children():
            widget.destroy()

        for i, text in enumerate(results):
            frame = ttk.Frame(forecast_frame)
            frame.pack(pady=5)
            icon_label = ttk.Label(frame, image=icons[i])
            icon_label.image = icons[i]
            icon_label.pack(side="left", padx=5)
            text_label = ttk.Label(frame, text=text, font=("Segoe UI", 10), justify="left")
            text_label.pack(side="left")
    else:
        messagebox.showerror("Erro", "Cidade não encontrada ou erro na API.")

# Interface principal
root = tk.Tk()
root.title("Previsão do Tempo")
root.geometry("420x400")
root.resizable(False, False)

background_label = tk.Label(root)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", background="#ffffff", font=("Segoe UI", 10))
style.configure("TFrame", background="#ffffff")

title_label = ttk.Label(root, text="App de Clima", font=("Segoe UI", 16, "bold"), background="#ffffff")
title_label.pack(pady=(20, 10))

entry_frame = ttk.Frame(root)
entry_frame.pack()

city_entry = ttk.Entry(entry_frame, width=30, font=("Segoe UI", 10))
city_entry.pack(side="left", padx=(0, 10))

search_button = ttk.Button(entry_frame, text="Buscar", command=show_weather)
search_button.pack(side="left")

forecast_frame = ttk.Frame(root)
forecast_frame.pack(pady=20)

root.mainloop()

