from pydantic import BaseModel

class Token(BaseModel):
    """Schema for returning a JWT token."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for the data contained within the JWT."""
    username: str | None = None


class User(BaseModel):
    """Schema for user data."""
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "johndoe",
                    "email": "johndoe@example.com",
                    "full_name": "John Doe",
                    "disabled": False
                }
            ]
        }
    }


class UserInDB(User):
    """Schema for user data stored in the database (includes hashed password)."""
    hashed_password: str
