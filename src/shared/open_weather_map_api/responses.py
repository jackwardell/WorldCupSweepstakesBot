from typing import TypedDict, List


class WeatherCoodResponse(TypedDict):
    lat: float
    lon: float


class WeatherMainResponse(TypedDict):
    feels_like: float
    humidity: int
    pressure: int
    temp: float
    temp_max: int
    temp_min: int


class WeatherSysResponse(TypedDict):
    country: str
    id: int
    sunrise: int
    sunset: int
    type: int


class SubWeatherResponse(TypedDict):
    description: str
    icon: str
    id: int
    main: str


class WeatherWindResponse(TypedDict):
    deg: int
    speed: float


class WeatherResponse(TypedDict):
    base: str
    cod: int
    coord: WeatherCoodResponse
    dt: int
    id: int
    main: WeatherMainResponse
    name: str
    sys: WeatherSysResponse
    timezone: int
    visibility: int
    weather: List[SubWeatherResponse]
    wind: WeatherWindResponse
