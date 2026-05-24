"""
Card data model
"""

from pydantic import BaseModel, field_validator


class CardError(Exception):
    """Card parsing failed"""


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
        # Only use numbered list for definitions if there are multiple
        if len(self.definition) > 1:
            definition_str = "<br/>".join(
                f"{i + 1}. {d}" for i, d in enumerate(self.definition)
            )
        else:
            definition_str = self.definition[0] if self.definition else ""

        return {
            "word": self.word,
            "category": self.category,
            "definition": definition_str,
            "forms": " | ".join(self.forms),
            "example": "<br/><br/>".join(self.example),
            "reverse": "<br/><br/>".join(self.reverse),
        }

    @classmethod
    def from_csv_row(cls, row: dict[str, str]) -> "Card":
        """Create Card from CSV row dict"""
        raw_definitions = row["definition"].split("<br/>") if row["definition"] else []
        definitions = [
            d.split(". ", 1)[1] if ". " in d and d[0].isdigit() else d
            for d in raw_definitions
        ]
        return cls(
            word=row["word"],
            category=row["category"],
            definition=definitions,
            forms=row["forms"].split(" | ") if row["forms"] else [],
            example=row["example"].split("<br/><br/>") if row["example"] else [],
            reverse=row["reverse"].split("<br/><br/>") if row["reverse"] else [],
        )
