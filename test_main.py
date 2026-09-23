"""Tests der im Feedback beschriebenen Bestellungen ueber das Menue."""

import pytest

from main import main


@pytest.mark.parametrize(
    "answers, expected, remaining",
    [
        (["3", "1", "1", "1", "1", "", "", "1", "4"],
         "Order made! Total payment: $2175.0", 98),
        (["3", "5", "1", "5", "1", "", "", "1", "4"],
         "Error while making order!", 100),
        (["3", "1", "2", "5", "2", "", "", "1", "4"],
         "Error while making order!", 100),
    ],
)
def test_feedback_scenarios_through_menu(
        monkeypatch, capsys, answers, expected, remaining):
    inputs = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    main()
    output = capsys.readouterr().out
    assert expected in output
    final_listing = output.rsplit("1. MacBook Air M2,", 1)[1]
    assert f"Quantity:{remaining}," in final_listing
    if expected.startswith("Error"):
        assert "Order made!" not in output
        assert "Shipping, Price: $10 Quantity:250" in final_listing


def test_menu_lists_inventory_and_handles_invalid_choice(monkeypatch, capsys):
    inputs = iter(["invalid", "1", "2", "4"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    main()
    output = capsys.readouterr().out
    assert "Error with your choice!" in output
    assert "Windows License, Price: $125 Quantity:Unlimited" in output
    assert "Total of 1100 items in store" in output
    assert "Bye!" in output
