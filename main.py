import asyncio
import json
from pathlib import Path

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from api import weather_api
from models.location import Location
from services import openweather_service, report_service
from views import home

api = fastapi.FastAPI()


def configure():
    configure_routing()
    configure_api_keys()


def configure_api_keys():
    file = Path("settings.json").absolute()
    if not file.exists():
        print(f"WARNING: {file} file found, API keys cannot be loaded")
        raise Exception("settings.json file not found, API keys cannot be loaded")

    with open(file) as fin:
        settings = json.load(fin)
        openweather_service.api_key = settings.get("api_key")


def configure_fake_data():
    # This was added to make it easier to test the weather event reporting
    # We have /api/reports but until you submit new data each run, it's missing
    # So this will give us something to start from
    loc = Location(city="Portland", state="OR", country="US")
    asyncio.run(report_service.add_report(description="The weather is nice", location=loc))
    asyncio.run(report_service.add_report(description="It's raining, I'm wet", location=loc))



def configure_routing():
    api.mount("/static", StaticFiles(directory="static"), name="static")
    api.include_router(router=home.router)
    api.include_router(router=weather_api.router)


if __name__ == "__main__":
    configure()
    uvicorn.run("main:api", port=8000, host='127.0.0.1')
else:
    configure()
