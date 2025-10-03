# CJDropshipping Odoo Addon - Quick Start Guide

Get up and running with CJDropshipping integration in 10 minutes!

## Prerequisites

- ✅ Odoo 19.0 installed
- ✅ CJDropshipping account with API access
- ✅ Python `requests` library installed

## Installation (5 minutes)

### Step 1: Clone Repository

```bash
cd /path/to/odoo/addons
git clone https://github.com/MBadberg/odoo_cjdropship_addon.git
```

### Step 2: Install Dependencies

```bash
pip3 install requests
```

### Step 3: Restart Odoo

```bash
./odoo-bin -c odoo.conf --addons-path=/path/to/odoo/addons
```

### Step 4: Install Module

1. Go to **Apps** in Odoo
2. Click **Update Apps List**
3. Search for **"CJDropshipping Integration"**
4. Click **Install**

## Configuration (3 minutes)

### Step 1: Open Settings

Navigate to: **CJDropshipping > Configuration > Settings**

### Step 2: Enter API Credentials

Fill in:
- **API Email**: `your-email@example.com`
- **API Password**: `your-password`

### Step 3: Configure Basic Settings

Recommended settings for beginners:
- **Default Product Type**: Consumable
- **Price Markup Type**: Percentage
- **Price Markup**: 30
- **Auto Fulfill Orders**: No (start with manual)

### Step 4: Test Connection

Click **"Test Connection"** button

✅ If successful, you'll see "Successfully connected to CJDropshipping API"

## Import Your First Products (2 minutes)

### Step 1: Open Import Wizard

From Settings page, click **"Import Products"**

### Step 2: Configure Import

- **Page Number**: 1
- **Products per Page**: 10
- **Create Odoo Products Immediately**: Yes

### Step 3: Import

Click **"Import Products"**

Wait for completion message: "10 products imported successfully"

### Step 4: View Products

Navigate to: **CJDropshipping > Products > CJ Products**

You should see your imported products!

## Create Your First Order (3 minutes)

### Step 1: Create Sale Order

1. Go to **Sales > Orders > Orders**
2. Click **Create**
3. Select a customer
4. Add CJDropshipping products
5. Click **Confirm**

### Step 2: Submit to CJDropshipping

On the sale order form:
1. Click **"Submit to CJDropshipping"**
2. Wait for confirmation
3. You'll see CJ Order status in the button box

### Step 3: Track Order

Click the **"CJ Order"** button to view:
- CJ Order ID
- Status
- Tracking number (when shipped)

## What's Next?

Now that you're set up, explore these features:

### 🔄 Automatic Sync
Enable automatic product synchronization:
1. Go to **Settings**
2. Enable **Auto Sync Products**
3. Set **Sync Interval** to 24 hours

### 🚀 Auto Fulfillment
Enable automatic order submission:
1. Go to **Settings**
2. Enable **Auto Fulfill Orders**
3. Orders will be sent to CJ automatically when confirmed

### 🔔 Webhooks
Set up real-time status updates:
1. Copy **Webhook URL** from Settings
2. Configure in CJDropshipping dashboard
3. Receive automatic status updates

### 📊 Monitor Operations

Check these regularly:
- **CJ Products**: View all imported products
- **CJ Orders**: Track order fulfillment
- **Webhooks**: Monitor incoming events

## Common Tasks Reference

### Import More Products

```
CJDropshipping > Configuration > Settings > Import Products
```

### Sync Product Prices

```
CJDropshipping > Products > CJ Products
Select products > Action > Sync from CJ
```

### Check Order Status

```
CJDropshipping > Orders > CJ Orders
Select order > Update Status
```

### View Tracking Info

```
CJDropshipping > Orders > CJ Orders
Select order > Query Logistics
```

## Troubleshooting Quick Fixes

### ❌ Connection Failed

**Solution:**
1. Verify API credentials
2. Check internet connection
3. Ensure firewall allows outbound HTTPS

### ❌ Import Failed

**Solution:**
1. Test connection first
2. Try smaller batch (5 products)
3. Check Odoo logs for details

### ❌ Order Submission Failed

**Solution:**
1. Verify products are CJDropshipping products
2. Check customer address is complete
3. Review error message in CJ Order

### ❌ Webhook Not Received

**Solution:**
1. Verify URL is accessible externally
2. Check webhook is enabled in Settings
3. Test with curl/Postman

## Keyboard Shortcuts

Useful shortcuts in Odoo:

- `Alt + C`: Create new record
- `Alt + E`: Edit record
- `Alt + S`: Save record
- `Ctrl + K`: Open command palette

## Support

Need help?

- 📖 Full docs: [README.md](README.md)
- 🔧 Developer guide: [DEVELOPMENT.md](DEVELOPMENT.md)
- 💡 Examples: [EXAMPLES.md](EXAMPLES.md)
- 🐛 Report issues: [GitHub Issues](https://github.com/MBadberg/odoo_cjdropship_addon/issues)

## Quick Command Reference

### View Logs
```bash
tail -f /var/log/odoo/odoo.log | grep cjdropship
```

### Check Module Status
```bash
./odoo-bin shell -c odoo.conf
>>> env['ir.module.module'].search([('name', '=', 'cjdropship')])
```

### Test API Connection
```bash
./odoo-bin shell -c odoo.conf
>>> config = env['cjdropship.config'].get_default_config()
>>> api = config.get_api_client()
>>> categories = api.get_categories()
>>> print(f"Success! Found {len(categories)} categories")
```

## Next Steps

Once comfortable with basics:

1. ✅ Set up automatic sync
2. ✅ Enable auto fulfillment
3. ✅ Configure webhooks
4. ✅ Customize price markup
5. ✅ Import more products
6. ✅ Process real orders

## Success Checklist

After completing this guide, you should be able to:

- [x] Install and configure the addon
- [x] Import products from CJDropshipping
- [x] Create Odoo products from CJ products
- [x] Submit orders to CJDropshipping
- [x] Track order status
- [x] Navigate the UI

🎉 Congratulations! You're ready to use CJDropshipping with Odoo!

---

**Time to Value**: ~10 minutes from installation to first order

**Difficulty**: Beginner-friendly

**Support Level**: Community-supported with comprehensive documentation
