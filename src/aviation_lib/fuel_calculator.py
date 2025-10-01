"""
Модуль для расчета топливной эффективности
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class FuelConsumption:
    """Данные о расходе топлива"""
    total_fuel: float  # Общий расход топлива в литрах
    fuel_per_100km: float  # Расход на 100 км
    fuel_per_hour: float  # Расход в час
    flight_time: float  # Время полета в часах
    distance: float  # Расстояние в км


class FuelCalculator:
    """Калькулятор топливной эффективности"""
    
    def __init__(self):
        # Базовые характеристики самолетов (расход л/100км)
        self.aircraft_profiles = {
            "boeing_737": {
                "fuel_rate": 2.5,  # л/100км
                "cruise_speed": 800,  # км/ч
                "max_range": 5000,  # км
                "fuel_capacity": 26000  # л
            },
            "airbus_a320": {
                "fuel_rate": 2.3,
                "cruise_speed": 820,
                "max_range": 5500,
                "fuel_capacity": 24000
            },
            "boeing_777": {
                "fuel_rate": 4.2,
                "cruise_speed": 900,
                "max_range": 15000,
                "fuel_capacity": 180000
            },
            "airbus_a380": {
                "fuel_rate": 5.8,
                "cruise_speed": 900,
                "max_range": 15000,
                "fuel_capacity": 320000
            },
            "cessna_172": {
                "fuel_rate": 0.8,
                "cruise_speed": 200,
                "max_range": 1000,
                "fuel_capacity": 200
            },
            "default": {
                "fuel_rate": 2.0,
                "cruise_speed": 600,
                "max_range": 3000,
                "fuel_capacity": 5000
            }
        }
    
    def calculate_fuel_consumption(self, distance: float, aircraft_type: str,
                                 wind_factor: float = 1.0, 
                                 payload_factor: float = 1.0) -> FuelConsumption:
        """
        Расчет расхода топлива
        
        Args:
            distance: Расстояние в км
            aircraft_type: Тип самолета
            wind_factor: Коэффициент влияния ветра (0.8-1.2)
            payload_factor: Коэффициент загрузки (0.8-1.2)
            
        Returns:
            Данные о расходе топлива
        """
        profile = self.aircraft_profiles.get(aircraft_type.lower(), 
                                            self.aircraft_profiles["default"])
        
        # Базовый расход топлива
        base_fuel_rate = profile["fuel_rate"]
        
        # Корректировка на ветер и загрузку
        adjusted_fuel_rate = base_fuel_rate * wind_factor * payload_factor
        
        # Расчет времени полета
        cruise_speed = profile["cruise_speed"]
        flight_time = distance / cruise_speed
        
        # Расчет общего расхода топлива
        total_fuel = (distance / 100) * adjusted_fuel_rate
        
        # Расход в час
        fuel_per_hour = total_fuel / flight_time if flight_time > 0 else 0
        
        return FuelConsumption(
            total_fuel=total_fuel,
            fuel_per_100km=adjusted_fuel_rate,
            fuel_per_hour=fuel_per_hour,
            flight_time=flight_time,
            distance=distance
        )
    
    def calculate_fuel_efficiency(self, distance: float, fuel_used: float) -> float:
        """
        Расчет топливной эффективности
        
        Args:
            distance: Расстояние в км
            fuel_used: Использованное топливо в литрах
            
        Returns:
            Эффективность в км/л
        """
        if fuel_used <= 0:
            return 0
        
        return distance / fuel_used
    
    def calculate_fuel_cost(self, fuel_consumption: FuelConsumption, 
                           fuel_price: float) -> float:
        """
        Расчет стоимости топлива
        
        Args:
            fuel_consumption: Данные о расходе топлива
            fuel_price: Цена топлива за литр
            
        Returns:
            Стоимость топлива
        """
        return fuel_consumption.total_fuel * fuel_price
    
    def calculate_optimal_speed(self, aircraft_type: str, distance: float) -> float:
        """
        Расчет оптимальной скорости для минимального расхода топлива
        
        Args:
            aircraft_type: Тип самолета
            distance: Расстояние в км
            
        Returns:
            Оптимальная скорость в км/ч
        """
        profile = self.aircraft_profiles.get(aircraft_type.lower(),
                                            self.aircraft_profiles["default"])
        
        # Для коротких расстояний оптимальная скорость ниже
        if distance < 1000:
            return profile["cruise_speed"] * 0.9
        elif distance < 3000:
            return profile["cruise_speed"] * 0.95
        else:
            return profile["cruise_speed"]
    
    def calculate_fuel_reserve(self, aircraft_type: str, distance: float) -> float:
        """
        Расчет резерва топлива
        
        Args:
            aircraft_type: Тип самолета
            distance: Расстояние в км
            
        Returns:
            Резерв топлива в литрах
        """
        profile = self.aircraft_profiles.get(aircraft_type.lower(),
                                            self.aircraft_profiles["default"])
        
        # Стандартный резерв: 30 минут полета + 5% от общего расхода
        base_consumption = self.calculate_fuel_consumption(distance, aircraft_type)
        reserve_30min = base_consumption.fuel_per_hour * 0.5
        reserve_5percent = base_consumption.total_fuel * 0.05
        
        return reserve_30min + reserve_5percent
    
    def get_aircraft_info(self, aircraft_type: str) -> Dict:
        """Получение информации о самолете"""
        return self.aircraft_profiles.get(aircraft_type.lower(),
                                         self.aircraft_profiles["default"])
    
    def compare_aircraft_efficiency(self, distance: float, 
                                  aircraft_types: List[str]) -> List[Dict]:
        """
        Сравнение топливной эффективности разных самолетов
        
        Args:
            distance: Расстояние в км
            aircraft_types: Список типов самолетов
            
        Returns:
            Список с данными о эффективности
        """
        results = []
        
        for aircraft_type in aircraft_types:
            consumption = self.calculate_fuel_consumption(distance, aircraft_type)
            efficiency = self.calculate_fuel_efficiency(distance, consumption.total_fuel)
            
            results.append({
                "aircraft_type": aircraft_type,
                "fuel_consumption": consumption.total_fuel,
                "efficiency": efficiency,
                "flight_time": consumption.flight_time,
                "fuel_per_100km": consumption.fuel_per_100km
            })
        
        # Сортировка по эффективности (больше км/л = лучше)
        results.sort(key=lambda x: x["efficiency"], reverse=True)
        
        return results
