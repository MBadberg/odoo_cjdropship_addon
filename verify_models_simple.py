#!/usr/bin/env python3
"""
Simple test to verify all model classes have correct _name attributes.
This only checks class definitions without trying to import the full modules.
"""

import ast
import logging
import os
import sys

logger = logging.getLogger(__name__)

def _is_odoo_model(node):
    """Check if a class node inherits from Model or TransientModel."""
    for base in node.bases:
        if isinstance(base, ast.Attribute):
            if base.attr in ['Model', 'TransientModel']:
                return True
    return False


def _extract_model_attributes(node):
    """Extract _name and _description from a class node."""
    model_name = None
    model_description = None

    for item in node.body:
        if not isinstance(item, ast.Assign):
            continue
        for target in item.targets:
            if not isinstance(target, ast.Name):
                continue
            if (target.id == '_name' and
                    isinstance(item.value, ast.Constant)):
                model_name = item.value.value
            elif (target.id == '_description' and
                  isinstance(item.value, ast.Constant)):
                model_description = item.value.value

    return model_name, model_description


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
        if not isinstance(node, ast.ClassDef):
            continue

        if not _is_odoo_model(node):
            continue

        model_name, model_description = _extract_model_attributes(node)

        if model_name:
            models.append({
                'class_name': node.name,
                'model_name': model_name,
                'description': model_description
            })

    return models, None

def main():
    """Run simple model verification test."""
    repo_root = '/home/runner/work/odoo_cjdropship_addon/odoo_cjdropship_addon'
    module_path = os.path.join(repo_root, 'cjdropship')

    logger.info("=" * 70)
    logger.info("Simple Model Verification Test")
    logger.info("=" * 70)
    logger.info("")

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
            logger.error("❌ %s", model_name)
            logger.error("   File not found: %s", info['file'])
            all_found = False
            continue

        models, error = extract_model_info_from_file(filepath)

        if error:
            logger.error("❌ %s", model_name)
            logger.error("   Error: %s", error)
            all_found = False
            continue

        found = False
        for model in models:
            if model['model_name'] == model_name:
                if model['class_name'] == info['class']:
                    logger.info("✅ %s", model_name)
                    logger.info("   File: %s", info['file'])
                    logger.info("   Class: %s", model['class_name'])
                    if model['description']:
                        logger.info("   Description: %s",
                                    model['description'])
                    logger.info("")
                    found = True
                else:
                    logger.warning("⚠️  %s", model_name)
                    logger.warning("   Expected class: %s", info['class'])
                    logger.warning("   Found class: %s",
                                   model['class_name'])
                    logger.info("")
                    found = True
                break

        if not found:
            logger.error("❌ %s", model_name)
            logger.error("   Model not found in %s", info['file'])
            all_found = False

    logger.info("=" * 70)
    if all_found:
        logger.info("✅ ALL MODELS VERIFIED SUCCESSFULLY!")
        logger.info("=" * 70)
        logger.info("")
        logger.info("Summary:")
        logger.info("  • All 5 expected models are properly defined")
        logger.info("  • Each model has correct _name attribute")
        logger.info("  • Python syntax is valid")
        logger.info("")
        logger.info("The module should install correctly in Odoo.")
        return 0

    logger.error("❌ VERIFICATION FAILED!")
    logger.error("=" * 70)
    logger.error("")
    logger.error("Some models are missing or incorrectly defined.")
    return 1

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    sys.exit(main())
