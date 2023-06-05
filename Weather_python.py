import tkinter as tk
import requests
import json
from tkinter import ttk
import textwrap

API_KEY = "e268cc7f0959400a0b58ccbb91f403b2"  # Reemplaza esto con tu clave de API

LANGUAGES = {
    "en": {
        "title": "Weather App",
        "enter_city": "Enter a city:",
        "get_weather": "Get Weather",
        "unable": "Unable to get weather data.",
        "notfound": "City not found.",
        "weather": "Weather in {city}: {weather}, {temp}°C",
    },
    "es": {
        "title": "Aplicación del Clima",
        "enter_city": "Introduce una ciudad:",
        "get_weather": "Ver Clima",
        "unable": "No se puede obtener los datos del clima.",
        "notfound": "Ciudad no encontrada.",
        "weather": "Clima en {city}: {weather}, {temp}°C",
    },
}

class WeatherApp:
    def __init__(self, master):
        self.master = master
        self.language = tk.StringVar(value="en")
        self.master.title(LANGUAGES[self.language.get()]["title"])
        self.master.configure(bg='lightblue')

        self.frame = tk.Frame(master, bg='white', bd=5)
        self.frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

        self.entry = tk.Entry(self.frame, font=('Courier',18))
        self.entry.place(relwidth=0.65, relheight=1)

        self.button = tk.Button(self.frame, text=LANGUAGES[self.language.get()]["get_weather"], font=('Courier',14), command=self.get_weather, wraplength=200)
        self.button.place(relx=0.7, relheight=1)

        self.lower_frame = tk.Frame(self.master, bg='white', bd=5)
        self.lower_frame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.6, anchor='n')

        self.result_label = tk.Label(self.lower_frame, font=('Courier',18), wraplength=400)
        self.result_label.place(relwidth=1, relheight=1)

        self.language_menu = ttk.Combobox(master, textvariable=self.language, values=("en", "es"), state="readonly")
        self.language_menu.place(relx=0.85, rely=0.05, relwidth=0.1)
        self.language.trace("w", self.update_ui)

    def get_weather(self):
        city = self.entry.get()
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")
        data = response.json()

        unable_text = LANGUAGES[self.language.get()]["unable"]
        notfound_text = LANGUAGES[self.language.get()]["notfound"]
        weather_text = LANGUAGES[self.language.get()]["weather"]

        if "weather" not in data:
            self.result_label["text"] = unable_text
        elif data["cod"] == "404":
            self.result_label["text"] = notfound_text
        else:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            self.result_label["text"] = weather_text.format(city=city, weather=weather, temp=temp)

    def update_ui(self, *args):
        self.master.title(LANGUAGES[self.language.get()]["title"])
        self.button.configure(text=LANGUAGES[self.language.get()]["get_weather"])
        self.button.configure(wraplength=200)  # Restaurar el ancho de ajuste de línea

        # Ajustar el tamaño del botón dinámicamente
        button_text = LANGUAGES[self.language.get()]["get_weather"]
        wrapped_text = textwrap.fill(button_text, 20)  # Envolver el texto en 20 caracteres por línea
        self.button.configure(text=wrapped_text)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    app = WeatherApp(root)
    root.mainloop()
