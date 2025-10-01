"""
Тесты для модуля FlightCalculator
"""

import pytest
from aviation_lib.flight_calculator import FlightCalculator


class TestFlightCalculator:
    """Тесты для FlightCalculator"""
    
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.calc = FlightCalculator()
    
    def test_calculate_flight_time(self):
        """Тест расчета времени полета"""
        # Нормальные условия
        time = self.calc.calculate_flight_time(1000, 800)
        assert time == 1.25
        
        # С учетом ветра
        time_wind = self.calc.calculate_flight_time(1000, 800, 0.8)
        assert time_wind == 1.5625
    
    def test_calculate_flight_time_invalid_speed(self):
        """Тест с неверной скоростью"""
        with pytest.raises(ValueError):
            self.calc.calculate_flight_time(1000, 0)
        
        with pytest.raises(ValueError):
            self.calc.calculate_flight_time(1000, -100)
    
    def test_calculate_distance(self):
        """Тест расчета расстояния между точками"""
        # Москва - Санкт-Петербург (примерно 635 км)
        distance = self.calc.calculate_distance(55.7558, 37.6176, 59.9311, 30.3609)
        assert 600 < distance < 700
    
    def test_calculate_altitude_pressure(self):
        """Тест расчета давления на высоте"""
        # Давление на уровне моря
        pressure_sea = self.calc.calculate_altitude_pressure(0)
        assert 1000 < pressure_sea < 1020
        
        # Давление на высоте 1000м
        pressure_1000m = self.calc.calculate_altitude_pressure(1000)
        assert pressure_1000m < pressure_sea
    
    def test_calculate_mach_number(self):
        """Тест расчета числа Маха"""
        mach = self.calc.calculate_mach_number(800, 10000)
        assert 0.5 < mach < 1.0
    
    def test_calculate_fuel_consumption(self):
        """Тест расчета расхода топлива"""
        fuel = self.calc.calculate_fuel_consumption(1000, "boeing_737")
        assert fuel > 0
        
        # Проверка разных типов самолетов
        fuel_cessna = self.calc.calculate_fuel_consumption(1000, "cessna_172")
        fuel_boeing = self.calc.calculate_fuel_consumption(1000, "boeing_737")
        assert fuel_cessna < fuel_boeing
