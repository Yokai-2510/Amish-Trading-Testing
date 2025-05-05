# --- START OF FILE brokers_api/login.py ---

from playwright.sync_api import sync_playwright, expect, TimeoutError
from urllib.parse import parse_qs, urlparse, quote
import pyotp
import requests
import json
import time
from rejson import Client, Path # Import Client for standalone testing block

# NOTE: Removed internal get_redis() function

def fetch_access_token(client):

    if not client:
        raise ValueError("A valid Redis client instance must be provided.")

    print("\n--- Fetching Access Token ---")

    # Fetch credentials from the NEW Redis path
    credentials_path = ".global_config.credentials"
    try:
        print(f"  Fetching credentials from Redis path: '{credentials_path}'")
        credentials = client.jsonget("trading_setup", Path(credentials_path))
        if not credentials:
            raise Exception(f"No credentials found in Redis under {credentials_path}")
        print("  Credentials retrieved.")
    except Exception as e:
         raise Exception(f"Error fetching credentials from Redis: {e}")

    # Extract necessary details
    API_KEY = credentials.get("API_KEY")
    SECRET_KEY = credentials.get("SECRET_KEY")
    RURL = credentials.get("RURL")
    TOTP_KEY = credentials.get("TOTP_KEY")
    MOBILE_NO = credentials.get("MOBILE_NO")
    PIN = credentials.get("PIN")

    if not all([API_KEY, SECRET_KEY, RURL, TOTP_KEY, MOBILE_NO, PIN]):
        missing = [k for k, v in {"API_KEY": API_KEY, "SECRET_KEY": SECRET_KEY, "RURL": RURL, "TOTP_KEY": TOTP_KEY, "MOBILE_NO": MOBILE_NO, "PIN": PIN}.items() if not v]
        raise Exception(f"Missing required credentials in Redis: {', '.join(missing)}")

    rurlEncode = quote(RURL, safe="")
    auth_code = None
    AUTH_URL = f'https://api-v2.upstox.com/login/authorization/dialog?response_type=code&client_id={API_KEY}&redirect_uri={rurlEncode}'

    print("  Launching browser automation for auth code...")
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True, # Keep headless for server environments
                args=['--disable-web-security', '--disable-features=IsolateOrigins,site-per-process', '--no-sandbox'] # Added --no-sandbox often needed in containers/linux
            )
            context = browser.new_context(ignore_https_errors=True, bypass_csp=True)
            page = context.new_page()

            try:
                print("    Navigating to Upstox login...")

                # Define request handler within the scope where auth_code is defined
                def handle_request(request):
                    nonlocal auth_code
                    if auth_code is None and RURL in request.url and 'code=' in request.url:
                        try:
                            auth_code = parse_qs(urlparse(request.url).query)['code'][0]
                            print(f"    Successfully captured authorization code.")
                        except (KeyError, IndexError):
                            print("    Warning: Found redirect URL but couldn't parse code.")

                page.on('request', handle_request)
                page.goto(AUTH_URL, wait_until='load', timeout=60000) # Increased timeout, wait_until='load' might be more reliable

                print("    Filling mobile number...")
                page.locator("#mobileNum").fill(MOBILE_NO)
                page.get_by_role("button", name="Get OTP").click()

                print("    Waiting for OTP field...")
                page.wait_for_selector("#otpNum", state="visible", timeout=30000)

                print("    Generating and filling OTP...")
                otp = pyotp.TOTP(TOTP_KEY).now()
                page.locator("#otpNum").fill(otp)
                page.get_by_role("button", name="Continue").click()

                print("    Waiting for PIN field...")
                page.wait_for_selector("input[type='password']", state="visible", timeout=30000)

                print("    Filling PIN...")
                page.get_by_label("Enter 6-digit PIN").fill(PIN)

                print("    Clicking Continue (expecting navigation or timeout)...")
                # Don't necessarily expect navigation. The code might be captured via the request handler before full navigation.
                try:
                    # Click continue, but don't wait indefinitely for navigation if code is already captured
                    page.get_by_role("button", name="Continue").click()
                    # Wait a short fixed time or for a specific element if navigation DOES occur
                    page.wait_for_timeout(5000) # Wait 5s to allow requests/redirects
                except Exception as click_err:
                    # Ignore errors here if code capture is the main goal
                    print(f"    Note: Error during final 'Continue' click (may be expected): {click_err}")

                # Final check after waiting
                if auth_code is None:
                    print("    Warning: Auth code not captured after interaction. Checking page URL again.")
                    current_url = page.url
                    if RURL in current_url and 'code=' in current_url:
                         try:
                             auth_code = parse_qs(urlparse(current_url).query)['code'][0]
                             print(f"    Successfully captured authorization code from final URL.")
                         except (KeyError, IndexError):
                             print("    Warning: Final URL check couldn't parse code.")

            except Exception as e:
                print(f"    Browser automation error: {str(e)}")
                # Capture screenshot for debugging if possible/needed
                # page.screenshot(path="playwright_error.png")
                raise # Re-raise the exception
            finally:
                print("    Closing browser context...")
                context.close()
                browser.close()
                print("    Browser closed.")

    except Exception as general_e:
         # Catch errors from Playwright startup/teardown too
         print(f"  Playwright setup/teardown error: {general_e}")
         raise # Re-raise

    if not auth_code:
        raise Exception("Failed to obtain authorization code after browser automation.")

    print(f"  Proceeding with authorization code to fetch access token...")

    token_url = 'https://api-v2.upstox.com/login/authorization/token'
    headers = {
        'accept': 'application/json',
        'Api-Version': '2.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'code': auth_code,
        'client_id': API_KEY,
        'client_secret': SECRET_KEY,
        'redirect_uri': RURL,
        'grant_type': 'authorization_code'
    }

    try:
        response = requests.post(token_url, headers=headers, data=data, timeout=30)
        response.raise_for_status() # Check for HTTP errors
        response_json = response.json()
        access_token = response_json.get('access_token')

        if not access_token:
            print("  Token exchange response content:", response.text)
            raise Exception("No access token found in the token exchange response.")

        # Update only the access token in the CORRECT nested structure using the passed client
        token_redis_path = ".global_config.credentials.access_token"
        client.jsonset("trading_setup", Path(token_redis_path), access_token)

        print(f"  Access token successfully updated in Redis at '{token_redis_path}'.")
        print("--- Access Token Fetch Complete ---")
        time.sleep(1)
        return access_token

    except requests.exceptions.RequestException as e:
        status_code = e.response.status_code if hasattr(e, 'response') and e.response is not None else 'N/A'
        response_text = e.response.text if hasattr(e, 'response') and e.response is not None else 'N/A'
        print(f"  Error during token exchange. Status code: {status_code}")
        print(f"  Response content: {response_text}")
        raise Exception(f"Failed to exchange authorization code for access token: {str(e)}")
    except Exception as e:
        print(f"  Unexpected error during token processing or Redis update: {e}")
        raise


# --- Standalone Execution (for testing this module directly) ---
if __name__ == "__main__":
    print("Running login.py directly for testing...")
    # Requires Redis to be running and setup via redis_setup.py
    test_client = None
    try:
        # Create a client instance specifically for this test run
        TEST_REDIS_HOST = "localhost"
        TEST_REDIS_PORT = 6379
        TEST_REDIS_DB = 0
        TEST_REDIS_PASSWORD = None
        print("  Connecting to Redis for test...")
        test_client = Client(host=TEST_REDIS_HOST, port=TEST_REDIS_PORT, db=TEST_REDIS_DB, password=TEST_REDIS_PASSWORD, decode_responses=True)
        test_client.ping()
        print("  Test Redis connection successful.")

        # Call the main function with the test client
        access_token = fetch_access_token(test_client)
        print("\nStandalone login test successful!")
        # print(f"Retrieved Token: {access_token[:5]}...{access_token[-5:]}") # Avoid printing full token

    except Exception as e:
        print(f"\nError during standalone login test: {str(e)}")
        import traceback
        traceback.print_exc() # Print full traceback for debugging
    finally:
        print("Standalone execution finished.")


# --- END OF FILE brokers_api/login.py ---