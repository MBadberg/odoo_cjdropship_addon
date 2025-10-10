import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CJDropshippingAPI:
    # ... other methods ...

    def _authenticate(self, url, payload):
        logger.debug(f"Request URL: {url}")
        logger.debug(f"Request Payload: {payload}")
        response = requests.post(url, json=payload)
        logger.debug(f"Response Status: {response.status_code}")
        logger.debug(f"Response Headers: {response.headers}")
        logger.debug(f"Response Text: {response.text}")
        # ... existing authentication logic ...
