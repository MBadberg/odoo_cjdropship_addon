# Installation Guide - CJDropshipping Odoo 19 Addon

## 🚀 Quick Start - Automated Installation

**The easiest way to install this module:**

```bash
git clone https://github.com/MBadberg/odoo_cjdropship_addon.git
cd odoo_cjdropship_addon
./install.sh
```

The installation script will:
- ✅ Automatically detect your Odoo installation
- ✅ Install the module in the correct location
- ✅ Install Python dependencies
- ✅ Set proper permissions
- ✅ Optionally restart Odoo

**After installation, verify everything is correct:**

```bash
./verify_installation.sh
```

If you encounter any issues, this script will tell you exactly what's wrong and how to fix it.

---

## ⚠️ Important: Correct Directory Structure

The most common installation issue is incorrect directory structure. This module **must** be installed correctly to appear as "Installable" in Odoo.

### ✅ Correct Structure

```
/path/to/odoo/addons/
├── base/
├── sale_management/
├── stock/
└── cjdropship/          ← The module folder
    ├── __init__.py
    ├── __manifest__.py
    ├── models/
    ├── views/
    ├── controllers/
    ├── wizards/
    ├── security/
    ├── data/
    └── static/
```

### ❌ Incorrect Structure (Will Show as "Not Installable")

```
/path/to/odoo/addons/
└── odoo_cjdropship_addon/     ← Repository folder
    └── cjdropship/             ← Module folder (too deep!)
        ├── __init__.py
        ├── __manifest__.py
        └── ...
```

## Installation Methods

### Method 1: Copy Module Folder (Recommended for Production)

```bash
# 1. Clone repository to temporary location
cd /tmp
git clone https://github.com/MBadberg/odoo_cjdropship_addon.git

# 2. Copy only the cjdropship folder to Odoo addons
sudo cp -r odoo_cjdropship_addon/cjdropship /path/to/odoo/addons/

# 3. Set correct permissions
sudo chown -R odoo:odoo /path/to/odoo/addons/cjdropship

# 4. Verify structure
ls -l /path/to/odoo/addons/cjdropship/__manifest__.py
# Should show the file exists

# 5. Restart Odoo
sudo systemctl restart odoo
# OR
./odoo-bin -c odoo.conf
```

### Method 2: Symbolic Link (Recommended for Development)

```bash
# 1. Clone repository to permanent location
cd /opt
sudo git clone https://github.com/MBadberg/odoo_cjdropship_addon.git

# 2. Create symlink to module folder
sudo ln -s /opt/odoo_cjdropship_addon/cjdropship /path/to/odoo/addons/cjdropship

# 3. Verify symlink
ls -l /path/to/odoo/addons/cjdropship
# Should show: cjdropship -> /opt/odoo_cjdropship_addon/cjdropship

# 4. Restart Odoo
sudo systemctl restart odoo
```

### Method 3: Using Custom Addons Path

If you don't want to copy/symlink, you can add the repository path directly:

```bash
# 1. Clone repository
cd /opt
sudo git clone https://github.com/MBadberg/odoo_cjdropship_addon.git

# 2. Edit odoo.conf
sudo nano /etc/odoo/odoo.conf

# 3. Add to addons_path (note: we add the cjdropship subfolder directly)
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/path/to/odoo/addons,/opt/odoo_cjdropship_addon

# 4. Restart Odoo
sudo systemctl restart odoo
```

⚠️ **Note**: For Method 3, Odoo will scan `/opt/odoo_cjdropship_addon` and find the `cjdropship` subdirectory automatically.

## Installing the Module in Odoo

1. **Log in to Odoo** as Administrator

2. **Enable Developer Mode**
   - Go to Settings
   - Scroll to bottom
   - Click "Activate the developer mode"

3. **Update Apps List**
   - Go to Apps menu
   - Click "Update Apps List" (in the top menu, may need to enable filters)
   - Click "Update" in the dialog

4. **Search for Module**
   - In Apps, remove "Apps" filter to show all modules
   - Search for "CJDropshipping"
   - You should see "CJDropshipping Integration"

5. **Install Module**
   - Click "Install" button
   - Wait for installation to complete
   - You'll see a confirmation message

## Verifying Installation

### Check Module Status in Odoo UI

After installation:
- Go to **Apps** menu
- Search for "CJDropshipping"
- Status should show "Installed"

### Check from Command Line

```bash
# Connect to Odoo database
psql -U odoo -d your_database_name

# Check if module is installed
SELECT name, state FROM ir_module_module WHERE name = 'cjdropship';

# Should show:
#    name    | state
# -----------+-----------
#  cjdropship | installed
```

### Check Odoo Logs

```bash
# View Odoo logs
sudo tail -f /var/log/odoo/odoo-server.log | grep cjdropship

# You should see:
# Loading module cjdropship
# Module cjdropship loaded successfully
```

## Troubleshooting

### Problem: Module not found in Apps list

**Diagnosis:**
```bash
# Check if module folder exists in addons path
ls -la /path/to/odoo/addons/cjdropship

# Check Odoo config
grep addons_path /etc/odoo/odoo.conf
```

**Solution:**
- Verify the `cjdropship` folder is directly in the addons path
- Make sure `__manifest__.py` exists in `cjdropship/` folder
- Restart Odoo and update apps list

### Problem: Shows as "Not Installable"

**Diagnosis:**
```bash
# Check manifest file
cat /path/to/odoo/addons/cjdropship/__manifest__.py | grep installable

# Should show: 'installable': True
```

**Common Causes:**
1. ❌ Wrong directory structure (repo folder instead of module folder)
2. ❌ Missing dependencies (base, sale_management, stock, product)
3. ❌ Python syntax errors in code
4. ❌ XML syntax errors in views

**Solution:**
```bash
# Verify structure is correct
cd /path/to/odoo/addons
ls -la cjdropship/__manifest__.py  # Should exist
ls -la cjdropship/models/__init__.py  # Should exist

# Check for Python errors
python3 -m py_compile cjdropship/__manifest__.py
python3 -m py_compile cjdropship/__init__.py

# Check Odoo logs for specific errors
sudo tail -100 /var/log/odoo/odoo-server.log
```

### Problem: Missing Dependencies

**Error in logs:**
```
No module named 'requests'
```

**Solution:**
```bash
# Install Python dependencies
pip3 install requests

# Restart Odoo
sudo systemctl restart odoo
```

### Problem: Database Error During Installation

**Error:**
```
relation "cjdropship_config" does not exist
```

**Solution:**
1. Check XML/CSV files for syntax errors
2. Ensure all data files listed in `__manifest__.py` exist
3. Check Odoo logs for specific error details

## Post-Installation Configuration

After successful installation:

1. **Go to CJDropshipping Settings**
   - Navigate: CJDropshipping > Configuration > Settings

2. **Enter API Credentials**
   - API Email: your-email@cjdropshipping.com
   - API Password: your-password

3. **Test Connection**
   - Click "Test Connection" button
   - Should see success message

4. **Configure Import Settings**
   - Default Product Type: Consumable (recommended)
   - Price Markup: 30% (adjust as needed)
   - Auto Sync: Off initially (enable after testing)

## Support

If you continue to experience issues:

1. **Check Logs:**
   ```bash
   sudo tail -f /var/log/odoo/odoo-server.log
   ```

2. **Enable Debug Mode:**
   - Settings > Activate Developer Mode
   - Shows more detailed error messages

3. **Report Issue:**
   - GitHub Issues: https://github.com/MBadberg/odoo_cjdropship_addon/issues
   - Include: Odoo version, installation method, error logs

## Quick Reference Commands

```bash
# Check if module folder is in correct location
ls -l /path/to/odoo/addons/cjdropship/__manifest__.py

# View Odoo config
cat /etc/odoo/odoo.conf | grep addons_path

# Restart Odoo (systemd)
sudo systemctl restart odoo

# Restart Odoo (direct)
./odoo-bin -c odoo.conf

# View logs
sudo tail -f /var/log/odoo/odoo-server.log

# Check module status in database
psql -U odoo -d dbname -c "SELECT name, state FROM ir_module_module WHERE name = 'cjdropship';"
```
