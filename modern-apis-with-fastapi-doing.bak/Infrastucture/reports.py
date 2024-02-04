import datetime
from typing import Optional

from pydantic import BaseModel

from models.location import Location


class ReportSubmittal(BaseModel):
    description: str
    location: Location


class Report(ReportSubmittal):
    created_date: Optional[datetime.datetime]
    id: str
