"""
Модуль для анализа метеорологических условий
"""

from typing import Dict, List, Tuple
from enum import Enum


class WeatherCondition(Enum):
    """Типы погодных условий"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    DANGEROUS = "dangerous"


class WeatherAnalyzer:
    """Анализатор погодных условий для авиации"""
    
    def __init__(self):
        self.visibility_thresholds = {
            "excellent": 10000,  # м
            "good": 5000,
            "fair": 2000,
            "poor": 1000,
            "dangerous": 500
        }
        
        self.wind_thresholds = {
            "excellent": 10,  # м/с
            "good": 15,
            "fair": 20,
            "poor": 25,
            "dangerous": 30
        }
    
    def analyze_conditions(self, temperature: float, pressure: float, 
                          wind_speed: float, visibility: float = None) -> Dict:
        """
        Анализ погодных условий
        
        Args:
            temperature: Температура в °C
            pressure: Давление в гПа
            wind_speed: Скорость ветра в м/с
            visibility: Видимость в метрах (опционально)
            
        Returns:
            Словарь с анализом условий
        """
        conditions = {
            "temperature": temperature,
            "pressure": pressure,
            "wind_speed": wind_speed,
            "visibility": visibility,
            "overall_condition": self._get_overall_condition(
                temperature, pressure, wind_speed, visibility
            ),
            "recommendations": self._get_recommendations(
                temperature, pressure, wind_speed, visibility
            )
        }
        
        return conditions
    
    def _get_overall_condition(self, temperature: float, pressure: float,
                              wind_speed: float, visibility: float = None) -> str:
        """Определение общего состояния погоды"""
        
        # Проверка видимости
        if visibility is not None:
            if visibility < self.visibility_thresholds["dangerous"]:
                return WeatherCondition.DANGEROUS.value
            elif visibility < self.visibility_thresholds["poor"]:
                return WeatherCondition.POOR.value
        
        # Проверка ветра
        if wind_speed > self.wind_thresholds["dangerous"]:
            return WeatherCondition.DANGEROUS.value
        elif wind_speed > self.wind_thresholds["poor"]:
            return WeatherCondition.POOR.value
        
        # Проверка давления (нормальное: 1013 гПа)
        pressure_deviation = abs(pressure - 1013)
        if pressure_deviation > 50:
            return WeatherCondition.POOR.value
        
        # Проверка температуры (экстремальные значения)
        if temperature < -40 or temperature > 50:
            return WeatherCondition.POOR.value
        
        # Определение общего состояния
        if (wind_speed < self.wind_thresholds["excellent"] and 
            pressure_deviation < 20 and 
            (visibility is None or visibility > self.visibility_thresholds["excellent"])):
            return WeatherCondition.EXCELLENT.value
        elif (wind_speed < self.wind_thresholds["good"] and 
              pressure_deviation < 30):
            return WeatherCondition.GOOD.value
        else:
            return WeatherCondition.FAIR.value
    
    def _get_recommendations(self, temperature: float, pressure: float,
                           wind_speed: float, visibility: float = None) -> List[str]:
        """Получение рекомендаций по полету"""
        recommendations = []
        
        if wind_speed > self.wind_thresholds["fair"]:
            recommendations.append("Осторожно: сильный ветер")
        
        if pressure < 1000:
            recommendations.append("Внимание: низкое давление")
        elif pressure > 1030:
            recommendations.append("Внимание: высокое давление")
        
        if visibility is not None and visibility < self.visibility_thresholds["good"]:
            recommendations.append("Ограниченная видимость")
        
        if temperature < -20:
            recommendations.append("Экстремально низкая температура")
        elif temperature > 40:
            recommendations.append("Экстремально высокая температура")
        
        if not recommendations:
            recommendations.append("Условия благоприятны для полета")
        
        return recommendations
    
    def calculate_wind_chill(self, temperature: float, wind_speed: float) -> float:
        """
        Расчет ощущаемой температуры с учетом ветра
        
        Args:
            temperature: Температура в °C
            wind_speed: Скорость ветра в м/с
            
        Returns:
            Ощущаемая температура в °C
        """
        if wind_speed < 1.3:
            return temperature
        
        # Формула расчета ветроохлаждения
        wind_chill = (13.12 + 0.6215 * temperature - 
                     11.37 * (wind_speed * 3.6) ** 0.16 + 
                     0.3965 * temperature * (wind_speed * 3.6) ** 0.16)
        
        return wind_chill
    
    def get_weather_summary(self, conditions: Dict) -> str:
        """Получение краткого описания погодных условий"""
        condition = conditions["overall_condition"]
        
        summaries = {
            "excellent": "Отличные условия для полета",
            "good": "Хорошие условия для полета", 
            "fair": "Удовлетворительные условия",
            "poor": "Плохие условия, требуется осторожность",
            "dangerous": "Опасные условия, полет не рекомендуется"
        }
        
        return summaries.get(condition, "Неопределенные условия")
