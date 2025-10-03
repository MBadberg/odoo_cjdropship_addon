# CJDropshipping Odoo Addon - Development Guide

## Architecture Overview

### Module Structure

The addon follows the standard Odoo module structure:

```
cjdropship/
├── __init__.py                    # Module initialization
├── __manifest__.py                # Module metadata and dependencies
├── models/                        # Business logic
│   ├── cjdropship_api.py         # API client wrapper
│   ├── cjdropship_config.py      # Configuration management
│   ├── cjdropship_product.py     # Product synchronization
│   ├── cjdropship_order.py       # Order management
│   ├── cjdropship_webhook.py     # Webhook processing
│   ├── sale_order.py             # Sale order extensions
│   └── product_template.py       # Product extensions
├── controllers/                   # HTTP endpoints
│   └── webhook_controller.py     # Webhook receiver
├── wizards/                       # User interaction wizards
│   └── product_import_wizard.py  # Product import wizard
├── views/                         # UI definitions
├── security/                      # Access rights
└── data/                         # Default data
```

## Core Components

### 1. API Client (`cjdropship_api.py`)

The API client handles all communication with CJDropshipping API:

**Key Methods:**
- `_authenticate()`: Obtains access token
- `_make_request()`: Generic API request handler
- `get_product_list()`: Retrieves product catalog
- `create_order()`: Creates orders in CJDropshipping
- `query_logistics()`: Gets tracking information

**Authentication:**
- Token-based authentication
- Automatic token refresh
- 2-hour token validity

### 2. Configuration Model (`cjdropship_config.py`)

Central configuration for the addon:

**Features:**
- API credential storage
- Sync settings
- Price markup configuration
- Webhook URL generation
- Connection testing

**Key Methods:**
- `get_api_client()`: Returns authenticated API client
- `action_test_connection()`: Tests API connectivity
- `calculate_sale_price()`: Applies markup to CJ prices

### 3. Product Model (`cjdropship_product.py`)

Manages CJDropshipping products:

**Fields:**
- CJ-specific: product_id, variant_id, SKU
- Pricing: cj_price, selling_price
- Inventory: cj_stock_qty
- Shipping: weight, dimensions

**Key Methods:**
- `action_create_odoo_product()`: Creates/updates Odoo products
- `action_sync_from_cj()`: Syncs data from CJDropshipping
- `action_bulk_create_products()`: Batch product creation

### 4. Order Model (`cjdropship_order.py`)

Handles order fulfillment:

**States:**
- draft: Initial state
- submitted: Sent to CJDropshipping
- processing: Being processed
- shipped: Shipped with tracking
- delivered: Completed
- cancelled: Cancelled
- error: Submission failed

**Key Methods:**
- `action_submit_to_cj()`: Submits order to CJDropshipping
- `action_update_status()`: Updates order status
- `action_query_logistics()`: Gets tracking info
- `_prepare_cj_order_data()`: Prepares order data for API

### 5. Webhook Model (`cjdropship_webhook.py`)

Processes webhook notifications:

**Types:**
- order_status: Order status updates
- tracking: Tracking number updates
- inventory: Stock level updates

**Processing:**
- Automatic webhook processing
- Error logging
- Status synchronization

## API Integration

### CJDropshipping API Endpoints Used

**Base URL:** `https://developers.cjdropshipping.com/api2.0/v1`

**Endpoints:**
1. `/authentication/getAccessToken` - Authentication
2. `/product/list` - Product catalog
3. `/product/query` - Product details
4. `/product/inventory/query` - Stock levels
5. `/shopping/order/createOrder` - Order creation
6. `/shopping/order/query` - Order details
7. `/logistic/trackQuery` - Tracking info

### Request Flow

```
1. User Action
   ↓
2. Odoo Model Method
   ↓
3. API Client (_make_request)
   ↓
4. Authentication Check
   ↓
5. HTTP Request to CJDropshipping
   ↓
6. Response Processing
   ↓
7. Update Odoo Records
   ↓
8. User Notification
```

## Webhook Implementation

### Endpoint

**URL Pattern:** `/cjdropship/webhook/{config_id}`
**Method:** POST
**Authentication:** Public (no auth required)
**Content-Type:** application/json

### Webhook Payload Structure

```json
{
  "event": "order.status.updated",
  "orderId": "CJ123456",
  "status": "SHIPPED",
  "trackingNumber": "TRACK123",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Processing Flow

```
1. Webhook Received
   ↓
2. Create Webhook Record
   ↓
3. Determine Webhook Type
   ↓
4. Process Based on Type
   ↓
5. Update Related Records
   ↓
6. Mark as Processed
```

## Database Schema

### Main Models

**cjdropship.config**
- Stores API credentials
- Configuration settings
- One active config per company

**cjdropship.product**
- Links CJ products to Odoo products
- Stores pricing and inventory
- Unique constraint on (cj_product_id, cj_variant_id)

**cjdropship.order**
- Links sale orders to CJ orders
- Tracks fulfillment status
- Stores API communication logs

**cjdropship.webhook**
- Logs all webhook events
- Processing status
- Error tracking

### Relationships

```
sale.order (1) ←→ (1) cjdropship.order
product.template (1) ←→ (0..1) cjdropship.product
cjdropship.order (0..1) ←→ (N) cjdropship.webhook
```

## Extending the Addon

### Adding New API Endpoints

1. Add method to `CJDropshippingAPI` class:

```python
def get_new_endpoint(self, params):
    return self._make_request('GET', '/new/endpoint', params=params)
```

2. Use in model:

```python
api = self.config_id.get_api_client()
result = api.get_new_endpoint({'param': 'value'})
```

### Adding New Webhook Types

1. Add to webhook_type selection:

```python
webhook_type = fields.Selection([
    # ... existing types
    ('new_type', 'New Type'),
])
```

2. Implement processing method:

```python
def _process_new_type(self, payload):
    # Process webhook data
    pass
```

3. Update webhook controller to handle new type

### Adding Custom Fields

1. Inherit model:

```python
class CJDropshippingProductExtended(models.Model):
    _inherit = 'cjdropship.product'
    
    custom_field = fields.Char('Custom Field')
```

2. Update views to include new field

## Testing

### Manual Testing Steps

1. **Configuration Test:**
   - Set up API credentials
   - Click "Test Connection"
   - Verify success notification

2. **Product Import Test:**
   - Click "Import Products"
   - Configure wizard
   - Verify products imported
   - Create Odoo products

3. **Order Fulfillment Test:**
   - Create sale order with CJ products
   - Confirm order
   - Submit to CJDropshipping
   - Verify CJ order created

4. **Webhook Test:**
   - Configure webhook URL in CJ dashboard
   - Trigger event (order status change)
   - Verify webhook received and processed

### Unit Testing (Future)

Structure for unit tests:

```python
from odoo.tests import TransactionCase

class TestCJDropshipping(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.config = self.env['cjdropship.config'].create({
            'name': 'Test Config',
            'api_email': 'test@example.com',
            'api_password': 'password'
        })
    
    def test_price_calculation(self):
        price = self.config.calculate_sale_price(100)
        self.assertEqual(price, 130)  # 30% markup
```

## Security Considerations

### Access Rights

- **Users:** Read/write products and orders
- **Managers:** Full access including configuration

### API Security

- Credentials stored in database
- Password field hidden in UI
- Token automatically refreshed
- HTTPS required for production

### Webhook Security

- Public endpoint (required by CJ)
- Validate config_id exists
- Check webhook_enabled flag
- Log all webhook events
- Consider adding signature verification (future)

## Performance Optimization

### Best Practices

1. **Batch Operations:**
   - Use `action_bulk_create_products()` for multiple products
   - Process webhooks in cron jobs for high volume

2. **Caching:**
   - API tokens cached for 2 hours
   - Product data cached until sync

3. **Async Processing:**
   - Consider queue_job module for long operations
   - Webhook processing can be deferred

4. **Database Indexes:**
   - All foreign keys indexed
   - cj_product_id indexed for lookups

## Troubleshooting

### Common Issues

**Issue: Connection Failed**
- Check API credentials
- Verify network connectivity
- Check firewall rules

**Issue: Product Import Fails**
- Check API limits
- Verify response format
- Check Odoo logs

**Issue: Webhooks Not Received**
- Verify URL accessibility
- Check webhook_enabled flag
- Test with curl/Postman

### Logging

Enable debug logging:

```python
import logging
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
```

Check logs:
```bash
tail -f /var/log/odoo/odoo.log | grep cjdropship
```

## Deployment

### Production Checklist

- [ ] Set proper API credentials
- [ ] Configure HTTPS
- [ ] Set up webhook URL in CJ dashboard
- [ ] Configure backup strategy
- [ ] Set up monitoring
- [ ] Test order flow end-to-end
- [ ] Configure cron jobs if needed
- [ ] Review security settings
- [ ] Document custom configurations

### Maintenance

**Daily:**
- Monitor webhook logs
- Check failed orders

**Weekly:**
- Review error logs
- Sync product inventory

**Monthly:**
- Update module if needed
- Review API usage
- Clean old webhook logs

## Contributing

### Code Style

- Follow Odoo coding guidelines
- Use meaningful variable names
- Add docstrings to all methods
- Comment complex logic

### Pull Request Process

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit PR with description

## Resources

- [Odoo Documentation](https://www.odoo.com/documentation/19.0/)
- [CJDropshipping API Docs](https://developers.cjdropshipping.com/en/api/introduction.html)
- [Python Requests](https://docs.python-requests.org/)

## Support

For issues and questions:
- GitHub Issues: https://github.com/MBadberg/odoo_cjdropship_addon/issues
- Odoo Community: https://www.odoo.com/forum
