#!/usr/bin/env python3
"""
Comprehensive Model Verification Script for CJDropshipping Odoo Module
Verifies that all models referenced in XML and CSV files are properly defined.
"""

import os
import re
import sys
import ast
from pathlib import Path

# Colors for output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

def print_error(msg):
    print(f"{RED}✗ {msg}{NC}")

def print_success(msg):
    print(f"{GREEN}✓ {msg}{NC}")

def print_warning(msg):
    print(f"{YELLOW}⚠ {msg}{NC}")

def print_info(msg):
    print(f"{BLUE}ℹ {msg}{NC}")

def print_header(msg):
    print(f"\n{'=' * 70}")
    print(msg)
    print('=' * 70)

def find_model_definitions_in_python(module_path):
    """Find all Odoo model definitions (_name attributes) in Python files."""
    models = {}
    
    for root, dirs, files in os.walk(module_path):
        # Skip __pycache__ and .git directories
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.pytest_cache']]
        
        for filename in files:
            if filename.endswith('.py') and filename != '__init__.py':
                filepath = os.path.join(root, filename)
                relative_path = os.path.relpath(filepath, module_path)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Parse the Python file
                    try:
                        tree = ast.parse(content)
                        
                        # Find all class definitions
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ClassDef):
                                # Check if class has _name attribute
                                for item in node.body:
                                    if isinstance(item, ast.Assign):
                                        for target in item.targets:
                                            if isinstance(target, ast.Name) and target.id == '_name':
                                                if isinstance(item.value, ast.Constant):
                                                    model_name = item.value.value
                                                    models[model_name] = {
                                                        'file': relative_path,
                                                        'class': node.name
                                                    }
                    except SyntaxError as e:
                        print_error(f"Syntax error in {relative_path}: {e}")
                        
                except Exception as e:
                    print_error(f"Error reading {relative_path}: {e}")
    
    return models

def find_model_references_in_xml(module_path):
    """Find all model references in XML files."""
    models = set()
    
    for root, dirs, files in os.walk(module_path):
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git']]
        
        for filename in files:
            if filename.endswith('.xml'):
                filepath = os.path.join(root, filename)
                relative_path = os.path.relpath(filepath, module_path)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Find model="..." patterns
                    matches = re.findall(r'model=["\']([^"\']+)["\']', content)
                    for match in matches:
                        # Only include cjdropship models
                        if match.startswith('cjdropship.'):
                            models.add(match)
                    
                    # Find <field name="model">...</field> patterns
                    field_matches = re.findall(r'<field name="model">([^<]+)</field>', content)
                    for match in field_matches:
                        match = match.strip()
                        if match.startswith('cjdropship.'):
                            models.add(match)
                            
                except Exception as e:
                    print_error(f"Error reading {relative_path}: {e}")
    
    return models

def find_model_references_in_csv(module_path):
    """Find all model references in CSV files (access rights)."""
    models = set()
    
    for root, dirs, files in os.walk(module_path):
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git']]
        
        for filename in files:
            if filename.endswith('.csv'):
                filepath = os.path.join(root, filename)
                relative_path = os.path.relpath(filepath, module_path)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # Skip header line
                    for line in lines[1:]:
                        # model_id:id column typically contains model_<model_name>
                        # Extract model names from model_cjdropship_* patterns
                        match = re.search(r'model_cjdropship_(\w+)', line)
                        if match:
                            # Convert model_cjdropship_product to cjdropship.product
                            model_parts = match.group(1).split('_')
                            if len(model_parts) == 1:
                                models.add(f'cjdropship.{model_parts[0]}')
                            else:
                                # Handle cases like product_import_wizard
                                models.add(f'cjdropship.{".".join(model_parts)}')
                            
                except Exception as e:
                    print_error(f"Error reading {relative_path}: {e}")
    
    return models

def check_imports(module_path):
    """Check that models are properly imported in __init__.py files."""
    issues = []
    
    # Check main __init__.py
    main_init = os.path.join(module_path, '__init__.py')
    if os.path.exists(main_init):
        with open(main_init, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'from . import models' not in content:
                issues.append("Main __init__.py doesn't import models")
            if 'from . import wizards' not in content:
                issues.append("Main __init__.py doesn't import wizards")
    else:
        issues.append("Main __init__.py not found")
    
    # Check models/__init__.py
    models_init = os.path.join(module_path, 'models', '__init__.py')
    if os.path.exists(models_init):
        with open(models_init, 'r', encoding='utf-8') as f:
            content = f.read()
            expected_imports = [
                'cjdropship_config',
                'cjdropship_product',
                'cjdropship_order',
                'cjdropship_webhook'
            ]
            for imp in expected_imports:
                if f'from . import {imp}' not in content:
                    issues.append(f"models/__init__.py doesn't import {imp}")
    else:
        issues.append("models/__init__.py not found")
    
    # Check wizards/__init__.py
    wizards_init = os.path.join(module_path, 'wizards', '__init__.py')
    if os.path.exists(wizards_init):
        with open(wizards_init, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'from . import product_import_wizard' not in content:
                issues.append("wizards/__init__.py doesn't import product_import_wizard")
    else:
        issues.append("wizards/__init__.py not found")
    
    return issues

def main():
    # Find module path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = '/home/runner/work/odoo_cjdropship_addon/odoo_cjdropship_addon'
    module_path = os.path.join(repo_root, 'cjdropship')
    
    if not os.path.exists(module_path):
        print_error(f"Module not found at: {module_path}")
        sys.exit(1)
    
    print_header("CJDropshipping Module Model Verification")
    print_info(f"Module path: {module_path}")
    
    # 1. Find all model definitions in Python files
    print_header("1. Scanning Python files for model definitions")
    python_models = find_model_definitions_in_python(module_path)
    
    if python_models:
        print_success(f"Found {len(python_models)} model definitions:")
        for model_name, info in sorted(python_models.items()):
            print(f"  • {model_name:45} → {info['file']:30} (class {info['class']})")
    else:
        print_error("No model definitions found!")
    
    # 2. Find model references in XML files
    print_header("2. Scanning XML files for model references")
    xml_models = find_model_references_in_xml(module_path)
    
    if xml_models:
        print_success(f"Found {len(xml_models)} model references in XML:")
        for model_name in sorted(xml_models):
            print(f"  • {model_name}")
    else:
        print_warning("No cjdropship model references found in XML files")
    
    # 3. Find model references in CSV files
    print_header("3. Scanning CSV files for model references")
    csv_models = find_model_references_in_csv(module_path)
    
    if csv_models:
        print_success(f"Found {len(csv_models)} model references in CSV:")
        for model_name in sorted(csv_models):
            print(f"  • {model_name}")
    else:
        print_warning("No model references found in CSV files")
    
    # 4. Check imports
    print_header("4. Checking __init__.py imports")
    import_issues = check_imports(module_path)
    
    if import_issues:
        print_error(f"Found {len(import_issues)} import issues:")
        for issue in import_issues:
            print(f"  • {issue}")
    else:
        print_success("All imports are correct")
    
    # 5. Cross-check: all referenced models should be defined
    print_header("5. Cross-checking: Referenced vs Defined Models")
    
    all_referenced = xml_models | csv_models
    all_defined = set(python_models.keys())
    
    missing = all_referenced - all_defined
    orphaned = all_defined - all_referenced
    
    if missing:
        print_error(f"Found {len(missing)} MISSING models (referenced but not defined):")
        for model_name in sorted(missing):
            print(f"  • {model_name}")
    else:
        print_success("All referenced models are properly defined")
    
    if orphaned:
        print_warning(f"Found {len(orphaned)} orphaned models (defined but not referenced):")
        for model_name in sorted(orphaned):
            print(f"  • {model_name}")
    
    # Final summary
    print_header("SUMMARY")
    
    errors = 0
    warnings = 0
    
    if not python_models:
        print_error("CRITICAL: No model definitions found!")
        errors += 1
    
    if import_issues:
        print_error(f"CRITICAL: {len(import_issues)} import issues found")
        errors += 1
    
    if missing:
        print_error(f"CRITICAL: {len(missing)} models are missing")
        errors += 1
    
    if orphaned:
        print_warning(f"INFO: {len(orphaned)} orphaned models (not necessarily a problem)")
        warnings += 1
    
    if errors == 0:
        print_success("\n✅ All models are properly defined and referenced!")
        print_success("   The module should install correctly in Odoo.")
        return 0
    else:
        print_error(f"\n❌ Found {errors} critical issues that need to be fixed!")
        if warnings:
            print_warning(f"   Also found {warnings} warnings")
        return 1

if __name__ == '__main__':
    sys.exit(main())
