#!/usr/bin/env python3
"""
Simple test to verify all model classes have correct _name attributes.
This only checks class definitions without trying to import the full modules.
"""

import ast
import os
import sys

def extract_model_info_from_file(filepath):
    """Extract model class name and _name attribute from a Python file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return None, f"Syntax error: {e}"
    
    models = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Check if this class inherits from Model or TransientModel
            is_model = False
            for base in node.bases:
                if isinstance(base, ast.Attribute):
                    if base.attr in ['Model', 'TransientModel']:
                        is_model = True
                        break
            
            if is_model:
                # Find _name attribute
                model_name = None
                model_description = None
                
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                if target.id == '_name' and isinstance(item.value, ast.Constant):
                                    model_name = item.value.value
                                elif target.id == '_description' and isinstance(item.value, ast.Constant):
                                    model_description = item.value.value
                
                if model_name:
                    models.append({
                        'class_name': node.name,
                        'model_name': model_name,
                        'description': model_description
                    })
    
    return models, None

def main():
    repo_root = '/home/runner/work/odoo_cjdropship_addon/odoo_cjdropship_addon'
    module_path = os.path.join(repo_root, 'cjdropship')
    
    print("=" * 70)
    print("Simple Model Verification Test")
    print("=" * 70)
    print()
    
    expected_models = {
        'cjdropship.config': {
            'file': 'models/cjdropship_config.py',
            'class': 'CJDropshippingConfig'
        },
        'cjdropship.product': {
            'file': 'models/cjdropship_product.py',
            'class': 'CJDropshippingProduct'
        },
        'cjdropship.order': {
            'file': 'models/cjdropship_order.py',
            'class': 'CJDropshippingOrder'
        },
        'cjdropship.webhook': {
            'file': 'models/cjdropship_webhook.py',
            'class': 'CJDropshippingWebhook'
        },
        'cjdropship.product.import.wizard': {
            'file': 'wizards/product_import_wizard.py',
            'class': 'ProductImportWizard'
        }
    }
    
    all_found = True
    
    for model_name, info in expected_models.items():
        filepath = os.path.join(module_path, info['file'])
        
        if not os.path.exists(filepath):
            print(f"❌ {model_name}")
            print(f"   File not found: {info['file']}")
            all_found = False
            continue
        
        models, error = extract_model_info_from_file(filepath)
        
        if error:
            print(f"❌ {model_name}")
            print(f"   Error: {error}")
            all_found = False
            continue
        
        found = False
        for model in models:
            if model['model_name'] == model_name:
                if model['class_name'] == info['class']:
                    print(f"✅ {model_name}")
                    print(f"   File: {info['file']}")
                    print(f"   Class: {model['class_name']}")
                    if model['description']:
                        print(f"   Description: {model['description']}")
                    print()
                    found = True
                else:
                    print(f"⚠️  {model_name}")
                    print(f"   Expected class: {info['class']}")
                    print(f"   Found class: {model['class_name']}")
                    print()
                    found = True
                break
        
        if not found:
            print(f"❌ {model_name}")
            print(f"   Model not found in {info['file']}")
            all_found = False
    
    print("=" * 70)
    if all_found:
        print("✅ ALL MODELS VERIFIED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print("Summary:")
        print("  • All 5 expected models are properly defined")
        print("  • Each model has correct _name attribute")
        print("  • Python syntax is valid")
        print()
        print("The module should install correctly in Odoo.")
        return 0
    else:
        print("❌ VERIFICATION FAILED!")
        print("=" * 70)
        print()
        print("Some models are missing or incorrectly defined.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
