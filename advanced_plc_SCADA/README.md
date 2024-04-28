# Advanced PLC SCADA Template Spring 2024 - Version 1.0
## General Description
This is the basic template for the University of Idaho Advanced PLC classes SCADA system for tying together all other portions of the class. These systems include but are not limited to:
  - The AutomationDirect BRX PLC Controlling the Fischertechnik Mini Fatcory 4.0
  - The KOYO Click PLC Controlling the Stepper Motor
  - The Schneider Electric (S.E) Modicon M172 PLC W/ Various Hardware and the S.E. Smart Thermostat
  - The Lenze C300 PLC Controlling the VFD W/ a 240VAC 3 Phase Motor Attached

## Built With
  - The Django Web Framework
    - [Documentation](https://www.djangoproject.com/)  
  - Boostrap 5
    - [Template](https://startbootstrap.com/template/sb-admin)
    - [Documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
  - Plotly JS
    - [Documentation](https://plotly.com/javascript/)
  - PyModbus
    - [Documentation](https://pymodbus.readthedocs.io/en/latest/)

## Install and Setup
- Clone repository
- Pip install -r requirements.txt
- Run py manage.py migrate

## Running The Code
- Run py manage.py runserver

## Authors
Hunter Hawkins - hawk5052@vandals.uidaho.edu

## License
This project is licensed under the [MIT License](LICENSE.md), which means it is free for anyone to use, modify, and distribute.
