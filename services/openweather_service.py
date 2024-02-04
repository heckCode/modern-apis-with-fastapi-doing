from typing import Optional, Tuple
import httpx
from httpx import Response

from Infrastucture import weather_cache
from models.validation_error import ValidationError

api_key: Optional[str] = None


async def get_report_async(city: str, state: Optional[str], country: str, units: str) -> dict:
    # Validate the inputted data
    city, state, country, units = validate_units(city, state, country, units)

    # Check the cache
    forecast = weather_cache.get_weather(city, state, country, units)
    if forecast:
        return forecast

    # Get the data from the weather service
    if state:
        q = f"{city},{state},{country}"
    else:
        q = f"{city},{state},{country}"

    url = (f"https://api.openweathermap.org/data/2.5/weather?q={q}"
           f"&appid={api_key}&units={units}")

    async with httpx.AsyncClient() as client:
        response: Response = await client.get(url)
        if response.status_code != 200:
            # raise httpx.HTTPStatusError(f"Error talking to weather provider.",
            #                             request=response.request, response=response)
            raise ValidationError(response.text, status_code=response.status_code)

    data = response.json()
    forecast = data["main"]

    # Cache the result
    weather_cache.set_weather(city, state, country, units, forecast)

    return forecast


def validate_units(
        city: str, state: Optional[str], country: Optional[str], units: str
) -> Tuple[str, Optional[str], str, str]:
    city = city.lower().strip()
    if not country:
        country = 'us'
    else:
        country = country.lower().strip()

    if len(country) != 2:
        error = f'Invalid country: {country}. It must be a two letter abbreviation such as US or GB.'
        raise ValidationError(error_msg=error, status_code=400)

    if state:
        state = state.strip().lower()

    if state and len(state) != 2:
        error = f'Invalid state: {state}. It must be a two letter abbreviation such as CA or KS (use for US only).'
        raise ValidationError(error_msg=error, status_code=400)

    if units:
        units = units.strip().lower()

    valid_units = {'standard', 'metric', 'imperial'}
    if units not in valid_units:
        error = f"Invalid units '{units}', it must be one of {valid_units}."
        raise ValidationError(error_msg=error, status_code=400)

    return city, state, country, units
