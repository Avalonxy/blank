"""
Модуль для расчета параметров полета
"""

import math
from typing import Tuple, Dict, Optional


class FlightCalculator:
    """Калькулятор для расчета параметров полета"""
    
    def __init__(self):
        self.earth_radius = 6371  # Радиус Земли в км
        self.gravity = 9.81  # Ускорение свободного падения м/с²
    
    def calculate_flight_time(self, distance: float, speed: float, 
                            wind_factor: float = 1.0) -> float:
        """
        Расчет времени полета
        
        Args:
            distance: Расстояние в км
            speed: Скорость в км/ч
            wind_factor: Коэффициент влияния ветра (0.8-1.2)
            
        Returns:
            Время полета в часах
        """
        if speed <= 0:
            raise ValueError("Скорость должна быть больше 0")
        
        effective_speed = speed * wind_factor
        return distance / effective_speed
    
    def calculate_distance(self, lat1: float, lon1: float, 
                          lat2: float, lon2: float) -> float:
        """
        Расчет расстояния между двумя точками по формуле гаверсинуса
        
        Args:
            lat1, lon1: Широта и долгота первой точки
            lat2, lon2: Широта и долгота второй точки
            
        Returns:
            Расстояние в км
        """
        # Перевод в радианы
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Разности координат
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        # Формула гаверсинуса
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(dlon/2)**2)
        c = 2 * math.asin(math.sqrt(a))
        
        return self.earth_radius * c
    
    def calculate_altitude_pressure(self, altitude: float) -> float:
        """
        Расчет атмосферного давления на заданной высоте
        
        Args:
            altitude: Высота в метрах
            
        Returns:
            Давление в гПа
        """
        # Стандартное атмосферное давление на уровне моря
        p0 = 1013.25  # гПа
        
        # Температурный градиент
        L = 0.0065  # К/м
        
        # Стандартная температура на уровне моря
        T0 = 288.15  # К
        
        # Универсальная газовая постоянная
        R = 8.31447  # Дж/(моль·К)
        
        # Молярная масса сухого воздуха
        M = 0.0289644  # кг/моль
        
        # Расчет давления
        pressure = p0 * (1 - (L * altitude) / T0) ** ((M * self.gravity) / (R * L))
        
        return pressure
    
    def calculate_mach_number(self, speed: float, altitude: float) -> float:
        """
        Расчет числа Маха
        
        Args:
            speed: Скорость в км/ч
            altitude: Высота в метрах
            
        Returns:
            Число Маха
        """
        # Скорость звука на заданной высоте
        temperature = 288.15 - 0.0065 * altitude  # Температура в К
        speed_of_sound = 20.05 * math.sqrt(temperature)  # м/с
        
        # Скорость в м/с
        speed_ms = speed / 3.6
        
        return speed_ms / speed_of_sound
    
    def calculate_fuel_consumption(self, distance: float, aircraft_type: str) -> float:
        """
        Расчет расхода топлива
        
        Args:
            distance: Расстояние в км
            aircraft_type: Тип самолета
            
        Returns:
            Расход топлива в литрах
        """
        # Базовые коэффициенты расхода топлива (л/100км)
        fuel_rates = {
            "boeing_737": 2.5,
            "airbus_a320": 2.3,
            "boeing_777": 4.2,
            "airbus_a380": 5.8,
            "cessna_172": 0.8,
            "default": 2.0
        }
        
        rate = fuel_rates.get(aircraft_type.lower(), fuel_rates["default"])
        return (distance / 100) * rate
