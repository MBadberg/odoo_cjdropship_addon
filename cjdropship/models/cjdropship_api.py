# -*- coding: utf-8 -*-
"""CJDropshipping API Client."""

import logging
import time

import requests

_logger = logging.getLogger(__name__)


class CJDropshippingAPI:
    """CJDropshipping API Client for handling API requests."""

    def __init__(self, email, password):
        self.base_url = "https://developers.cjdropshipping.com/api2.0/v1"
        self.email = email
        self.password = password
        self.access_token = None
        self.token_expiry = 0

    def _get_headers(self):
        """Get headers with authentication token"""
        if not self.access_token or time.time() >= self.token_expiry:
            self._authenticate()

        return {
            'Content-Type': 'application/json',
            'CJ-Access-Token': self.access_token
        }

    def _authenticate(self):
        """Authenticate with CJDropshipping API"""
        url = f"{self.base_url}/authentication"

        payload = {
            'email': self.email,
            'password': self.password
        }

        try:
            # Debug logging for troubleshooting
            _logger.info(f"CJ API Debug - Request URL: {url}")
            _logger.info(f"CJ API Debug - Request Payload: {payload}")
            _logger.info(f"CJ API Debug - Base URL: {self.base_url}")
            
            response = requests.post(url, json=payload, timeout=30)
            
            # Log detailed response information
            _logger.info(f"CJ API Debug - Response Status Code: {response.status_code}")
            _logger.info(f"CJ API Debug - Response Headers: {dict(response.headers)}")
            _logger.info(f"CJ API Debug - Response Content-Type: {response.headers.get('content-type', 'N/A')}")
            _logger.info(f"CJ API Debug - Response Text: {response.text}")
            _logger.info(f"CJ API Debug - Response URL: {response.url}")
            
            # Try to parse JSON response
            try:
                response_json = response.json()
                _logger.info(f"CJ API Debug - Response JSON: {response_json}")
            except Exception as json_error:
                _logger.error(f"CJ API Debug - Failed to parse JSON: {json_error}")
            
            response.raise_for_status()

            data = response.json()
            if data.get('code') == 200 and data.get('result'):
                self.access_token = data['data']['accessToken']
                # Token typically valid for 2 hours
                self.token_expiry = time.time() + 7000
                _logger.info(
                    "Successfully authenticated with CJDropshipping API"
                )
            else:
                error_msg = data.get('message', 'Unknown error')
                _logger.error(f"CJ API Debug - Authentication failed - Response Code: {data.get('code')}, Message: {error_msg}, Full Response: {data}")
                raise ValueError(
                    f"Authentication failed: {error_msg}"
                )

        except requests.exceptions.RequestException as e:
            _logger.error(
                "CJDropshipping API authentication error: %s", str(e)
            )
            _logger.error(f"CJ API Debug - Exception type: {type(e).__name__}")
            _logger.error(f"CJ API Debug - Exception details: {str(e)}")
            raise

    def _make_request(self, method, endpoint, data=None, params=None):
        """Make API request with error handling"""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        try:
            if method == 'GET':
                response = requests.get(
                    url, headers=headers, params=params, timeout=30
                )
            elif method == 'POST':
                response = requests.post(
                    url, headers=headers, json=data, timeout=30
                )
            elif method == 'PUT':
                response = requests.put(
                    url, headers=headers, json=data, timeout=30
                )
            else:
                raise ValueError(
                    f"Unsupported HTTP method: {method}"
                )

            response.raise_for_status()
            result = response.json()

            if result.get('code') != 200:
                error_msg = result.get('message', 'Unknown error')
                raise ValueError(f"API Error: {error_msg}")

            return result.get('data', {})

        except requests.exceptions.RequestException as e:
            _logger.error(
                "CJDropshipping API request error: %s", str(e)
            )
            raise

    # Product Methods
    def get_product_list(self, page=1, page_size=20, category_id=None):
        """Get list of products from CJDropshipping"""
        params = {
            'pageNum': page,
            'pageSize': page_size
        }
        if category_id:
            params['categoryId'] = category_id

        return self._make_request('GET', '/product/list', params=params)

    def get_product_detail(self, product_id):
        """Get detailed product information"""
        params = {'pid': product_id}
        return self._make_request('GET', '/product/query', params=params)

    def get_product_variant(self, product_id):
        """Get product variants"""
        params = {'pid': product_id}
        return self._make_request('GET', '/product/variant/query', params=params)

    def get_product_inventory(self, product_id, variant_id=None):
        """Get product inventory/stock"""
        params = {'pid': product_id}
        if variant_id:
            params['vid'] = variant_id

        return self._make_request('GET', '/product/inventory/query', params=params)

    # Order Methods
    def create_order(self, order_data):
        """Create order in CJDropshipping"""
        return self._make_request('POST', '/shopping/order/createOrder', data=order_data)

    def get_order_detail(self, order_id):
        """Get order details"""
        params = {'orderId': order_id}
        return self._make_request('GET', '/shopping/order/query', params=params)

    def get_order_list(self, page=1, page_size=20):
        """Get list of orders"""
        params = {
            'pageNum': page,
            'pageSize': page_size
        }
        return self._make_request('GET', '/shopping/order/list', params=params)

    # Logistics Methods
    def get_shipping_methods(self, product_list, country_code):
        """Get available shipping methods"""
        data = {
            'products': product_list,
            'countryCode': country_code
        }
        return self._make_request('POST', '/logistic/freightCalculate', data=data)

    def query_logistics(self, order_id):
        """Query logistics/tracking information"""
        params = {'orderId': order_id}
        return self._make_request('GET', '/logistic/trackQuery', params=params)

    # Category Methods
    def get_categories(self):
        """Get product categories"""
        return self._make_request('GET', '/product/categoryList')
