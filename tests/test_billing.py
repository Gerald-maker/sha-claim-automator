import pytest
from unittest.mock import AsyncMock, MagicMock
from src.billing import (
    open_billing_panel,
    select_billing_category,
    enter_billing_amount,
    save_billing_entry,
    process_billing_category,
    process_all_billing,
    calculate_total,
    validate_prices,
)


# --- calculate_total ---

def test_calculate_total(sample_prices):
    """Total should be sum of all billing categories."""
    total = calculate_total(sample_prices)
    assert total == 1350


def test_calculate_total_zero():
    """Total should be 0 if all prices are 0."""
    prices = {"prescription": 0, "lab": 0, "consultation": 0}
    assert calculate_total(prices) == 0


def test_calculate_total_missing_category():
    """Missing category should default to 0 in total."""
    prices = {"prescription": 750, "lab": 300}
    total = calculate_total(prices)
    assert total == 1050


# --- validate_prices ---

def test_validate_prices_valid(sample_prices):
    """Valid prices should return True."""
    assert validate_prices(sample_prices) is True


def test_validate_prices_missing_category():
    """Missing category should raise ValueError."""
    prices = {"prescription": 750, "lab": 300}
    with pytest.raises(ValueError, match="Missing billing category"):
        validate_prices(prices)


def test_validate_prices_zero_amount():
    """Zero amount should raise ValueError."""
    prices = {"prescription": 0, "lab": 300, "consultation": 300}
    with pytest.raises(ValueError, match="Invalid amount"):
        validate_prices(prices)


def test_validate_prices_negative_amount():
    """Negative amount should raise ValueError."""
    prices = {"prescription": -100, "lab": 300, "consultation": 300}
    with pytest.raises(ValueError, match="Invalid amount"):
        validate_prices(prices)


def test_validate_prices_non_integer():
    """Non-integer amount should raise ValueError."""
    prices = {"prescription": "750", "lab": 300, "consultation": 300}
    with pytest.raises(ValueError, match="Invalid amount"):
        validate_prices(prices)


# --- select_billing_category ---

@pytest.mark.asyncio
async def test_select_billing_category_valid(mock_page):
    """Should successfully select a valid billing category."""
    result = await select_billing_category(mock_page, "prescription")
    assert result is True


@pytest.mark.asyncio
async def test_select_billing_category_invalid(mock_page):
    """Should raise ValueError for unknown category."""
    with pytest.raises(ValueError, match="Unknown billing category"):
        await select_billing_category(mock_page, "unknown")


@pytest.mark.asyncio
async def test_select_billing_category_all(mock_page):
    """Should successfully select all valid categories."""
    for category in ["prescription", "lab", "consultation"]:
        result = await select_billing_category(mock_page, category)
        assert result is True


# --- enter_billing_amount ---

@pytest.mark.asyncio
async def test_enter_billing_amount_success(mock_page):
    """Should successfully enter a billing amount."""
    mock_element = MagicMock()
    mock_element.is_visible = AsyncMock(return_value=True)
    mock_element.scroll_into_view_if_needed = AsyncMock()
    mock_element.focus = AsyncMock()
    mock_element.fill = AsyncMock()
    mock_element.dispatch_event = AsyncMock()
    mock_page.locator = MagicMock(return_value=mock_element)

    result = await enter_billing_amount(mock_page, 750)
    assert result is True


@pytest.mark.asyncio
async def test_enter_billing_amount_failure():
    """Should raise RuntimeError when amount entry fails."""
    page = MagicMock()
    mock_element = MagicMock()
    mock_element.is_visible = AsyncMock(return_value=True)
    mock_element.scroll_into_view_if_needed = AsyncMock()
    mock_element.focus = AsyncMock()
    mock_element.fill = AsyncMock(side_effect=Exception("Fill failed"))
    page.locator = MagicMock(return_value=mock_element)

    with pytest.raises(RuntimeError, match="Failed to enter billing amount"):
        await enter_billing_amount(page, 750)


# --- save_billing_entry ---

@pytest.mark.asyncio
async def test_save_billing_entry_success(mock_page):
    """Should successfully click the save button."""
    result = await save_billing_entry(mock_page)
    assert result is True


@pytest.mark.asyncio
async def test_save_billing_entry_failure():
    """Should raise RuntimeError when save button not found."""
    page = MagicMock()
    mock_element = MagicMock()
    mock_element.is_visible = AsyncMock(return_value=False)
    mock_element.first = mock_element
    page.locator = MagicMock(return_value=mock_element)

    with pytest.raises(RuntimeError, match="Could not find or click Save button"):
        await save_billing_entry(page)


# --- process_all_billing ---

@pytest.mark.asyncio
async def test_process_all_billing_success(mock_page, sample_prices):
    """Should process all billing categories successfully."""
    result = await process_all_billing(mock_page, sample_prices)
    assert result is True


@pytest.mark.asyncio
async def test_process_all_billing_missing_price(mock_page):
    """Should raise ValueError when a price is missing."""
    incomplete_prices = {"prescription": 750, "lab": 300}
    with pytest.raises(ValueError, match="Missing price for category"):
        await process_all_billing(mock_page, incomplete_prices)