from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from everkept.api import create_app
from everkept.platform.clock import FakeClock
from everkept.platform.config import Settings


def test_healthz() -> None:
    client = TestClient(create_app(Settings(env="test")))
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_demo_mode_refused_in_prod() -> None:
    with pytest.raises(RuntimeError):
        create_app(Settings(env="prod", demo_mode=True))


def test_fake_clock_advances_and_never_rewinds() -> None:
    clock = FakeClock()
    start = clock.now()
    clock.advance(timedelta(days=90))
    assert clock.now() - start == timedelta(days=90)
    with pytest.raises(ValueError):
        clock.advance(timedelta(seconds=-1))
