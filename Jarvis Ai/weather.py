import requests


def weather(city="Dharashiv"):
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        return response.text.strip()

    except requests.exceptions.RequestException:
        return "Sorry sir, weather service is currently unavailable."


# Test weather.py directly
if __name__ == "__main__":
    print(weather())