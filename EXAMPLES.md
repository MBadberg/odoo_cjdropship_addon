# CJDropshipping Odoo Addon - Examples

This document provides practical examples for using the CJDropshipping Odoo addon.

## Configuration Examples

### Basic Configuration

Minimum configuration to get started:

```
Navigation: CJDropshipping > Configuration > Settings

Fields:
- Configuration Name: "CJDropshipping Production"
- API Email: your-email@example.com
- API Password: your-password
- Default Product Type: Consumable
- Price Markup Type: Percentage
- Price Markup: 30.0
- Auto Fulfill Orders: Yes
```

### Advanced Configuration

Full configuration with auto-sync:

```
Navigation: CJDropshipping > Configuration > Settings

Basic Settings:
- Configuration Name: "CJ Production"
- API Email: your-email@example.com
- API Password: your-password
- Active: Yes

Product Settings:
- Auto Sync Products: Yes
- Sync Interval: 12 (hours)
- Default Product Type: Consumable
- Default Category: Dropshipping Products
- Price Markup Type: Percentage
- Price Markup: 35.0

Order Settings:
- Auto Fulfill Orders: Yes

Webhook Settings:
- Enable Webhooks: Yes
- Webhook URL: https://your-odoo.com/cjdropship/webhook/1
```

## Product Import Examples

### Example 1: Import First 20 Products

```
Navigation: CJDropshipping > Configuration > Settings > Import Products

Settings:
- Configuration: CJDropshipping Production
- Category Filter: (leave empty for all)
- Page Number: 1
- Products per Page: 20
- Create Odoo Products Immediately: Yes

Click: Import Products
```

### Example 2: Import Specific Category

```
Navigation: CJDropshipping > Configuration > Settings > Import Products

Settings:
- Configuration: CJDropshipping Production
- Category Filter: Electronics
- Page Number: 1
- Products per Page: 50
- Create Odoo Products Immediately: No

Click: Import Products

Then manually review and create products:
Navigation: CJDropshipping > Products > CJ Products
Select products > Action > Create Odoo Products
```

### Example 3: Bulk Import Multiple Pages

```python
# Using Odoo shell for bulk import
# Access: ./odoo-bin shell -c odoo.conf

config = env['cjdropship.config'].search([('name', '=', 'CJDropshipping Production')], limit=1)

for page in range(1, 6):  # Import pages 1-5
    wizard = env['cjdropship.product.import.wizard'].create({
        'config_id': config.id,
        'page_number': page,
        'page_size': 50,
        'create_odoo_products': True
    })
    wizard.action_import_products()
    print(f"Page {page}: {wizard.imported_count} products imported")
```

## Order Processing Examples

### Example 1: Manual Order Submission

```
Step 1: Create Sale Order
Navigation: Sales > Orders > Orders > Create

- Customer: John Doe
- Add products (CJDropshipping products)
- Confirm Sale

Step 2: Submit to CJDropshipping
On Sale Order form:
Click: Submit to CJDropshipping

Step 3: View CJ Order
Click: CJ Order button in button box
Or: CJDropshipping > Orders > CJ Orders
```

### Example 2: Automatic Order Fulfillment

```
Prerequisites:
- Configure Auto Fulfill Orders = Yes

Process:
1. Create Sale Order with CJ products
2. Confirm Sale Order
3. Order automatically submitted to CJDropshipping
4. Check CJ Order status: Sales > Orders > [Order] > CJ Order button
```

### Example 3: Track Order Status

```
Navigation: CJDropshipping > Orders > CJ Orders > [Select Order]

Actions:
1. Update Status: Fetches latest status from CJDropshipping
2. Query Logistics: Gets tracking information
3. View in Sale Order: Opens related sale order

Status Flow:
Draft → Submitted → Processing → Shipped → Delivered
```

## Webhook Examples

### Example 1: Configure Webhook in CJDropshipping

```
1. Get Webhook URL from Odoo:
   CJDropshipping > Configuration > Settings
   Copy: Webhook URL (e.g., https://your-odoo.com/cjdropship/webhook/1)

2. Configure in CJDropshipping Dashboard:
   - Login to CJDropshipping
   - Go to API Settings
   - Add Webhook URL
   - Select events: Order Status, Tracking Updates
   - Save

3. Test Webhook:
   - Trigger an event in CJDropshipping
   - Check: CJDropshipping > Webhooks
   - Verify webhook received and processed
```

### Example 2: Manual Webhook Testing

```bash
# Test webhook endpoint with curl
curl -X POST https://your-odoo.com/cjdropship/webhook/1 \
  -H "Content-Type: application/json" \
  -d '{
    "event": "order.status.updated",
    "orderId": "CJ123456",
    "status": "SHIPPED",
    "trackingNumber": "TRACK123456",
    "timestamp": "2024-01-01T12:00:00Z"
  }'

# Check webhook log in Odoo
Navigation: CJDropshipping > Webhooks
Find: Recent webhook with orderId CJ123456
Verify: Processed = Yes
```

### Example 3: Webhook Processing

```
Automatic Processing:
- Webhooks are automatically processed when received
- Check processing status: CJDropshipping > Webhooks

Manual Processing:
Navigation: CJDropshipping > Webhooks > [Select Webhook]
Click: Process Webhook (if not already processed)
```

## Product Management Examples

### Example 1: Sync Product Prices

```
Update prices for all products:

Method 1: Individual Sync
Navigation: CJDropshipping > Products > CJ Products
Select products
Action: Sync from CJ

Method 2: Automated Sync
Configure in Settings:
- Auto Sync Products: Yes
- Sync Interval: 24 hours

Products will sync automatically
```

### Example 2: Update Product Pricing

```
Change markup for all products:

Step 1: Update Configuration
Navigation: CJDropshipping > Configuration > Settings
Change: Price Markup from 30% to 35%
Save

Step 2: Recalculate Prices
Navigation: CJDropshipping > Products > CJ Products
Select all products
Action: Sync from CJ (recalculates with new markup)
```

### Example 3: Link CJ Product to Existing Odoo Product

```python
# Using Odoo shell
# This is useful if you already have products in Odoo

cj_product = env['cjdropship.product'].search([('cj_product_id', '=', 'CJ123456')], limit=1)
odoo_product = env['product.template'].search([('default_code', '=', 'SKU123')], limit=1)

# Link products
odoo_product.write({
    'cjdropship_product_id': cj_product.id,
    'is_cjdropship': True
})

# Update from CJ data
odoo_product.write({
    'list_price': cj_product.selling_price,
    'standard_price': cj_product.cj_price
})
```

## API Usage Examples

### Example 1: Get Product Details

```python
# Using Odoo shell

# Get configuration
config = env['cjdropship.config'].get_default_config()

# Get API client
api = config.get_api_client()

# Get product details
product_data = api.get_product_detail('CJ123456')
print(product_data)
```

### Example 2: Query Order Status

```python
# Using Odoo shell

config = env['cjdropship.config'].get_default_config()
api = config.get_api_client()

# Get order details
order_data = api.get_order_detail('CJ-ORDER-123456')
print(f"Status: {order_data.get('status')}")
print(f"Tracking: {order_data.get('trackingNumber')}")
```

### Example 3: Get Shipping Methods

```python
# Using Odoo shell

config = env['cjdropship.config'].get_default_config()
api = config.get_api_client()

# Prepare product list
products = [
    {'productId': 'CJ123456', 'quantity': 2},
    {'productId': 'CJ789012', 'quantity': 1}
]

# Get shipping methods
shipping = api.get_shipping_methods(products, 'US')
for method in shipping:
    print(f"{method['name']}: ${method['cost']}")
```

## Automation Examples

### Example 1: Scheduled Product Sync

```python
# Create scheduled action
# Settings > Technical > Automation > Scheduled Actions

Name: CJDropshipping Product Sync
Model: cjdropship.product
Execute Every: 1 Days
Number of Calls: -1 (unlimited)

Python Code:
```python
# Sync all active CJ products
products = env['cjdropship.product'].search([('active', '=', True)])
for product in products:
    try:
        product.action_sync_from_cj()
    except Exception as e:
        _logger.error(f"Failed to sync product {product.cj_product_id}: {e}")
```

### Example 2: Auto-Update Order Status

```python
# Create scheduled action

Name: Update CJDropshipping Order Status
Model: cjdropship.order
Execute Every: 4 Hours
Number of Calls: -1

Python Code:
```python
# Update orders that are in progress
orders = env['cjdropship.order'].search([
    ('state', 'in', ['submitted', 'processing', 'shipped'])
])
for order in orders:
    try:
        order.action_update_status()
    except Exception as e:
        _logger.error(f"Failed to update order {order.cj_order_id}: {e}")
```

### Example 3: Inventory Alerts

```python
# Create scheduled action

Name: CJDropshipping Low Stock Alert
Model: cjdropship.product
Execute Every: 12 Hours
Number of Calls: -1

Python Code:
```python
# Alert on low stock products
low_stock = env['cjdropship.product'].search([
    ('cj_stock_qty', '<', 10),
    ('product_tmpl_id', '!=', False),
    ('active', '=', True)
])

if low_stock:
    # Send email to procurement team
    template = env.ref('cjdropship.email_template_low_stock_alert')
    for product in low_stock:
        template.send_mail(product.id, force_send=True)
```

## Troubleshooting Examples

### Example 1: Debug Connection Issues

```python
# Using Odoo shell

config = env['cjdropship.config'].get_default_config()

# Test authentication
try:
    api = config.get_api_client()
    categories = api.get_categories()
    print("✓ Connection successful")
    print(f"Categories: {len(categories)}")
except Exception as e:
    print(f"✗ Connection failed: {e}")
```

### Example 2: Retry Failed Orders

```python
# Using Odoo shell

# Find failed orders
failed_orders = env['cjdropship.order'].search([('state', '=', 'error')])

print(f"Found {len(failed_orders)} failed orders")

# Retry submission
for order in failed_orders:
    print(f"Retrying order {order.sale_order_id.name}")
    try:
        order.write({'state': 'draft'})
        order.action_submit_to_cj()
        print(f"  ✓ Success")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
```

### Example 3: Clean Old Webhooks

```python
# Using Odoo shell

from datetime import datetime, timedelta

# Delete webhooks older than 30 days
cutoff_date = datetime.now() - timedelta(days=30)
old_webhooks = env['cjdropship.webhook'].search([
    ('create_date', '<', cutoff_date),
    ('processed', '=', True)
])

print(f"Deleting {len(old_webhooks)} old webhooks")
old_webhooks.unlink()
```

## Best Practices

### Product Management

1. **Import Strategy**: Start with small batches (20-50 products) to test
2. **Review Before Creating**: Import without auto-create, review, then create selectively
3. **Regular Sync**: Set up automatic sync for price and inventory updates
4. **Categorization**: Use Odoo categories to organize products

### Order Processing

1. **Test Mode**: Test with small orders first
2. **Monitor Status**: Regularly check order status updates
3. **Customer Communication**: Use sale order notes for special instructions
4. **Tracking**: Always query logistics for shipped orders

### Webhook Configuration

1. **Verify URL**: Ensure webhook URL is accessible from internet
2. **Monitor Logs**: Regularly check webhook logs
3. **Error Handling**: Review and resolve failed webhook processing
4. **Test First**: Use test webhooks before going live

### Performance

1. **Batch Operations**: Process multiple products/orders together
2. **Schedule Heavy Tasks**: Run syncs during off-peak hours
3. **Archive Old Data**: Regularly archive old webhooks and orders
4. **Monitor API Limits**: Be aware of CJDropshipping API rate limits

## Support Resources

- GitHub Issues: https://github.com/MBadberg/odoo_cjdropship_addon/issues
- CJDropshipping API: https://developers.cjdropshipping.com/
- Odoo Documentation: https://www.odoo.com/documentation/19.0/
