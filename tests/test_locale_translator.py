import pytest
from src.constants.locale_translator import LocaleTranslator

@pytest.fixture
def LT() -> LocaleTranslator:
    return LocaleTranslator.get_instance()

def test_get_key(LT: LocaleTranslator):
    assert LT.get("orb_period") == "Orbital Period"
    assert LT.get("kase") == "key_kase"