# Widget Replacements - Enterprise to Community Edition

This document shows all the widget replacements made to convert the addon from Enterprise to Community Edition compatibility.

## Summary

| Widget | Instances | Replacement | Files Affected |
|--------|-----------|-------------|----------------|
| `web_ribbon` | 1 | Removed | config_views.xml |
| `boolean_toggle` | 6 | Standard checkbox | config, product, webhook views |
| `ace` | 4 | `widget="text"` | order, webhook views |
| `badge` | 2 | Standard field | order views |
| **Total** | **13** | - | **4 files** |

---

## 1. web_ribbon Widget

### Before (Enterprise)
```xml
<widget name="web_ribbon" title="Archived" bg_color="text-bg-danger" invisible="active"/>
```

### After (Community)
```xml
<!-- Removed - Odoo handles archived status automatically -->
```

**File:** `cjdropship/views/cjdropship_config_views.xml`

**Impact:** The ribbon showing "Archived" on inactive records is removed. Odoo still indicates archived records through standard UI elements.

---

## 2. boolean_toggle Widget

### Before (Enterprise)
```xml
<field name="active" widget="boolean_toggle"/>
<field name="processed" widget="boolean_toggle"/>
```

### After (Community)
```xml
<field name="active"/>
<field name="processed"/>
```

**Files:**
- `cjdropship/views/cjdropship_config_views.xml` (2 instances)
- `cjdropship/views/cjdropship_product_views.xml` (2 instances)
- `cjdropship/views/cjdropship_webhook_views.xml` (2 instances)

**Impact:** Toggle switches are replaced with standard checkboxes. Functionality remains identical.

---

## 3. ace Widget (Code Editor)

### Before (Enterprise)
```xml
<field name="request_data" widget="ace" options="{'mode': 'json'}"/>
<field name="response_data" widget="ace" options="{'mode': 'json'}"/>
<field name="payload" widget="ace" options="{'mode': 'json'}"/>
<field name="headers" widget="ace" options="{'mode': 'json'}"/>
```

### After (Community)
```xml
<field name="request_data" widget="text"/>
<field name="response_data" widget="text"/>
<field name="payload" widget="text"/>
<field name="headers" widget="text"/>
```

**Files:**
- `cjdropship/views/cjdropship_order_views.xml` (2 instances)
- `cjdropship/views/cjdropship_webhook_views.xml` (2 instances)

**Impact:** JSON data is displayed in a text area without syntax highlighting. Users can still view and copy the data. Consider formatting JSON in Python before displaying for better readability.

---

## 4. badge Widget

### Before (Enterprise)
```xml
<field name="state" widget="badge" 
    decoration-info="state == 'draft'" 
    decoration-warning="state == 'processing'"
    decoration-success="state in ['shipped', 'delivered']"/>

<field name="cjdropship_state" widget="badge"/>
```

### After (Community)
```xml
<field name="state"/>

<field name="cjdropship_state"/>
```

**Files:**
- `cjdropship/views/cjdropship_order_views.xml` (2 instances)

**Impact:** Status fields display as plain text instead of colored badges. Tree view decorations (row colors) are still applied via `decoration-*` attributes on the `<tree>` element.

---

## Visual Comparison

### Boolean Fields

| Enterprise | Community |
|------------|-----------|
| Toggle switch (on/off slider) | Checkbox (☐/☑) |
| Modern UI | Classic UI |

### JSON/Code Display

| Enterprise | Community |
|------------|-----------|
| Syntax highlighted code editor | Plain text area |
| Line numbers | No line numbers |
| Code folding | Full text display |

### Status Display

| Enterprise | Community |
|------------|-----------|
| Colored badge pills | Plain text |
| `[Draft]` in blue pill | "draft" text |

---

## Testing Checklist

After these changes, verify:

- [ ] Configuration form opens without errors
- [ ] Boolean fields work as checkboxes
- [ ] JSON data is visible and readable in webhook/order forms
- [ ] Status fields show correct values
- [ ] All menus and actions work
- [ ] No console errors in browser
- [ ] Module installs successfully
- [ ] All CRUD operations work on all models

---

## Additional Notes

### For Developers

If you need better JSON display in Community Edition, consider:

1. **Format in Python**: Use `json.dumps(data, indent=2)` before storing
2. **Add HTML widget**: Create a computed field with formatted HTML
3. **Custom widget**: Create a simple Community-compatible JSON viewer widget

Example:
```python
formatted_json = fields.Text(
    string='Formatted JSON',
    compute='_compute_formatted_json',
    store=False
)

@api.depends('payload')
def _compute_formatted_json(self):
    for record in self:
        if record.payload:
            try:
                data = json.loads(record.payload)
                record.formatted_json = json.dumps(data, indent=2)
            except:
                record.formatted_json = record.payload
```

### For Users

The functionality of the addon remains exactly the same. Only visual presentation differs slightly:

- Boolean fields: Click the checkbox instead of toggling a switch
- JSON data: Displayed as formatted text instead of syntax-highlighted code
- Status: Shown as text instead of colored badges

All core features work identically in Community Edition as they would in Enterprise.

---

## Compatibility

These changes make the addon compatible with:

- ✅ Odoo Community Edition 19.0 and 19.1 (including alpha versions)
- ✅ Odoo Community Edition 18.0 (likely)
- ✅ Odoo Community Edition 17.0 (with minor adjustments)
- ✅ Odoo Enterprise Edition 19.0 and 19.1 (backwards compatible)

The addon uses only standard Odoo widgets that have been available since Odoo 10.0.
