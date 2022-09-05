import requests

from config import settings
from dto.api import TwelveDataInfo


def get_twelvedata_info() -> TwelveDataInfo:
    resp = requests.get(settings.scheduler_conn + "twelveDataInfo")

    return TwelveDataInfo(**resp.json())
