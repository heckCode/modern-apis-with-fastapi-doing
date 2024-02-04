import pytest
from httpx import Response, Request
from services.openweather_service import get_report_async
from unittest.mock import AsyncMock
import httpx


@pytest.mark.asyncio
async def test_get_report_async_raises_http_status_error(mocker):
    # Create a mock request object
    mock_request = Request(method="GET", url="http://test/")

    # Mock the AsyncClient's get method to return a Response with the mock request
    mock_get = AsyncMock(
        return_value=Response(
            status_code=500,
            json={"error": "Internal Server Error"},
            request=mock_request
        )
    )

    # Use mocker to patch the get method of httpx.AsyncClient
    mocker.patch('httpx.AsyncClient.get', new=mock_get)

    # Ensure that the appropriate exception is raised for a non-200 status code
    with pytest.raises(httpx.HTTPStatusError):
        await get_report_async(
            city="test_city",
            state="test_state",
            country="test_country",
            units="metric")
