import asyncio
import logging

logger = logging.getLogger(__name__)


async def wait(ms: int) -> None:
    """Wait for a given number of milliseconds."""
    await asyncio.sleep(ms / 1000)


async def safe_click(page, selector: str) -> bool:
    """Safely scroll to and click an element."""
    try:
        element = page.locator(selector).first
        await element.scroll_into_view_if_needed()
        await element.click()
        logger.info(f"✅ Clicked: {selector}")
        return True
    except Exception as e:
        logger.warning(f"⚠️ Could not click {selector}: {e}")
        return False


async def type_amount(page, amount: int) -> bool:
    """Type a billing amount into the amount input field."""
    try:
        # Primary selector
        input_selector = '#silInlineForm_input_unit_price_0'
        fallback_selector = 'input[id^="silInlineForm_input_unit_price_"]'

        input_field = page.locator(input_selector).first
        if not await input_field.is_visible():
            logger.warning("Primary input not found, trying fallback...")
            input_field = page.locator(fallback_selector).first

        await input_field.scroll_into_view_if_needed()
        await input_field.focus()
        await input_field.fill(str(amount))
        await input_field.dispatch_event('input')
        await input_field.dispatch_event('change')
        logger.info(f"✅ Typed amount: {amount}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to type amount {amount}: {e}")
        return False


async def find_billing_button(page):
    """Find the billing button using primary or fallback selectors."""
    try:
        # Primary selector
        primary = page.locator('span.fs-17 > strong').first
        if await primary.is_visible():
            logger.info("✅ Found billing button (primary selector)")
            return primary

        # Fallback - find by text
        fallback = page.locator('strong').filter(has_text='Billing').first
        if await fallback.is_visible():
            logger.info("✅ Found billing button (fallback selector)")
            return fallback

        logger.warning("⚠️ Billing button not found")
        return None
    except Exception as e:
        logger.warning(f"⚠️ Error finding billing button: {e}")
        return None


async def is_billing_button_loaded(page) -> bool:
    """Check if the billing button is visible and clickable."""
    try:
        button = await find_billing_button(page)
        if button and await button.is_visible():
            return True
        return False
    except Exception:
        return False