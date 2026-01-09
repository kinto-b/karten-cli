"""
Card data model
"""

from pydantic import BaseModel, field_validator


class CardError(Exception):
    """Card could not be created"""


class Card(BaseModel):
    """Card data from LLM"""

    word: str
    category: str
    definition: list[str]
    forms: list[str]
    example: list[str]
    reverse: list[str]

    @field_validator("definition", "forms", "example", "reverse", mode="before")
    @classmethod
    def ensure_list(cls, v):
        """Ensure field is a list, convert string to single-item list"""
        if v is None:
            return []
        if isinstance(v, str):
            return [v]
        if not isinstance(v, list):
            raise ValueError(f"Expected list or string, got {type(v)}")
        return v

    @field_validator("*", mode="before")
    @classmethod
    def none_to_empty(cls, v):
        """Convert None to empty string or empty list based on field type"""
        if v is None:
            return ""
        return v

    @classmethod
    def from_json(cls, json_str: str) -> "Card":
        """Parse JSON string into Card with validation"""
        try:
            return cls.model_validate_json(json_str)
        except Exception as e:
            raise CardError(f"Failed to parse card JSON: {json_str}") from e

    def to_csv_row(self) -> dict[str, str]:
        """Format card for CSV export"""
        return {
            "word": self.word,
            "category": self.category,
            "definition": "; ".join(self.definition),
            "forms": " | ".join(self.forms),
            "example": "<br/><br/>".join(self.example),
            "reverse": "<br/><br/>".join(self.reverse),
        }
