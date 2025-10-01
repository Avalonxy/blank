"""
Модуль для работы с аэропортами и маршрутами
"""

from typing import Dict, List, Optional, Tuple
import json


class Airport:
    """Класс для представления аэропорта"""
    
    def __init__(self, icao_code: str, name: str, city: str, 
                 country: str, latitude: float, longitude: float,
                 elevation: float = 0):
        self.icao_code = icao_code
        self.name = name
        self.city = city
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation  # Высота над уровнем моря в метрах
    
    def __str__(self):
        return f"{self.icao_code} - {self.name} ({self.city}, {self.country})"
    
    def to_dict(self) -> Dict:
        """Преобразование в словарь"""
        return {
            "icao_code": self.icao_code,
            "name": self.name,
            "city": self.city,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "elevation": self.elevation
        }


class AirportManager:
    """Менеджер для работы с аэропортами"""
    
    def __init__(self):
        self.airports: Dict[str, Airport] = {}
        self._load_default_airports()
    
    def _load_default_airports(self):
        """Загрузка базовых аэропортов"""
        default_airports = [
            Airport("UUEE", "Шереметьево", "Москва", "Россия", 55.9736, 37.4145, 190),
            Airport("UUDD", "Домодедово", "Москва", "Россия", 55.4146, 37.8994, 179),
            Airport("UUMO", "Внуково", "Москва", "Россия", 55.5915, 37.2615, 209),
            Airport("EGLL", "Хитроу", "Лондон", "Великобритания", 51.4700, -0.4543, 25),
            Airport("LFPG", "Шарль де Голль", "Париж", "Франция", 49.0097, 2.5479, 119),
            Airport("EDDF", "Франкфурт", "Франкфурт", "Германия", 50.0379, 8.5622, 113),
            Airport("KJFK", "Кеннеди", "Нью-Йорк", "США", 40.6413, -73.7781, 4),
            Airport("KLAX", "Лос-Анджелес", "Лос-Анджелес", "США", 33.9416, -118.4085, 38),
            Airport("RJTT", "Ханеда", "Токио", "Япония", 35.5494, 139.7798, 6),
            Airport("ZBAA", "Пекин Столичный", "Пекин", "Китай", 40.0801, 116.5846, 35)
        ]
        
        for airport in default_airports:
            self.airports[airport.icao_code] = airport
    
    def add_airport(self, airport: Airport):
        """Добавление аэропорта"""
        self.airports[airport.icao_code] = airport
    
    def get_airport(self, icao_code: str) -> Optional[Airport]:
        """Получение аэропорта по ICAO коду"""
        return self.airports.get(icao_code.upper())
    
    def search_airports(self, query: str) -> List[Airport]:
        """Поиск аэропортов по названию, городу или стране"""
        query = query.lower()
        results = []
        
        for airport in self.airports.values():
            if (query in airport.name.lower() or 
                query in airport.city.lower() or 
                query in airport.country.lower() or
                query in airport.icao_code.lower()):
                results.append(airport)
        
        return results
    
    def get_airports_by_country(self, country: str) -> List[Airport]:
        """Получение аэропортов по стране"""
        return [airport for airport in self.airports.values() 
                if airport.country.lower() == country.lower()]
    
    def calculate_distance_between_airports(self, icao1: str, icao2: str) -> Optional[float]:
        """Расчет расстояния между двумя аэропортами"""
        airport1 = self.get_airport(icao1)
        airport2 = self.get_airport(icao2)
        
        if not airport1 or not airport2:
            return None
        
        # Используем формулу гаверсинуса
        from math import radians, cos, sin, asin, sqrt
        
        lat1, lon1 = radians(airport1.latitude), radians(airport1.longitude)
        lat2, lon2 = radians(airport2.latitude), radians(airport2.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        # Радиус Земли в км
        earth_radius = 6371
        distance = earth_radius * c
        
        return distance
    
    def get_route_info(self, departure: str, arrival: str) -> Optional[Dict]:
        """Получение информации о маршруте"""
        dep_airport = self.get_airport(departure)
        arr_airport = self.get_airport(arrival)
        
        if not dep_airport or not arr_airport:
            return None
        
        distance = self.calculate_distance_between_airports(departure, arrival)
        
        return {
            "departure": dep_airport.to_dict(),
            "arrival": arr_airport.to_dict(),
            "distance_km": distance,
            "route": f"{dep_airport.icao_code} → {arr_airport.icao_code}"
        }
    
    def export_airports(self, filename: str):
        """Экспорт списка аэропортов в JSON"""
        airports_data = [airport.to_dict() for airport in self.airports.values()]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(airports_data, f, ensure_ascii=False, indent=2)
    
    def import_airports(self, filename: str):
        """Импорт аэропортов из JSON"""
        with open(filename, 'r', encoding='utf-8') as f:
            airports_data = json.load(f)
        
        for airport_data in airports_data:
            airport = Airport(
                icao_code=airport_data['icao_code'],
                name=airport_data['name'],
                city=airport_data['city'],
                country=airport_data['country'],
                latitude=airport_data['latitude'],
                longitude=airport_data['longitude'],
                elevation=airport_data.get('elevation', 0)
            )
            self.add_airport(airport)
