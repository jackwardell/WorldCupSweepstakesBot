from typing import Generator

import pytest
from src.shared.bot_api.api import get_engine
from src.shared.bot_api.db import Base


@pytest.fixture(scope="function", autouse=True)
def setup(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    monkeypatch.setenv("TESTING", "true")
    Base.metadata.drop_all(get_engine())
    Base.metadata.create_all(get_engine())
    yield
    monkeypatch.delenv("TESTING")
