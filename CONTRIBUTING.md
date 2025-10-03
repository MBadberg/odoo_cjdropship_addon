# Contributing to CJDropshipping Odoo Addon

Thank you for your interest in contributing to the CJDropshipping Odoo Addon! This document provides guidelines and instructions for contributing.

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior

- Be respectful and considerate
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other contributors

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**Good bug reports include:**
- Clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Odoo version and environment details
- Screenshots if applicable
- Error logs

**Example:**

```markdown
**Title:** Product import fails with 500 error

**Steps to reproduce:**
1. Go to Configuration > Settings
2. Click "Import Products"
3. Enter page 1, size 20
4. Click Import

**Expected:** Products imported successfully
**Actual:** 500 Internal Server Error

**Environment:**
- Odoo: 19.0 Community
- Python: 3.10
- OS: Ubuntu 22.04

**Error log:**
[paste error log here]
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:
- Clear description of the feature
- Use cases and benefits
- Potential implementation approach
- Any relevant examples

### Pull Requests

#### Before Submitting

1. Check existing PRs to avoid duplicates
2. Discuss major changes in an issue first
3. Test your changes thoroughly
4. Follow the coding standards

#### Process

1. **Fork the repository**
   ```bash
   git clone https://github.com/MBadberg/odoo_cjdropship_addon.git
   cd odoo_cjdropship_addon
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clear, commented code
   - Follow Odoo coding guidelines
   - Add/update documentation

4. **Test your changes**
   - Install the module in a test environment
   - Test all affected functionality
   - Verify no regressions

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add feature description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Provide clear title and description
   - Reference any related issues
   - Include screenshots if UI changes
   - List all changes made

#### Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: Add bulk product sync functionality

fix: Correct price calculation for percentage markup

docs: Update installation instructions in README

refactor: Improve API error handling
```

## Coding Standards

### Python Style

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) and [Odoo Guidelines](https://www.odoo.com/documentation/19.0/contributing/development/coding_guidelines.html):

```python
# Good
def calculate_price(self, base_price, markup):
    """Calculate final price with markup.
    
    Args:
        base_price (float): Base price from CJDropshipping
        markup (float): Markup percentage or amount
    
    Returns:
        float: Final price
    """
    if self.price_markup_type == 'percentage':
        return base_price * (1 + markup / 100)
    return base_price + markup

# Bad
def calc_price(self,bp,m):
    if self.pmt=='percentage':
        return bp*(1+m/100)
    return bp+m
```

### XML Style

Follow Odoo XML guidelines:

```xml
<!-- Good -->
<record id="view_product_form" model="ir.ui.view">
    <field name="name">product.form</field>
    <field name="model">product.product</field>
    <field name="arch" type="xml">
        <form string="Product">
            <group>
                <field name="name"/>
                <field name="price"/>
            </group>
        </form>
    </field>
</record>

<!-- Bad: Inconsistent indentation, unclear naming -->
<record id="v1" model="ir.ui.view">
<field name="name">f1</field>
<field name="model">product.product</field>
<field name="arch" type="xml">
<form>
<field name="name"/>
<field name="price"/>
</form>
</field>
</record>
```

### Documentation

#### Code Comments

```python
# Single-line comments for brief explanations
result = api.get_products()  # Fetch products from CJ

# Multi-line comments for complex logic
# This calculates the optimal shipping method based on:
# 1. Destination country
# 2. Package weight
# 3. Available shipping options
# 4. Cost optimization
shipping_method = self._calculate_shipping(order)
```

#### Docstrings

```python
def process_webhook(self, payload):
    """Process incoming webhook from CJDropshipping.
    
    This method handles all webhook types (order status, tracking, inventory)
    and updates the corresponding Odoo records.
    
    Args:
        payload (dict): Webhook payload from CJDropshipping
            {
                'event': 'order.status.updated',
                'orderId': 'CJ123456',
                'status': 'SHIPPED'
            }
    
    Returns:
        bool: True if processed successfully, False otherwise
    
    Raises:
        ValidationError: If payload is invalid
        UserError: If order not found
    """
    # Implementation
```

## Testing

### Manual Testing Checklist

Before submitting PR, test:

- [ ] Module installation
- [ ] Configuration setup
- [ ] Product import
- [ ] Product sync
- [ ] Order creation
- [ ] Order submission to CJ
- [ ] Status updates
- [ ] Webhook reception
- [ ] Error handling

### Test Scenarios

1. **Clean Install**
   - Install in fresh Odoo database
   - Verify no errors

2. **Configuration**
   - Test with valid credentials
   - Test with invalid credentials
   - Test connection

3. **Product Flow**
   - Import products
   - Create Odoo products
   - Sync product data
   - Update prices

4. **Order Flow**
   - Create order with CJ products
   - Submit to CJ
   - Update status
   - Query logistics

5. **Webhook Flow**
   - Send test webhook
   - Verify processing
   - Check error handling

## Documentation

### When to Update Documentation

Update documentation when:
- Adding new features
- Changing existing functionality
- Fixing bugs that affect usage
- Modifying configuration
- Adding/removing dependencies

### Documentation Files

- `README.md`: User-facing documentation
- `DEVELOPMENT.md`: Developer documentation
- `CONTRIBUTING.md`: This file
- Docstrings: In-code documentation

## Review Process

### What Reviewers Look For

- Code quality and style
- Test coverage
- Documentation completeness
- Performance considerations
- Security implications
- Backward compatibility

### Response Time

- Initial review: 3-7 days
- Follow-up reviews: 1-3 days
- Merging: After approval and CI pass

### Addressing Review Comments

- Respond to all comments
- Make requested changes
- Push updates to the same branch
- Re-request review when ready

## Getting Help

### Resources

- [Odoo Documentation](https://www.odoo.com/documentation/19.0/)
- [CJDropshipping API Docs](https://developers.cjdropshipping.com/)
- [Odoo Community Forum](https://www.odoo.com/forum)

### Contact

- GitHub Issues: For bugs and features
- GitHub Discussions: For questions and ideas
- Pull Requests: For code contributions

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant commits

Thank you for contributing to CJDropshipping Odoo Addon!
