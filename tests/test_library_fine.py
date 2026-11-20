"""Check Library Loans specification Sections 2 and 3.1."""

import pytest

from src.library_fine import calculate_fine


@pytest.mark.parametrize(
    "days_overdue, expected_cents",
    [
        pytest.param(0, 0, id="zero-days"),
        pytest.param(1, 50, id="one-day"),
        pytest.param(2, 100, id="ordinary-positive-days"),
        pytest.param(9, 450, id="nine-days"),
        pytest.param(10, 500, id="ten-days"),
        pytest.param(11, 550, id="eleven-days-no-cap"),
        pytest.param(100, 5000, id="large-value-no-cap"),
    ],
)
def test_nonnegative_days_return_expected_integer_fine(days_overdue, expected_cents):
    # Arrange: each row supplies an input and the requirement-based expectation.
    # Act
    result = calculate_fine(days_overdue)

    # Assert: the amount is in cents and must be an actual int.
    assert result == expected_cents
    assert type(result) is int


@pytest.mark.parametrize("days_overdue", [-1, -100], ids=["below-zero", "negative-days"])
def test_negative_days_raise_value_error(days_overdue):
    with pytest.raises(ValueError):
        calculate_fine(days_overdue)


@pytest.mark.parametrize(
    "days_overdue",
    [True, False, 1.0, "1", None, [], {}],
    ids=["bool-true", "bool-false", "float", "string", "none", "list", "dict"],
)
def test_noninteger_days_raise_type_error(days_overdue):
    with pytest.raises(TypeError):
        calculate_fine(days_overdue)
