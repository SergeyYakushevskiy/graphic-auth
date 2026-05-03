from pydantic import BaseModel, Field, field_validator


class Argon2Config(BaseModel):
    time_cost: int = Field(ge=1)
    memory_cost: int = Field(ge=8 * 1024)  # минимум ~8MB
    parallelism: int = Field(ge=1)
    hash_len: int = Field(ge=16, le=64)

    @field_validator("memory_cost")
    @classmethod
    def memory_multiple_of_1024(cls, v: int):
        if v % 1024 != 0:
            raise ValueError("memory_cost must be multiple of 1024")
        return v


class AppSettings(BaseModel):
    argon2: Argon2Config
