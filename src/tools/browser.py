import os
import time
import base64
from typing import Dict, Any, Optional, List
from crewai.tools import BaseTool
from pydantic import Field, BaseModel

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import (
        TimeoutException, 
        NoSuchElementException, 
        WebDriverException
    )
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

class BrowserUseToolSchema(BaseModel):
    """Schema for the Browser Use Tool"""
    action: str = Field(description="The browser action to perform (visit, click, etc.)")
    url: Optional[str] = Field(None, description="URL for navigation actions")
    selector: Optional[str] = Field(None, description="CSS selector for finding elements")
    text: Optional[str] = Field(None, description="Text for input actions")
    index: Optional[int] = Field(None, description="Element index for multiple matches")
    script: Optional[str] = Field(None, description="JavaScript code to execute")
    scroll_amount: Optional[int] = Field(None, description="Pixels to scroll")
    tab_id: Optional[int] = Field(None, description="Tab ID for switching tabs")
    timeout: int = Field(10, description="Maximum wait time in seconds")

class BrowserUseTool(BaseTool):
    """Tool for automating web browser interactions."""
    
    name: str = "Browser Use"
    description: str = """Interact with a web browser to perform various actions such as navigation, 
element interaction, content extraction, and screenshot capture.

Use this tool when you need to:
- Navigate to a web page
- Click on elements
- Input text into forms
- Extract content from websites
- Take screenshots
- Scroll web pages
- Execute JavaScript"""
    args_schema = BrowserUseToolSchema
    
    def __init__(self):
        super().__init__()
        self._driver = None
        self._tabs = {}
        self._current_tab_id = None
    
    def _ensure_driver_initialized(self) -> bool:
        """Initialize the web driver if not already done."""
        if not SELENIUM_AVAILABLE:
            return False
            
        if self._driver is None:
            try:
                # Set up Chrome options
                chrome_options = Options()
                chrome_options.add_argument("--headless")  # Run in headless mode
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                
                # Initialize the driver
                self._driver = webdriver.Chrome(options=chrome_options)
                
                # Set window size
                self._driver.set_window_size(1366, 768)
                
                # Initialize tab tracking
                self._current_tab_id = 0
                self._tabs = {0: self._driver.current_window_handle}
                
                return True
            except Exception as e:
                # Log the specific exception for debugging
                print(f"Error initializing Chrome WebDriver: {str(e)}")
                return False
        
        return True
    
    def _run(self, action: str, url: Optional[str] = None, selector: Optional[str] = None,
            text: Optional[str] = None, index: Optional[int] = None, script: Optional[str] = None,
            scroll_amount: Optional[int] = None, tab_id: Optional[int] = None, timeout: int = 10) -> Dict[str, Any]:
        """
        Execute the specified browser action.
        
        Args:
            action: The action to perform ('visit', 'click', 'input', 'extract', etc.)
            url: URL to navigate to or interact with
            selector: CSS selector for finding elements
            text: Text to input into form fields
            index: Index of element when multiple elements match the selector
            script: JavaScript code to execute
            scroll_amount: Amount to scroll the page (pixels)
            tab_id: ID of the tab to switch to
            timeout: Time to wait for operations to complete
            
        Returns:
            Result of the browser action
        """
        # Check if Selenium is available
        if not SELENIUM_AVAILABLE:
            return {
                "success": False,
                "error": "Selenium is not installed. Please install with: pip install selenium",
                "action": action
            }
        
        # Initialize driver if needed
        if not self._ensure_driver_initialized():
            return {
                "success": False,
                "error": "Failed to initialize web driver",
                "action": action
            }
        
        try:
            # Execute the requested action
            if action == "navigate":
                return self._navigate(url, timeout)
            elif action == "click":
                return self._click(selector, index, timeout)
            elif action == "input_text":
                return self._input_text(selector, text, index, timeout)
            elif action == "get_text":
                return self._get_text(selector, timeout)
            elif action == "get_html":
                return self._get_html()
            elif action == "screenshot":
                return self._take_screenshot()
            elif action == "scroll":
                return self._scroll(scroll_amount)
            elif action == "execute_js":
                return self._execute_js(script)
            elif action == "new_tab":
                return self._new_tab(url, timeout)
            elif action == "switch_tab":
                return self._switch_tab(tab_id)
            elif action == "close_tab":
                return self._close_tab()
            elif action == "refresh":
                return self._refresh()
            else:
                return {
                    "success": False,
                    "error": f"Unknown action: {action}",
                    "action": action
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error during {action}: {str(e)}",
                "action": action
            }
    
    def _navigate(self, url: str, timeout: int) -> Dict[str, Any]:
        """Navigate to a URL."""
        try:
            self._driver.get(url)
            # Wait for page to load
            WebDriverWait(self._driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            return {
                "success": True,
                "action": "navigate",
                "url": url,
                "title": self._driver.title,
                "current_url": self._driver.current_url
            }
        except TimeoutException:
            return {
                "success": False,
                "action": "navigate",
                "error": "Page load timed out",
                "url": url,
                "current_url": self._driver.current_url
            }
    
    def _click(self, selector: str, index: int, timeout: int) -> Dict[str, Any]:
        """Click on an element identified by selector."""
        try:
            # Find elements matching the selector
            elements = WebDriverWait(self._driver, timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )
            
            if not elements:
                return {
                    "success": False,
                    "action": "click",
                    "error": f"No elements found matching selector: {selector}"
                }
            
            # Use index to select the element
            idx = index if index is not None else 0
            if idx < 0 or idx >= len(elements):
                return {
                    "success": False,
                    "action": "click",
                    "error": f"Index {idx} out of range (0-{len(elements)-1})",
                    "element_count": len(elements)
                }
            
            # Scroll element into view and click
            element = elements[idx]
            self._driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Brief pause for scroll to complete
            element.click()
            
            # Wait for page to stabilize after click
            time.sleep(1)
            
            return {
                "success": True,
                "action": "click",
                "selector": selector,
                "index": idx,
                "element_count": len(elements),
                "current_url": self._driver.current_url
            }
        except TimeoutException:
            return {
                "success": False,
                "action": "click",
                "error": f"Timeout waiting for elements matching selector: {selector}"
            }
        except Exception as e:
            return {
                "success": False,
                "action": "click",
                "error": f"Error clicking element: {str(e)}"
            }
    
    def _input_text(self, selector: str, text: str, index: int, timeout: int) -> Dict[str, Any]:
        """Input text into an element identified by selector."""
        try:
            # Find elements matching the selector
            elements = WebDriverWait(self._driver, timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )
            
            if not elements:
                return {
                    "success": False,
                    "action": "input_text",
                    "error": f"No elements found matching selector: {selector}"
                }
            
            # Use index to select the element
            idx = index if index is not None else 0
            if idx < 0 or idx >= len(elements):
                return {
                    "success": False,
                    "action": "input_text",
                    "error": f"Index {idx} out of range (0-{len(elements)-1})",
                    "element_count": len(elements)
                }
            
            # Scroll element into view, focus, clear and input text
            element = elements[idx]
            self._driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Brief pause for scroll to complete
            element.click()
            element.clear()
            element.send_keys(text)
            
            return {
                "success": True,
                "action": "input_text",
                "selector": selector,
                "text": text,
                "index": idx,
                "element_count": len(elements)
            }
        except TimeoutException:
            return {
                "success": False,
                "action": "input_text",
                "error": f"Timeout waiting for elements matching selector: {selector}"
            }
        except Exception as e:
            return {
                "success": False,
                "action": "input_text",
                "error": f"Error inputting text: {str(e)}"
            }
    
    def _get_text(self, selector: Optional[str], timeout: int) -> Dict[str, Any]:
        """Get text content from the page or specific elements."""
        try:
            if selector:
                # Get text from specific elements
                elements = WebDriverWait(self._driver, timeout).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )
                
                if not elements:
                    return {
                        "success": False,
                        "action": "get_text",
                        "error": f"No elements found matching selector: {selector}"
                    }
                
                text_content = [element.text for element in elements]
                
                return {
                    "success": True,
                    "action": "get_text",
                    "selector": selector,
                    "element_count": len(elements),
                    "text": text_content
                }
            else:
                # Get text from whole page
                body_element = self._driver.find_element(By.TAG_NAME, "body")
                text_content = body_element.text
                
                return {
                    "success": True,
                    "action": "get_text",
                    "text": text_content
                }
        except TimeoutException:
            return {
                "success": False,
                "action": "get_text",
                "error": f"Timeout waiting for elements matching selector: {selector}"
            }
        except Exception as e:
            return {
                "success": False,
                "action": "get_text",
                "error": f"Error getting text: {str(e)}"
            }
    
    def _get_html(self) -> Dict[str, Any]:
        """Get the HTML content of the current page."""
        try:
            html_content = self._driver.page_source
            
            return {
                "success": True,
                "action": "get_html",
                "html": html_content
            }
        except Exception as e:
            return {
                "success": False,
                "action": "get_html",
                "error": f"Error getting HTML: {str(e)}"
            }
    
    def _take_screenshot(self) -> Dict[str, Any]:
        """Take a screenshot of the current page."""
        try:
            # Take screenshot as base64
            screenshot = self._driver.get_screenshot_as_base64()
            
            return {
                "success": True,
                "action": "screenshot",
                "screenshot_base64": screenshot,
                "screenshot_data_uri": f"data:image/png;base64,{screenshot}"
            }
        except Exception as e:
            return {
                "success": False,
                "action": "screenshot",
                "error": f"Error taking screenshot: {str(e)}"
            }
    
    def _scroll(self, scroll_amount: int) -> Dict[str, Any]:
        """Scroll the page by a specified amount of pixels."""
        try:
            # Execute JavaScript to scroll
            self._driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            return {
                "success": True,
                "action": "scroll",
                "scroll_amount": scroll_amount
            }
        except Exception as e:
            return {
                "success": False,
                "action": "scroll",
                "error": f"Error scrolling page: {str(e)}"
            }
    
    def _execute_js(self, script: str) -> Dict[str, Any]:
        """Execute JavaScript on the current page."""
        try:
            result = self._driver.execute_script(script)
            
            return {
                "success": True,
                "action": "execute_js",
                "result": str(result) if result is not None else None
            }
        except Exception as e:
            return {
                "success": False,
                "action": "execute_js",
                "error": f"Error executing JavaScript: {str(e)}"
            }
    
    def _new_tab(self, url: str, timeout: int) -> Dict[str, Any]:
        """Open a new tab and navigate to the specified URL."""
        try:
            # Open new tab
            self._driver.switch_to.new_window('tab')
            
            # Get the current window handle
            new_tab = self._driver.current_window_handle
            
            # Generate new tab ID
            new_tab_id = max(self._tabs.keys()) + 1 if self._tabs else 0
            
            # Store tab info
            self._tabs[new_tab_id] = new_tab
            self._current_tab_id = new_tab_id
            
            # Navigate to URL
            result = self._navigate(url, timeout)
            result["tab_id"] = new_tab_id
            
            return result
        except Exception as e:
            return {
                "success": False,
                "action": "new_tab",
                "error": f"Error opening new tab: {str(e)}"
            }
    
    def _switch_tab(self, tab_id: int) -> Dict[str, Any]:
        """Switch to a tab by its ID."""
        try:
            if tab_id not in self._tabs:
                return {
                    "success": False,
                    "action": "switch_tab",
                    "error": f"Tab ID {tab_id} not found",
                    "available_tabs": list(self._tabs.keys())
                }
            
            # Switch to the specified tab
            self._driver.switch_to.window(self._tabs[tab_id])
            self._current_tab_id = tab_id
            
            return {
                "success": True,
                "action": "switch_tab",
                "tab_id": tab_id,
                "title": self._driver.title,
                "current_url": self._driver.current_url
            }
        except Exception as e:
            return {
                "success": False,
                "action": "switch_tab",
                "error": f"Error switching to tab: {str(e)}"
            }
    
    def _close_tab(self) -> Dict[str, Any]:
        """Close the current tab."""
        try:
            # Get current tab ID
            tab_id = self._current_tab_id
            
            # Close current tab
            self._driver.close()
            
            # Remove from tab tracking
            if tab_id in self._tabs:
                del self._tabs[tab_id]
            
            # Switch to first available tab if any
            if self._tabs:
                next_tab_id = next(iter(self._tabs.keys()))
                self._driver.switch_to.window(self._tabs[next_tab_id])
                self._current_tab_id = next_tab_id
                
                return {
                    "success": True,
                    "action": "close_tab",
                    "closed_tab_id": tab_id,
                    "current_tab_id": next_tab_id,
                    "title": self._driver.title,
                    "current_url": self._driver.current_url
                }
            else:
                # No tabs left
                self._current_tab_id = None
                
                return {
                    "success": True,
                    "action": "close_tab",
                    "closed_tab_id": tab_id,
                    "message": "All tabs closed"
                }
                
        except Exception as e:
            return {
                "success": False,
                "action": "close_tab",
                "error": f"Error closing tab: {str(e)}"
            }
    
    def _refresh(self) -> Dict[str, Any]:
        """Refresh the current page."""
        try:
            self._driver.refresh()
            
            # Wait for page to load
            WebDriverWait(self._driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            return {
                "success": True,
                "action": "refresh",
                "title": self._driver.title,
                "current_url": self._driver.current_url
            }
        except Exception as e:
            return {
                "success": False,
                "action": "refresh",
                "error": f"Error refreshing page: {str(e)}"
            }
    
    def __del__(self):
        """Clean up resources when the tool is destroyed."""
        if self._driver is not None:
            try:
                self._driver.quit()
            except:
                pass 