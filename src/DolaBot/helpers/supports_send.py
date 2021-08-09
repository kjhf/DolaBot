from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class SupportsSend(Protocol):
    """An ABC with one abstract method send()."""
    __slots__ = ()

    @abstractmethod
    async def send(self, content=None, *, tts=False, embed=None, file=None,
                   files=None, delete_after=None, nonce=None,
                   allowed_mentions=None, reference=None,
                   mention_author=None):
        pass
