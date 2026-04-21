import asyncio
import logging
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from src.diagnosis import detect_patient_type, select_random_diagnosis, get_prices, select_diagnosis_on_page
from src.billing import process_all_billing, validate_prices

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


class SHAClaimAutomator:
    def __init__(self, headless: bool = False, slow_mo: int = 200):
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None

    async def start(self):
        """Launch the browser and create a new context and page."""
        self._playwright = await async_playwright().start()
        self.browser = await self._playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo,
        )
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        logger.info("✅ Browser started")

    async def stop(self):
        """Close the browser and playwright instance."""
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()
        logger.info("✅ Browser stopped")

    async def navigate(self, url: str):
        """Navigate to a given URL."""
        await self.page.goto(url, wait_until="networkidle")
        logger.info(f"✅ Navigated to: {url}")

    async def process_patient(self) -> dict:
        """
        Full automation flow for a single patient:
        1. Detect patient type (child/adult)
        2. Select a random diagnosis
        3. Select diagnosis on the page
        4. Process all billing
        """
        # Step 1: Detect patient type
        patient = await detect_patient_type(self.page)
        is_child = patient["is_child"]
        name = patient["name"]
        logger.info(f"👤 Patient: {name} ({'Child' if is_child else 'Adult'})")

        # Step 2: Select random diagnosis
        diagnosis = select_random_diagnosis(is_child)
        logger.info(f"🩺 Diagnosis: {diagnosis}")

        # Step 3: Select diagnosis on page
        await select_diagnosis_on_page(self.page, diagnosis)

        # Step 4: Get prices and validate
        prices = get_prices(diagnosis)
        validate_prices(prices)

        # Step 5: Process billing
        await process_all_billing(self.page, prices)

        result = {
            "name": name,
            "is_child": is_child,
            "diagnosis": diagnosis,
            "prices": prices,
            "total": sum(prices.values()),
        }

        logger.info(f"✅ Patient processed: {name} | {diagnosis} | Total: {result['total']}")
        return result

    async def run(self, url: str) -> dict:
        """Main entry point: start browser, navigate, process patient, stop."""
        try:
            await self.start()
            await self.navigate(url)
            result = await self.process_patient()
            return result
        except Exception as e:
            logger.error(f"❌ Automation failed: {e}")
            raise
        finally:
            await self.stop()


async def main():
    import os
    from dotenv import load_dotenv
    load_dotenv()

    url = os.getenv("SHA_URL", "https://your-sha-portal-url.com")
    automator = SHAClaimAutomator(headless=False, slow_mo=300)
    result = await automator.run(url)
    print(f"\n✅ Done: {result}")


if __name__ == "__main__":
    asyncio.run(main())