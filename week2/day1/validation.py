from pydantic import BaseModel, field_validator


class User(BaseModel):
    password: str

    @field_validator("password")
    def check_password(cls, value):

        if "@" not in value:
            raise ValueError(
                "Password must contain @"
            )

        return value


#test
User(password="Ali123")
User(password="Ali123@")