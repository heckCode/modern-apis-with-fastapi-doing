import datetime
import uuid
from typing import List

from Infrastucture.reports import Report
from models.location import Location

__reports: List[Report] = []


async def get_reports() -> List[Report]:

    # Would be an async call here
    return list(__reports)


async def add_report(description: str, location: Location) -> Report:
    now = datetime.datetime.now()
    report = Report(
        id=str(uuid.uuid4()),
        description=description,
        location=location,
        created_date=now
    )

    # Simulate saving to the database
    # Would be an async call here
    __reports.append(report)
    __reports.sort(key=lambda r: r.created_date, reverse=True)

    return report