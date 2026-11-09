import pandas as pd

from nido.checks import check_allowed_values, check_min, check_not_null, check_unique


def test_check_unique_passes_on_unique_column():
    df = pd.DataFrame({"order_id": ["O1", "O2", "O3"]})
    assert check_unique(df, "order_id") == []


def test_check_unique_reports_duplicates():
    df = pd.DataFrame({"order_id": ["O1", "O1", "O2"]})
    failures = check_unique(df, "order_id")
    assert len(failures) == 1
    assert "order_id" in failures[0]


def test_check_not_null_one_message_per_column():
    df = pd.DataFrame({"a": [1, None], "b": [None, None], "c": [1, 2]})
    failures = check_not_null(df, ["a", "b", "c"])
    assert len(failures) == 2


def test_check_allowed_values_lists_unexpected_values():
    df = pd.DataFrame({"country": ["DE", "AT", "Germany"]})
    failures = check_allowed_values(df, "country", {"DE", "AT"})
    assert len(failures) == 1
    assert "Germany" in failures[0]


def test_check_allowed_values_ignores_nulls():
    df = pd.DataFrame({"country": ["DE", None]})
    assert check_allowed_values(df, "country", {"DE"}) == []


def test_check_min():
    df = pd.DataFrame({"quantity": [1, 0, -1, 5]})
    assert check_min(df, "quantity", 1) == ["quantity: 2 values below 1"]
    assert check_min(df, "quantity", -5) == []
