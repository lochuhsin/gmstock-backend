from pydantic import BaseModel


class TwelveDataInfo(BaseModel):
    plan: str
    global_: list[str]

    class Config:
        fields = {
            'global_': 'global'
        }

