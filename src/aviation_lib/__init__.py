"""
AviationLib - Библиотека для работы с авиационными данными
"""

from .flight_calculator import FlightCalculator
from .weather_analyzer import WeatherAnalyzer
from .airport_manager import AirportManager
from .fuel_calculator import FuelCalculator

__version__ = "0.1.0"
__author__ = "Avalonxy"

__all__ = [
    "FlightCalculator",
    "WeatherAnalyzer", 
    "AirportManager",
    "FuelCalculator"
]
