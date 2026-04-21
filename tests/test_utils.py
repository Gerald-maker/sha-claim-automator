import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.utils import wait, safe_click, type_amount, find_billing_button, is_billing_button_loaded


@pytest.mark.asyncio
async def test_wait():
    """Test that wait completes without error."""
    await wait(100)


@pytest.mark.asyncio
async def test_safe_click_success(mock_page):
    """Test safe_click returns True when element is clickable."""
    result = await safe_click(mock_page, "button.test")
    assert result is True


@pytest.mark.asyncio
async def test_safe_click_failure():
    """Test safe_click returns False when element raises an exception."""
    page = MagicMock()
    mock_element = MagicMock()
    mock_element.scroll_into_view_if_needed = AsyncMock(side_effect=Exception("Not found"))
    page.locator = MagicMock(return_value=mock_element)

    result = await safe_click(page, "button.missing")
    assert result is False


@pytest.mark.asyncio
async def test_type_amount_success(mock_page):
    """Test type_amount returns True on success."""
    mock_element = MagicMock()
    mock_element.is_visible = AsyncMock(return_value=True)
    mock_element.scroll_into_view_if_needed = AsyncMock()
    mock_element.focus = AsyncMock()
    mock_element.fill = AsyncMock()
    mock_element.dispatch_event = AsyncMock()
    mock_page.locator = MagicMock(return_value=mock_element)

    result = await type_amount(mock_page, 750)
    assert result is True
    mock_element.fill.assert_called_once_with("750")


@pytest.mark.asyncio
async def test_type_amount_failure():
    """Test type_amount returns False when fill raises an exception."""
    page = MagicMock()
    mock_element = MagicMock()
    mock_element.is_visible = AsyncMock(return_value=True)
    mock_element.scroll_into_view_if_needed = AsyncMock()
    mock_element.focus = AsyncMock()
    mock_element.fill = AsyncMock(side_effect=Exception("Fill failed"))
    page.locator = MagicMock(return_value=mock_element)

    result = await type_amount(page, 500)
    assert result is False


@pytest.mark.asyncio
async def test_find_billing_button_primary(mock_page):
    """Test find_billing_button returns element using primary selector."""
    result = await find_billing_button(mock_page)
    assert result is not None


@pytest.mark.asyncio
async def test_find_billing_button_fallback():
    """Test find_billing_button falls back to secondary selector."""
    page = MagicMock()

    primary = MagicMock()
    primary.is_visible = AsyncMock(return_value=False)

    fallback = MagicMock()
    fallback.is_visible = AsyncMock(return_value=True)

    def locator_side_effect(selector, **kwargs):
        mock = MagicMock()
        if selector == 'span.fs-17 > strong':
            mock.first = primary
        else:
            mock.first = fallback
        return mock

    page.locator = MagicMock(side_effect=locator_side_effect)

    result = await find_billing_button(page)
    assert result is not None


@pytest.mark.asyncio
async def test_find_billing_button_not_found():
    """Test find_billing_button returns None when no button found."""
    page = MagicMock()
    mock_element = MagicMock()
    mock_element.is_visible = AsyncMock(return_value=False)
    mock_element.first = mock_element
    page.locator = MagicMock(return_value=mock_element)

    result = await find_billing_button(page)
    assert result is None


@pytest.mark.asyncio
async def test_is_billing_button_loaded_true(mock_page):
    """Test is_billing_button_loaded returns True when button is visible."""
    result = await is_billing_button_loaded(mock_page)
    assert result is True


@pytest.mark.asyncio
async def test_is_billing_button_loaded_false():
    """Test is_billing_button_loaded returns False when button not visible."""
    page = MagicMock()
    mock_element = MagicMock()
    mock_element.is_visible = AsyncMock(return_value=False)
    mock_element.first = mock_element
    page.locator = MagicMock(return_value=mock_element)

    result = await is_billing_button_loaded(page)
    assert result is False