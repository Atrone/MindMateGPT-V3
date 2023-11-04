from dataclasses import dataclass, field, asdict


@dataclass
class UserSessionData:
    childhood: str = field(default_factory=str)
    relationship: str = field(default_factory=str)
    mbti: str = field(default_factory=str)
    working: str = field(default_factory=str)
    summary: str = field(default_factory=str)
    insight: str = field(default_factory=str)
    prompt: str = field(default_factory=str)
    transcript: str = field(default_factory=str)

    def to_dict(self):
        return asdict(self)

@dataclass
class PersistentUserData:
    last_session: str = "None"
    mbti: str = "idk"
