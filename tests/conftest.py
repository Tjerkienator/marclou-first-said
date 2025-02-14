import pytest

# Enable pytest-asyncio for the entire test suite
pytest_plugins = ('pytest_asyncio',)

# Set asyncio mode to auto
def pytest_configure(config):
    config.addinivalue_line("asyncio_mode", "auto") 