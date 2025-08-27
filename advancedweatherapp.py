import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime

# Your API key
API_KEY = "c83fdb035d514c2b90cd9802f494c5b2"

def get_weather():
    city = city_entry.get().strip()
    country = country_entry.get().strip()

    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name!")
        return

    query = f"{city},{country}" if country else city
    url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            condition = data['weather'][0]['description'].title()
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            icon_code = data['weather'][0]['icon']
            timestamp = data['dt']
            local_time = datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')

            # Set result text (with emoji, bold, white)
            result.set(
                f"🌡 Temp: {temp}°C\n"
                f"🤔 Feels Like: {feels_like}°C\n"
                f"🌥 Condition: {condition}\n"
                f"💧 Humidity: {humidity}%\n"
                f"💨 Wind: {wind} m/s\n"
                f"🕒 Time: {local_time}"
            )

            # Fetch and display weather icon
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_response = requests.get(icon_url)
            icon_image = Image.open(BytesIO(icon_response.content))
            icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo  # Keep a reference

        else:
            message = data.get("message", "Something went wrong!")
            messagebox.showerror("Error", message)
    except Exception as e:
        messagebox.showerror("Error", str(e))


def clear_all():
    city_entry.delete(0, tk.END)
    country_entry.delete(0, tk.END)
    result.set("")
    icon_label.config(image='')


# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("Weather App")
root.geometry("500x500")
root.configure(bg="blue")

# ---------- Frames for better layout ----------
input_frame = tk.Frame(root, bg="blue")  # Match background
input_frame.pack(pady=10)

output_frame = tk.Frame(root, bg="blue")  # Match background
output_frame.pack(pady=10)

# ---------- Input fields ----------
tk.Label(input_frame, text="City:", font=("Algerian", 12, "bold"), bg="blue", fg="white").grid(row=0, column=0, padx=5)
city_entry = tk.Entry(input_frame, font=("Algerian", 12), width=15)
city_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Country Code (optional):", font=("Algerian", 12, "bold"), bg="blue", fg="white").grid(row=0, column=2, padx=5)
country_entry = tk.Entry(input_frame, font=("Algerian", 12), width=5)
country_entry.grid(row=0, column=3)

# ---------- Buttons ----------
tk.Button(root, text="Get Weather", command=get_weather, font=("Georgia", 12, "bold")).pack(pady=5)
tk.Button(root, text="Clear", command=clear_all, font=("Georgia", 12, "bold")).pack()

# ---------- Output area ----------
result = tk.StringVar()
tk.Label(output_frame, textvariable=result, font=("Georgia", 14, "bold"), bg="blue", fg="white", justify="left").pack()

# ---------- Weather icon ----------
icon_label = tk.Label(root, bg="blue")
icon_label.pack(pady=10)

root.mainloop()
