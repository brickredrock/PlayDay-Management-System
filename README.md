# PlayDay-Management-System
Open Source PlayDay Management System for tracking events like Cloverleaf Barrels, Straightaway Barrels, and Poles for anyone to use.

Built and tested with Python version 3.10.7.

Modules installed:
wxPython
pandas
PySerial

Installed via pip using:
pip install wxpython
pip install pandas
pip install pyserial

Tested conversions with auto-py-to-exe (https://pypi.org/project/auto-py-to-exe/) and pyinstaller (https://pypi.org/project/pyinstaller/).

AS OF NOW:
This program runs 4 events in a 3 series format (each series is one of the primary events.  Cloverleaf Barrels, StraightAway Barrels, and Poles with a single Jackpot winner per each age group.  Each age group is parsed out as 5-8, 9-12, 13-16, 17-30, and 31+.  Works with the Farmtek Timer by setting your serial port to COM3.  10 Points are given per series to the fastest time with each place getting 1 less point for each additional place.  After 10 participants each additional rider would receive 0 points.

Series riders are defined based on checkbox in the rider entry form.  Winners per event are calculated in addition to the total series to allow for individual ranking on each day.

(Some of the) PLANNED UPDATES:
Configuration view for setting items like serial port, event types, series definitions, and age groups (or alternate grouping)
Divisions for different events (long term change)
Generic event definitions, allowing for more dynamic Play Day setups
Posting standings/winners to social media (long term change)
