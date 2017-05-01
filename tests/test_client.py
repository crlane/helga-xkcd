import pytest

from helga_xkcd.client import XKCDClient


@pytest.fixture
def client():
    return XKCDClient()


def test_uses_https(client):
    assert client.BASE.startswith('https')
