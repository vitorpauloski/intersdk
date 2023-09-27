from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from intersdk.misc.typing import TokenScope


@dataclass
class Token:
    token_type: str
    access_token: str
    scope: list[TokenScope]
    expires_in: datetime

    @property
    def expired(self) -> bool:
        return self.expires_in - timedelta(minutes=1) <= datetime.now(tz=timezone.utc).replace(tzinfo=None)

    @property
    def authorization_header(self) -> str:
        return f"{self.token_type} {self.access_token}"
