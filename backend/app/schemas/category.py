from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import CategoryType


class CreateCategoryRequest(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )
    type: CategoryType


class UpdateCategoryRequest(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    type: CategoryType | None = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    type: CategoryType
    is_system: bool
