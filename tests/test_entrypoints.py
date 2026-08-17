import importlib

from myproject import database


def test_get_session_yields_session():
    gen = database.get_session()
    db = next(gen)
    try:
        # basic smoke checks
        assert hasattr(db, "query")
    finally:
        # close generator to run cleanup
        gen.close()


def test_main_on_startup_calls_init_db(monkeypatch):
    called = {"ok": False}

    def fake_init_db():
        called["ok"] = True

    monkeypatch.setattr(database, "init_db", fake_init_db)

    # reload main so it binds to the monkeypatched database.init_db
    main = importlib.reload(importlib.import_module("myproject.main"))
    # call the startup function directly
    main.on_startup()
    assert called["ok"] is True
