"""Check Library Loans specification Sections 2 and 3.2."""

import pytest

from src.library_eligibility import can_borrow


@pytest.mark.parametrize(
    "active_loans, overdue_books, expected",
    [
        pytest.param(0, 0, True, id="no-loans-no-overdue"),
        pytest.param(1, 0, True, id="ordinary-eligible-reader"),
        pytest.param(4, 0, True, id="just-below-loan-limit"),
        pytest.param(5, 0, False, id="at-loan-limit"),
        pytest.param(6, 0, False, id="above-loan-limit"),
        pytest.param(100, 0, False, id="many-active-loans"),
        pytest.param(0, 1, False, id="overdue-book-no-active-loans"),
        pytest.param(4, 1, False, id="below-limit-but-overdue"),
        pytest.param(5, 1, False, id="at-limit-and-overdue"),
        pytest.param(6, 1, False, id="above-limit-and-overdue"),
        pytest.param(0, 100, False, id="many-overdue-books"),
    ],
)
def test_valid_counts_return_expected_boolean(active_loans, overdue_books, expected):
    # Arrange: the data covers the loan boundary and both borrowing conditions.
    # Act
    result = can_borrow(active_loans, overdue_books)

    # Assert: identity also rejects 1 and 0 as Boolean return values.
    assert result is expected


@pytest.mark.parametrize(
    "active_loans, overdue_books",
    [(-1, 0), (0, -1), (-1, -1)],
    ids=["negative-active-loans", "negative-overdue-books", "both-negative"],
)
def test_negative_counts_raise_value_error(active_loans, overdue_books):
    with pytest.raises(ValueError):
        can_borrow(active_loans, overdue_books)


@pytest.mark.parametrize(
    "active_loans",
    [True, False, 1.0, "1", None, [], {}],
    ids=["bool-true", "bool-false", "float", "string", "none", "list", "dict"],
)
def test_noninteger_active_loans_raise_type_error(active_loans):
    # Keep the other argument valid to isolate this parameter's validation.
    with pytest.raises(TypeError):
        can_borrow(active_loans, 0)


@pytest.mark.parametrize(
    "overdue_books",
    [True, False, 1.0, "1", None, [], {}],
    ids=["bool-true", "bool-false", "float", "string", "none", "list", "dict"],
)
def test_noninteger_overdue_books_raise_type_error(overdue_books):
    # Keep the other argument valid to isolate this parameter's validation.
    with pytest.raises(TypeError):
        can_borrow(0, overdue_books)
