### NOTE: The API key has expired so the software can no longer be run

# Team Coconuts

### Members

-   Vishal Aiely
-   Omar Trejo
-   Colby Smith
-   Logan Wrinkle
-   Selena Xue

# Weather App

## Technical Details

This project uses python version `3.10` (latest stable build).
Package versions will be mentioned in `requirements.txt`.

### Tech Stack

-   python (3.10)
-   PyQt6

## Resources
Icons used in widgets were obtained from Freepik: <div>Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>


### How to run

Install necessary packages

```bash
$ pip install -r requirements.txt
```

Run the `GUI` of our application using the following prompt (from root)

```bash
$ python main.py
```

### Directory Structure

```
├── README.md
├── main.py (Entry point)
├── 📁 backend
│   ├── location.py 
│   ├── secure_API_key.py
│   └── weather.py
│   # classes to help with app functionality
├── 📁 helpers
│   ├── temperature.py
│   └── 📁 notifications
│       └── rain.py 
│   # icons used in widgets
├── 📁 icons
│   # images used for background'
├── 📁 images
│   # All widgets utilized in application
├── 📁 widgets
│   ├── clouds.py
│   ├── currentTemp.py
│   ├── displaycity.py
│   ├── displayUserCoord.py
│   ├── highlow.py
│   ├── hourly_weather.py
│   ├── humidity.py
│   ├── locationbutton.py
│   ├── map.py
│   ├── notification.py
│   ├── searchbox.py
│   ├── sunriseSunset.py
│   ├── uvNotify.py
│   ├── uvRays.py
│   ├── weather_icons.py
│   ├── weatherDays.py
│   ├── weatherDes.py
│   ├── wind.py
│   ├── displayUserCoord.py
│   ├── map.py
│   ├── weatherDays.py
│   └── wind.py
├── .env (Ignored)
├── requirements.txt 
└── .gitignore
```
