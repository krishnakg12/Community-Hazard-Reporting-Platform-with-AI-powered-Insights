import requests

def get_traffic_score(api_key, center_lat, center_lng, delta=0.0025):
    """
    Fetches traffic data for a bounding box around the center coordinate
    and computes an overall traffic score from 0 to 100.
    
    The score is computed by weighting:
      - 70% from the jam factor (jamFactor * 10)
      - 30% from the relative speed reduction ((freeFlow - speed) / freeFlow * 100)
    Scores are weighted by each segment's length.
    
    Parameters:
      api_key (str): Your HERE API key.
      center_lat (float): Latitude of the center point.
      center_lng (float): Longitude of the center point.
      delta (float): Half of the span in degrees for the bounding box.
    
    Returns:
      float: Traffic score (0 to 100) or None if no data.
    """
    # Create bounding box around the center coordinate
    min_lon = center_lng - delta
    max_lon = center_lng + delta
    min_lat = center_lat - delta
    max_lat = center_lat + delta
    bbox = f"bbox:{min_lon},{min_lat},{max_lon},{max_lat}"
    
    # Construct the HERE Traffic API URL
    url = f"https://data.traffic.hereapi.com/v7/flow?locationReferencing=shape&in={bbox}&apiKey={api_key}"
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Traffic API request failed with status code: {response.status_code}")
        return None

    data = response.json()
    segments = data.get("results", [])
    if not segments:
        print("No traffic data found for the specified bounding box.")
        return None

    total_length = 0.0
    weighted_score_sum = 0.0

    for seg in segments:
        current_flow = seg.get("currentFlow", {})
        location = seg.get("location", {})
        jam = current_flow.get("jamFactor", 0)
        speed = current_flow.get("speed", 0)
        free_flow = current_flow.get("freeFlow", 0)
        length = location.get("length", 0)

        # Calculate relative speed reduction (0 if freeFlow is zero)
        if free_flow > 0:
            speed_reduction = (free_flow - speed) / free_flow  # 0 to 1
        else:
            speed_reduction = 0

        # Scale the jam factor (0-10) to 0-100
        jam_score = jam * 10
        # Scale speed reduction to 0-100
        speed_score = speed_reduction * 100

        # Compute the segment score with 70% weight on jam and 30% on speed reduction
        seg_score = 0.7 * jam_score + 0.3 * speed_score

        total_length += length
        weighted_score_sum += seg_score * length

    overall_traffic_score = weighted_score_sum / total_length if total_length > 0 else 0
    return overall_traffic_score

def get_openweather(api_key, lat, lon):
    """
    Fetches current weather data from OpenWeatherMap for the given latitude and longitude.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"  # Temperature in Celsius
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"OpenWeatherMap API request failed with status code: {response.status_code}")
        print("Response:", response.text)
        return None
    return response.json()

def compute_weather_score(weather_data):
    """
    Computes a refined weather score (0-100) for hazard evaluation.
    
    Base score is determined from the weather description:
      - "thunderstorm": 90
      - "heavy rain": 80
      - "rain": 70
      - "drizzle": 50
      - "snow": 80
      - "cloud": 40
      - "clear": 10
      - default: 30
    
    Adjustments:
      - If wind speed > 10 m/s, add 10.
      - If wind speed is between 5 and 10 m/s, add 5.
      - If temperature is below 0°C or above 35°C, add 10.
    
    The final score is clamped to 100.
    """
    description = weather_data.get("weather", [{}])[0].get("description", "").lower()
    wind_speed = weather_data.get("wind", {}).get("speed", 0)
    temperature = weather_data.get("main", {}).get("temp", 20)  # default 20°C if missing

    # Base score based on weather condition
    if "thunderstorm" in description:
        base_score = 90
    elif "heavy rain" in description:
        base_score = 80
    elif "rain" in description:
        base_score = 70
    elif "drizzle" in description:
        base_score = 50
    elif "snow" in description:
        base_score = 80
    elif "cloud" in description:
        base_score = 40
    elif "clear" in description:
        base_score = 10
    else:
        base_score = 30

    adjustment = 0
    # Adjust for wind speed
    if wind_speed > 10:
        adjustment += 10
    elif wind_speed > 5:
        adjustment += 5

    # Adjust for extreme temperatures
    if temperature < 0 or temperature > 35:
        adjustment += 10

    weather_score = base_score + adjustment
    return min(weather_score, 100)

if __name__ == "__main__":
    # Define coordinate for the hazard
    center_lat, center_lng = 12.863463, 77.531683

    # HERE Traffic API key
    here_api_key = "qbtEgtO91z_lAe2PwHBU-G_m8YX5h7M2GZVZLkq0NCY"
    # OpenWeatherMap API key
    owm_api_key = "581d40ca26ab7fa277b8f94947c97385"

    # Use a delta of 0.002 to focus on the hazard vicinity
    traffic_score = get_traffic_score(here_api_key, center_lat, center_lng, delta=0.002)
    if traffic_score is None:
        print("Failed to get traffic score.")
    else:
        print(f"Traffic Score: {traffic_score:.2f} / 100")

    weather_data = get_openweather(owm_api_key, center_lat, center_lng)
    if weather_data is None:
        print("Failed to get weather data.")
    else:
        weather_score = compute_weather_score(weather_data)
        print(f"Weather Score: {weather_score:.2f} / 100")

    # Combine scores into an overall hazard priority score.
    # Here we weight traffic at 60% and weather at 40%.
    if traffic_score is not None and weather_data is not None:
        overall_priority = 0.6 * traffic_score + 0.4 * weather_score
        print(f"Overall Hazard Priority Score: {overall_priority:.2f} / 100")
