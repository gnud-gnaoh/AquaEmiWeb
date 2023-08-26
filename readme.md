# AquaEmi

**AquaEmi** is a web IOT product aim to identify, control and evaluate environmental effects of water pollution.

The project uses [Flask](https://flask.palletsprojects.com/en/2.3.x/) for back-end, [MySQL](https://www.mysql.com/) for database.

[Leaflet](https://leafletjs.com/) and [Mapbox](https://www.mapbox.com/) API for interactive maps. 

The project also integrates [AI technology](https://github.com/AIMasterRace/Aquaemi-ARIMA) to predict water quality, [IOT](https://github.com/AIMasterRace/AquaEmi_IoT) to measure water data and [MQTT Paho](https://pypi.org/project/paho-mqtt/) to connect with the hardware.

Some more details and statistics about the [hardware and the forecasting](https://docs.google.com/document/d/1TaorF_7x6znF8inQv3C-6PSgdkxXTADECVwlWkkH1LI/edit#heading=h.mggxvvj6fy1c).
## Installation & usage

- (Optional) Create a virtual environment

Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```
    
Windows:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

If there is error with "Execution Policies", run:
```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```

- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install require packages.
```bash
pip install -r requirements.txt
```

- To run:
```bash
flask run 
```