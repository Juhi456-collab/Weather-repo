import requests
from fpdf import FPDF
from datetime import datetime
import os

# === CONFIGURATION ===
API_KEY = "355c9aa7ac81dc75659d81095d3f1c07"
CITY = "Mumbai"
REPORT_FOLDER = "reports"

# === FETCH WEATHER DATA ===
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return {"error": data.get("message", "Error fetching data")}
    
    return {
        "City": city,
        "Temperature (°C)": data["main"]["temp"],
        "Humidity (%)": data["main"]["humidity"],
        "Weather": data["weather"][0]["description"].capitalize(),
        "Wind Speed (m/s)": data["wind"]["speed"],
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# === GENERATE PDF REPORT ===
def generate_pdf(data):
    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, txt="Automated Weather Report", ln=True, align="C")
    pdf.ln(10)

    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    filename = f"{REPORT_FOLDER}/weather_report_{data['City']}_{datetime.now().date()}.pdf"
    pdf.output(filename)
    return filename

# === MAIN FUNCTION ===
def main():
    weather_data = get_weather(CITY)
    if "error" in weather_data:
        print(f"Failed to fetch weather: {weather_data['error']}")
    else:
        pdf_file = generate_pdf(weather_data)
        print(f"Report generated: {pdf_file}")

if __name__ == "__main__":
    main()
    
