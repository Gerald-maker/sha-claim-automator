import pytest
from unittest.mock import AsyncMock, MagicMock
from src.diagnosis import (
    get_diagnosis_pool,
    select_random_diagnosis,
    get_prices,
    detect_patient_type,
    select_diagnosis_on_page,
    ADULT_DIAGNOSES,
    CHILD_DIAGNOSES,
    DIAGNOSIS_PRICES,
)


# --- get_diagnosis_pool ---

def test_get_diagnosis_pool_adult():
    """Adult pool should return ADULT_DIAGNOSES."""
    pool = get_diagnosis_pool(is_child=False)
    assert pool == ADULT_DIAGNOSES


def test_get_diagnosis_pool_child():
    """Child pool should return CHILD_DIAGNOSES."""
    pool = get_diagnosis_pool(is_child=True)
    assert pool == CHILD_DIAGNOSES


# --- select_random_diagnosis ---

def test_select_random_diagnosis_adult():
    """Selected adult diagnosis should be in ADULT_DIAGNOSES."""
    diagnosis = select_random_diagnosis(is_child=False)
    assert diagnosis in ADULT_DIAGNOSES


def test_select_random_diagnosis_child():
    """Selected child diagnosis should be in CHILD_DIAGNOSES."""
    diagnosis = select_random_diagnosis(is_child=True)
    assert diagnosis in CHILD_DIAGNOSES


def test_select_random_diagnosis_returns_string():
    """Diagnosis should always be a non-empty string."""
    diagnosis = select_random_diagnosis(is_child=False)
    assert isinstance(diagnosis, str)
    assert len(diagnosis) > 0


# --- get_prices ---

def test_get_prices_valid(adult_diagnosis):
    """Valid diagnosis should return a dict with all billing categories."""
    prices = get_prices(adult_diagnosis)
    assert isinstance(prices, dict)
    assert "prescription" in prices
    assert "lab" in prices
    assert "consultation" in prices


def test_get_prices_all_positive(adult_diagnosis):
    """All prices should be positive integers."""
    prices = get_prices(adult_diagnosis)
    for category, amount in prices.items():
        assert isinstance(amount, int), f"{category} is not an int"
        assert amount > 0, f"{category} is not positive"


def test_get_prices_invalid_diagnosis():
    """Unknown diagnosis should raise ValueError."""
    with pytest.raises(ValueError, match="No prices found"):
        get_prices("Unknown Diagnosis XYZ")


def test_all_diagnoses_have_prices():
    """Every diagnosis in both pools should have prices defined."""
    all_diagnoses = ADULT_DIAGNOSES + CHILD_DIAGNOSES
    for diagnosis in all_diagnoses:
        prices = get_prices(diagnosis)
        assert prices is not None, f"Missing prices for: {diagnosis}"


# --- detect_patient_type ---

@pytest.mark.asyncio
async def test_detect_patient_type_child():
    """Should detect child patient correctly."""
    page = MagicMock()

    child_element = MagicMock()
    child_element.is_visible = AsyncMock(return_value=True)
    child_element.text_content = AsyncMock(return_value="Mary Wanjiku")

    adult_element = MagicMock()
    adult_element.is_visible = AsyncMock(return_value=False)

    def locator_side_effect(selector):
        mock = MagicMock()
        if selector == '[data-child-highlighted="true"]':
            mock.first = child_element
        else:
            mock.first = adult_element
        return mock

    page.locator = MagicMock(side_effect=locator_side_effect)

    result = await detect_patient_type(page)
    assert result["is_child"] is True
    assert result["name"] == "Mary"


@pytest.mark.asyncio
async def test_detect_patient_type_adult():
    """Should detect adult patient correctly."""
    page = MagicMock()

    child_element = MagicMock()
    child_element.is_visible = AsyncMock(return_value=False)

    adult_element = MagicMock()
    adult_element.is_visible = AsyncMock(return_value=True)
    adult_element.text_content = AsyncMock(return_value="John Kamau")

    def locator_side_effect(selector):
        mock = MagicMock()
        if selector == '[data-child-highlighted="true"]':
            mock.first = child_element
        else:
            mock.first = adult_element
        return mock

    page.locator = MagicMock(side_effect=locator_side_effect)

    result = await detect_patient_type(page)
    assert result["is_child"] is False
    assert result["name"] == "John"


@pytest.mark.asyncio
async def test_detect_patient_type_fails():
    """Should raise RuntimeError when patient type cannot be determined."""
    page = MagicMock()
    mock_element = MagicMock()
    mock_element.is_visible = AsyncMock(return_value=False)
    mock_element.first = mock_element
    page.locator = MagicMock(return_value=mock_element)

    with pytest.raises(RuntimeError, match="Could not determine patient type"):
        await detect_patient_type(page)


# --- select_diagnosis_on_page ---

@pytest.mark.asyncio
async def test_select_diagnosis_on_page_success(adult_diagnosis):
    """Should successfully select a diagnosis on the page."""
    page = MagicMock()

    mock_element = MagicMock()
    mock_element.is_visible = AsyncMock(return_value=True)
    mock_element.click = AsyncMock()
    mock_element.focus = AsyncMock()
    mock_element.fill = AsyncMock()
    mock_element.scroll_into_view_if_needed = AsyncMock()
    mock_element.dispatch_event = AsyncMock()
    mock_element.first = mock_element

    page.locator = MagicMock(return_value=mock_element)

    result = await select_diagnosis_on_page(page, adult_diagnosis, delay=0)
    assert result is True


@pytest.mark.asyncio
async def test_select_diagnosis_on_page_fails(adult_diagnosis):
    """Should raise RuntimeError after 3 failed attempts."""
    page = MagicMock()
    mock_element = MagicMock()
    mock_element.is_visible = AsyncMock(return_value=True)
    mock_element.click = AsyncMock(side_effect=Exception("Click failed"))
    mock_element.first = mock_element
    page.locator = MagicMock(return_value=mock_element)

    with pytest.raises(RuntimeError, match="Diagnosis selection failed"):
        await select_diagnosis_on_page(page, adult_diagnosis, delay=0)