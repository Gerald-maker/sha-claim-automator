import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_page():
    """Create a mock Playwright page object."""
    page = MagicMock()

    # Make locator return a mock element
    mock_element = MagicMock()
    mock_element.is_visible = AsyncMock(return_value=True)
    mock_element.click = AsyncMock()
    mock_element.fill = AsyncMock()
    mock_element.focus = AsyncMock()
    mock_element.scroll_into_view_if_needed = AsyncMock()
    mock_element.dispatch_event = AsyncMock()
    mock_element.text_content = AsyncMock(return_value="John Doe")

    page.locator = MagicMock(return_value=mock_element)
    page.goto = AsyncMock()

    return page


@pytest.fixture
def mock_element():
    """Create a standalone mock element."""
    element = MagicMock()
    element.is_visible = AsyncMock(return_value=True)
    element.click = AsyncMock()
    element.fill = AsyncMock()
    element.focus = AsyncMock()
    element.scroll_into_view_if_needed = AsyncMock()
    element.dispatch_event = AsyncMock()
    element.text_content = AsyncMock(return_value="Test Patient")
    return element


@pytest.fixture
def sample_prices():
    """Sample billing prices for testing."""
    return {
        "prescription": 750,
        "lab": 300,
        "consultation": 300,
    }


@pytest.fixture
def adult_diagnosis():
    """A known adult diagnosis for testing."""
    return "Peptic ulcer, site unspecified"


@pytest.fixture
def child_diagnosis():
    """A known child diagnosis for testing."""
    return "Acute tonsillitis, unspecified"