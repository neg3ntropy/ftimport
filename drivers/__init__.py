from pathlib import Path
from typing import Optional

from selenium import webdriver
from webdriverdownloader import ChromeDriverDownloader, GeckoDriverDownloader

DRIVERS_ROOT = Path(__file__).parent.resolve()
DOWNLOAD_DIR = DRIVERS_ROOT / "cache"
BIN_DIR = DOWNLOAD_DIR / "bin"

GECKODRIVER_VERSION = "v0.24.0"
CHROMEDRIVER_VERSION = "75.0.3770.140"


def get_driver_path(driver: str) -> Optional[str]:
    if not driver:
        return None
    driver = driver.lower()
    if driver in ("firefox", "gecko"):
        downloader_class = GeckoDriverDownloader
        version = GECKODRIVER_VERSION
    elif driver in ("chrome", "chromium"):
        downloader_class = ChromeDriverDownloader
        version = CHROMEDRIVER_VERSION
    else:
        return None

    downloader = downloader_class(DOWNLOAD_DIR, BIN_DIR)
    exe, _link = downloader.download_and_install(version, show_progress_bar=False)
    return exe


def get_driver():
    options = webdriver.FirefoxOptions()
    options.profile = webdriver.FirefoxProfile("profile")
    return webdriver.Firefox(
        executable_path=get_driver_path("firefox"), options=options
    )
