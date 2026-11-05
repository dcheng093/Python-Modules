from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from enum import Enum


class ContactType(Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_info(self) -> "AlienContact":
        contact_id = self.contact_id
        contact_type = self.contact_type
        signal = self.signal_strength
        witnesses = self.witness_count
        message = self.message_received
        verified = self.is_verified
        if not contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC' (Alien Contact)")
        if contact_type == ContactType.physical and not verified:
            raise ValueError("Physical contact reports must be verified")
        if contact_type == ContactType.telepathic and witnesses < 3:
            raise ValueError("Telepathic contact requires at least 3 "
                             "witnesses")
        if signal > 7.0 and not message:
            raise ValueError("Strong signals (> 7.0) should include "
                             "received messages")
        return self


def contact_demo() -> None:
    print("Alien Contact Log Validation")
    try:
        print("======================================")
        ac = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.radio,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli"
        )
        print("Valid contact report:")
        print(f"ID: {ac.contact_id}")
        print(f"Type: {ac.contact_type.value}")
        print(f"Location: {ac.location}")
        print(f"Signal: {ac.signal_strength}/10")
        print(f"Duration: {ac.duration_minutes} minutes")
        print(f"Witnesses: {ac.witness_count}")
        print(f"Message: '{ac.message_received}'")
    except ValidationError as e:
        print("Validation error:")
        for error in e.errors():
            print(error["msg"])
    print("\n======================================")
    try:
        AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.telepathic,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli"
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            msg = error["msg"].replace("Value error, ", "")
            print(msg)


if __name__ == "__main__":
    contact_demo()
