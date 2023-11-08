from dataclasses import dataclass, field, asdict, fields


@dataclass
class UserSessionData:
    childhood: str = "Not provided"
    relationship: str = "Not provided"
    mbti: str = "No last session"
    working: str = "Not provided"
    summary: str = "No last session"
    insight: str = "No last session"
    prompt: str = field(default_factory=str)
    transcript: str = field(default_factory=str)

    def to_dict(self):
        return asdict(self)


@dataclass
class PersistentUserData:
    last_session: str = "None"
    mbti: str = "idk"
