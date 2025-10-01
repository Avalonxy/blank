"""
Примеры использования AviationLib
"""

from aviation_lib import FlightCalculator, WeatherAnalyzer, AirportManager, FuelCalculator


def main():
    """Основная функция с примерами"""
    
    print("=== AviationLib - Примеры использования ===\n")
    
    # 1. Расчет параметров полета
    print("1. Расчет параметров полета:")
    calc = FlightCalculator()
    
    # Время полета
    flight_time = calc.calculate_flight_time(1000, 800, 0.9)
    print(f"Время полета: {flight_time:.2f} часов")
    
    # Расстояние между городами
    distance = calc.calculate_distance(55.7558, 37.6176, 59.9311, 30.3609)  # Москва - СПб
    print(f"Расстояние Москва-СПб: {distance:.0f} км")
    
    # Давление на высоте
    pressure = calc.calculate_altitude_pressure(10000)
    print(f"Давление на высоте 10000м: {pressure:.1f} гПа")
    
    print()
    
    # 2. Анализ погоды
    print("2. Анализ погодных условий:")
    weather = WeatherAnalyzer()
    
    conditions = weather.analyze_conditions(
        temperature=15,
        pressure=1013,
        wind_speed=12,
        visibility=8000
    )
    
    print(f"Общее состояние: {conditions['overall_condition']}")
    print(f"Рекомендации: {', '.join(conditions['recommendations'])}")
    
    # Ветроохлаждение
    wind_chill = weather.calculate_wind_chill(5, 15)
    print(f"Ощущаемая температура: {wind_chill:.1f}°C")
    
    print()
    
    # 3. Работа с аэропортами
    print("3. Работа с аэропортами:")
    airport_mgr = AirportManager()
    
    # Поиск аэропортов
    moscow_airports = airport_mgr.search_airports("Москва")
    print(f"Аэропорты Москвы: {len(moscow_airports)}")
    for airport in moscow_airports:
        print(f"  - {airport}")
    
    # Расстояние между аэропортами
    distance_airports = airport_mgr.calculate_distance_between_airports("UUEE", "EGLL")
    print(f"Расстояние Шереметьево-Хитроу: {distance_airports:.0f} км")
    
    # Информация о маршруте
    route_info = airport_mgr.get_route_info("UUEE", "EGLL")
    if route_info:
        print(f"Маршрут: {route_info['route']}")
        print(f"Расстояние: {route_info['distance_km']:.0f} км")
    
    print()
    
    # 4. Расчет топлива
    print("4. Расчет топливной эффективности:")
    fuel_calc = FuelCalculator()
    
    # Расход топлива
    fuel_consumption = fuel_calc.calculate_fuel_consumption(2000, "boeing_737")
    print(f"Расход топлива на 2000км: {fuel_consumption.total_fuel:.0f} л")
    print(f"Время полета: {fuel_consumption.flight_time:.2f} часов")
    print(f"Расход на 100км: {fuel_consumption.fuel_per_100km:.1f} л")
    
    # Стоимость топлива
    fuel_cost = fuel_calc.calculate_fuel_cost(fuel_consumption, 50)  # 50 руб/л
    print(f"Стоимость топлива: {fuel_cost:.0f} руб")
    
    # Сравнение самолетов
    aircraft_comparison = fuel_calc.compare_aircraft_efficiency(
        1000, ["boeing_737", "airbus_a320", "cessna_172"]
    )
    print("\nСравнение эффективности самолетов на 1000км:")
    for aircraft in aircraft_comparison:
        print(f"  {aircraft['aircraft_type']}: {aircraft['efficiency']:.1f} км/л")
    
    print("\n=== Примеры завершены ===")


if __name__ == "__main__":
    main()
