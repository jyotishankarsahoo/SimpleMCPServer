from mcp.server.fastmcp import FastMCP
import playwright
import asyncio
import base64
from playwright.async_api import Page, async_playwright, Browser

page: Page = None
browser: Browser = None
playwright_instance = None

mcp = FastMCP("playwright-mcp-server")

async def _ensure_browser():
    """Ensure Page and Browser are Initialized"""
    global page, browser, playwright_instance

    if browser is None or page is None:
        playwright_instance = await async_playwright().start()
        browser = await playwright_instance.chromium.launch(headless=False)
        page = await browser.new_page()