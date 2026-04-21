import asyncio
import logging
from src.utils import wait, safe_click, type_amount, find_billing_button, is_billing_button_loaded

logger = logging.getLogger(__name__)

BILLING_CATEGORIES = ["prescription", "lab", "consultation"]


async def open_billing_panel(page) -> bool:
    """Open the billing panel by clicking the billing button."""
    MAX_ATTEMPTS = 5
    RETRY_DELAY = 500

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            logger.info(f"Opening billing panel (attempt {attempt})...")

            # Wait for billing button to load
            loaded = await is_billing_button_loaded(page)
            if not loaded:
                logger.warning(f"⚠️ Billing button not loaded yet (attempt {attempt})")
                await wait(RETRY_DELAY)
                continue

            billing_btn = await find_billing_button(page)
            if billing_btn:
                await billing_btn.scroll_into_view_if_needed()
                await billing_btn.click()
                await asyncio.sleep(0.5)
                logger.info("✅ Billing panel opened")
                return True

        except Exception as e:
            logger.warning(f"⚠️ Billing panel open attempt {attempt} failed: {e}")
            await wait(RETRY_DELAY)

    raise RuntimeError("Failed to open billing panel after multiple attempts")


async def select_billing_category(page, category: str) -> bool:
    """Select a billing category tab (prescription, lab, consultation)."""
    SELECTORS = {
        "prescription": 'a[href="#prescription"]',
        "lab": 'a[href="#lab"]',
        "consultation": 'a[href="#consultation"]',
    }

    selector = SELECTORS.get(category.lower())
    if not selector:
        raise ValueError(f"Unknown billing category: {category}")

    for attempt in range(1, 4):
        try:
            tab = page.locator(selector).first
            await tab.scroll_into_view_if_needed()
            await tab.click()
            await asyncio.sleep(0.3)
            logger.info(f"✅ Selected billing category: {category}")
            return True
        except Exception as e:
            logger.warning(f"⚠️ Category select attempt {attempt} failed: {e}")
            await asyncio.sleep(0.3)

    raise RuntimeError(f"Failed to select billing category: {category}")


async def enter_billing_amount(page, amount: int) -> bool:
    """Enter a billing amount into the input field."""
    success = await type_amount(page, amount)
    if not success:
        raise RuntimeError(f"Failed to enter billing amount: {amount}")
    return True


async def save_billing_entry(page) -> bool:
    """Click the save button to submit a billing entry."""
    SAVE_SELECTORS = [
        'button[ng-click="saveBilling()"]',
        'button.btn-primary.btn-sm:has-text("Save")',
        'button:has-text("Save")',
    ]

    for selector in SAVE_SELECTORS:
        try:
            btn = page.locator(selector).first
            if await btn.is_visible():
                await btn.scroll_into_view_if_needed()
                await btn.click()
                await asyncio.sleep(0.5)
                logger.info(f"✅ Billing entry saved (selector: {selector})")
                return True
        except Exception:
            continue

    raise RuntimeError("Could not find or click Save button")


async def process_billing_category(page, category: str, amount: int) -> bool:
    """Process a single billing category: select tab, enter amount, save."""
    logger.info(f"Processing billing: {category} = {amount}")

    await select_billing_category(page, category)
    await asyncio.sleep(0.3)

    await enter_billing_amount(page, amount)
    await asyncio.sleep(0.2)

    await save_billing_entry(page)
    await asyncio.sleep(0.5)

    logger.info(f"✅ Billing complete: {category} = {amount}")
    return True


async def process_all_billing(page, prices: dict) -> bool:
    """Process all billing categories for a patient visit."""
    await open_billing_panel(page)
    await asyncio.sleep(0.5)

    for category in BILLING_CATEGORIES:
        amount = prices.get(category)
        if amount is None:
            raise ValueError(f"Missing price for category: {category}")
        await process_billing_category(page, category, amount)

    logger.info("✅ All billing categories processed successfully")
    return True


def calculate_total(prices: dict) -> int:
    """Calculate the total billing amount."""
    return sum(prices.get(cat, 0) for cat in BILLING_CATEGORIES)


def validate_prices(prices: dict) -> bool:
    """Validate that all required billing categories have positive amounts."""
    for category in BILLING_CATEGORIES:
        amount = prices.get(category)
        if amount is None:
            raise ValueError(f"Missing billing category: {category}")
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError(f"Invalid amount for {category}: {amount}")
    return True