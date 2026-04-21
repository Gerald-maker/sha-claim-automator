import random
import logging

logger = logging.getLogger(__name__)

DIAGNOSIS_PRICES = {
    "Peptic ulcer, site unspecified": {"prescription": 750, "lab": 300, "consultation": 300},
    "Gastritis, unspecified": {"prescription": 750, "lab": 300, "consultation": 300},
    "Essential hypertension, unspecified": {"prescription": 700, "lab": 300, "consultation": 300},
    "Diabetes mellitus, type unspecified": {"prescription": 800, "lab": 400, "consultation": 300},
    "Allergic asthma": {"prescription": 700, "lab": 200, "consultation": 300},
    "Urinary tract infection, site and agent not specified": {"prescription": 650, "lab": 250, "consultation": 300},
    "Epilepsy or seizures, unspecified": {"prescription": 700, "lab": 300, "consultation": 300},
    "Functional diarrhoea": {"prescription": 750, "lab": 250, "consultation": 300},
    "Malaria due to Plasmodium falciparum, unspecified": {"prescription": 800, "lab": 300, "consultation": 300},
    "Alcoholic gastritis": {"prescription": 750, "lab": 300, "consultation": 300},
    "Acute bronchitis, unspecified": {"prescription": 750, "lab": 300, "consultation": 300},
    "Typhoid fever, unspecified": {"prescription": 750, "lab": 300, "consultation": 300},
    "Pneumonia due to Streptococcus pneumoniae": {"prescription": 650, "lab": 200, "consultation": 300},
    "Acute upper respiratory infection, site unspecified": {"prescription": 500, "lab": 200, "consultation": 300},
    "Acute tonsillitis, unspecified": {"prescription": 650, "lab": 200, "consultation": 300},
    "Tinea nigra": {"prescription": 700, "lab": 200, "consultation": 300},
    "Cystitis, unspecified": {"prescription": 650, "lab": 250, "consultation": 300},
    "Migraine, unspecified": {"prescription": 700, "lab": 200, "consultation": 300},
    "Dental caries": {"prescription": 650, "lab": 200, "consultation": 300},
    "Streptococcal cellulitis of skin": {"prescription": 800, "lab": 300, "consultation": 300},
    "Other specified conjunctivitis": {"prescription": 700, "lab": 200, "consultation": 300},
    "Atopic eczema, unspecified": {"prescription": 750, "lab": 200, "consultation": 300},
    "Other allergic rhinitis": {"prescription": 750, "lab": 250, "consultation": 300},
    "Gastroenteritis or colitis without specification of origin": {"prescription": 700, "lab": 250, "consultation": 300},
    "Allergic contact dermatitis due to food allergen": {"prescription": 700, "lab": 200, "consultation": 300},
    "Otitis media, unspecified": {"prescription": 700, "lab": 200, "consultation": 300},
}

ADULT_DIAGNOSES = [
    "Peptic ulcer, site unspecified",
    "Gastritis, unspecified",
    "Essential hypertension, unspecified",
    "Diabetes mellitus, type unspecified",
    "Urinary tract infection, site and agent not specified",
    "Epilepsy or seizures, unspecified",
    "Functional diarrhoea",
    "Malaria due to Plasmodium falciparum, unspecified",
    "Alcoholic gastritis",
    "Typhoid fever, unspecified",
    "Acute bronchitis, unspecified",
    "Dental caries",
    "Cystitis, unspecified",
    "Streptococcal cellulitis of skin",
    "Migraine, unspecified",
    "Allergic asthma",
]

CHILD_DIAGNOSES = [
    "Pneumonia due to Streptococcus pneumoniae",
    "Acute upper respiratory infection, site unspecified",
    "Acute tonsillitis, unspecified",
    "Tinea nigra",
    "Otitis media, unspecified",
    "Other specified conjunctivitis",
    "Gastroenteritis or colitis without specification of origin",
    "Allergic contact dermatitis due to food allergen",
    "Streptococcal cellulitis of skin",
    "Other allergic rhinitis",
    "Atopic eczema, unspecified",
]


def get_diagnosis_pool(is_child: bool) -> list:
    """Return the appropriate diagnosis pool based on patient type."""
    return CHILD_DIAGNOSES if is_child else ADULT_DIAGNOSES


def select_random_diagnosis(is_child: bool) -> str:
    """Randomly select a diagnosis from the appropriate pool."""
    pool = get_diagnosis_pool(is_child)
    selected = random.choice(pool)
    logger.info(f"✅ Selected diagnosis ({'Child' if is_child else 'Adult'}): {selected}")
    return selected


def get_prices(diagnosis: str) -> dict:
    """Get billing prices for a given diagnosis."""
    prices = DIAGNOSIS_PRICES.get(diagnosis)
    if not prices:
        raise ValueError(f"No prices found for diagnosis: {diagnosis}")
    return prices


async def detect_patient_type(page) -> dict:
    """Detect whether the patient is a child or adult from the page."""
    MAX_ATTEMPTS = 5
    RETRY_DELAY = 200

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            # Check for child indicator
            child_element = page.locator('[data-child-highlighted="true"]').first
            if await child_element.is_visible():
                name = (await child_element.text_content()).strip().split()[0]
                logger.info(f"✅ Child patient detected: {name}")
                return {"is_child": True, "name": name}

            # Check for adult patient name
            adult_element = page.locator('.patient-name').first
            if await adult_element.is_visible():
                name = (await adult_element.text_content()).strip().split()[0]
                logger.info(f"✅ Adult patient detected: {name}")
                return {"is_child": False, "name": name}

        except Exception as e:
            logger.warning(f"⚠️ Patient detection attempt {attempt} failed: {e}")

        if attempt < MAX_ATTEMPTS:
            import asyncio
            await asyncio.sleep(RETRY_DELAY / 1000)

    raise RuntimeError("Could not determine patient type after multiple attempts")


async def select_diagnosis_on_page(page, diagnosis: str, delay: float = 0.333) -> bool:
    """Perform diagnosis selection on the page."""
    import asyncio

    for attempt in range(1, 4):
        try:
            logger.info(f"Diagnosis attempt {attempt}: {diagnosis}")

            # Click Add button
            add_btn = page.locator('button.btn-success.btn-sm.m-r-5.text-uppercase').first
            if await add_btn.is_visible():
                await add_btn.click()
                await asyncio.sleep(delay)

            # Type diagnosis
            input_field = page.locator('input[type="text"]:visible').first
            await input_field.focus()
            await input_field.fill(diagnosis)
            await input_field.dispatch_event('input')
            await asyncio.sleep(1)

            # Click matching result
            match = page.locator(f'text="{diagnosis}"').first
            await match.click()
            await asyncio.sleep(delay)

            # Click Save
            save_btn = page.locator('button[ng-disabled="inline.loader"].btn-primary.btn-sm').first
            await save_btn.scroll_into_view_if_needed()
            await asyncio.sleep(0.2)
            await save_btn.click()
            await asyncio.sleep(delay)

            logger.info(f"✅ Diagnosis selected: {diagnosis}")
            return True

        except Exception as e:
            logger.warning(f"⚠️ Diagnosis attempt {attempt} failed: {e}")

    raise RuntimeError(f"Diagnosis selection failed after 3 attempts: {diagnosis}")