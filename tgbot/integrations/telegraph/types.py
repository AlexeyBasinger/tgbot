from pydantic import Field, BaseModel, validator

from tgbot.integrations.telegraph.config import BASE_TELEGRAPH_API_LINK


class UploadedFile(BaseModel):
    link: str = Field(..., alias="src")

    @validator("link")
    def link_validator(cls, value: str):
        return BASE_TELEGRAPH_API_LINK.format(endpoint=value)