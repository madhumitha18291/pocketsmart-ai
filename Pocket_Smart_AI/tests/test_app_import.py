import importlib


def test_main_module_imports():
    module = importlib.import_module("app.main")
    assert module.app is not None
    assert module.settings.app_name
