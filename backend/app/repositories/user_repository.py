from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    @property
    def collection_name(self) -> str:
        return "users"

    async def create_user(self, user: User) -> User:
        document = user.model_dump(exclude={"id"})

        inserted_id = await self.create(document)

        return User(
            id=inserted_id,
            **document,
        )

    async def find_by_email(self, email: str) -> User | None:
        document = await self.collection.find_one({"email": email})

        if document is None:
            return None

        document["id"] = str(document.pop("_id"))

        return User.model_validate(document)
