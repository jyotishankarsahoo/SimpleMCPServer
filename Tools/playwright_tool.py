from mcp.server.fastmcp import FastMCP
import asyncio
import subprocess
import logging
import sys
from playwright.async_api import Page, async_playwright, Browser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("playwright-browser-mcp")

mcp = FastMCP("playwright-mcp-server")

page: Page = None
browser: Browser = None
playwright_instance = None

def install_playwright_browser():
    """Check and installs Chromium if missing"""
    try:
        logger.info("Verifying Chromium installation...")
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"], 
            check=True, 
            capture_output= True
        )
        logger.info("Chromium is installed and ready.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install Chromium: {e.stderr}")

async def _ensure_browser():
    """Ensure Page and Browser are Initialized"""
    # Run installation check first
    install_playwright_browser()
    global page, browser, playwright_instance
    logger.info("Starting Playwright...")
    if browser is None or page is None:
        playwright_instance = await async_playwright().start()
        browser = await playwright_instance.chromium.launch(headless=False)
        page = await browser.new_page()
        logger.info("Browser Successfully initialized")

@mcp.tool()
async def navigate(url) -> str:
    "Navigates to the given URL"
    try:
        await _ensure_browser()
        await page.goto(url, wait_until= "domcontentloaded")
        page_title = await page.title()
        return f"Navigated to {url}\n Page title {page_title}"
    except Exception as e:
        return f"Error navigating to {url}: {str(e)}"

@mcp.tool()
async def click(selector: str) -> str:
    """Click an element on the page"""
    try:
        await _ensure_browser()
        await page.click(selector)
    except Exception as e:
        logger.error(f"Error clicking element {selector}: {e}")
        return f"Error clicking element {selector}: {e}"

@mcp.tool()
async def fill(selector: str, value: str) -> str:
    """Fill value in selector on the page"""
    try:
        await _ensure_browser()
        
        await page.fill(selector, value)
    except Exception as e:
        logger.error(f"Error filling element {selector}: {e}")
        return f"Error filling element {selector}: {e}"

@mcp.tool()
async def evaluate_js(script: str) -> str:
    """Execute Javascript on the page"""
    try:
        await _ensure_browser()
        await page.evaluate(script)
    except Exception as e:
        logger.error(f"Error evaluating JS {script}: {e}")
        return f"Error evaluating JS {script}: {e}"

@mcp.tool()
async def get_text_content() -> str:
    """Get Visible Text Content of the Page"""
    try:
        await _ensure_browser()
        content = await page.locator("body").inner_text()
        if len(content) > 1000:
            content = content[:1000] + "...(truncated)"
        return f"Page Content: \n\n{content}"
    except Exception as e:
        logger.error(f"Error getting page content: {e}")
        return f"Error getting page content: {e}"

if __name__ == "__main__":
    try:
        mcp.run()
    finally:
        logger.info("Shutting down browser...")
        if browser:
            asyncio.run(browser.close())
        if playwright_instance:
            asyncio.run(playwright_instance.stop())
        print("Playwright MCP server is running and resources are cleaned up")