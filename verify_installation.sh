#!/bin/bash
#########################################################################
# CJDropshipping Odoo Module - Installation Verification Script
#########################################################################
# This script helps diagnose installation issues and verifies that
# the module is correctly installed and ready to be activated in Odoo.
#########################################################################

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored messages
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_header() {
    echo ""
    echo "=========================================="
    echo "$1"
    echo "=========================================="
}

# Track issues
ISSUES_FOUND=0

# Find Odoo addons directories
find_addons_paths() {
    print_header "Searching for Odoo Installation"
    
    ADDONS_PATHS=()
    
    # Check common locations
    COMMON_PATHS=(
        "/opt/odoo/addons"
        "/opt/odoo/custom/addons"
        "/usr/lib/python3/dist-packages/odoo/addons"
        "/var/lib/odoo/addons"
        "$HOME/odoo/addons"
    )
    
    for path in "${COMMON_PATHS[@]}"; do
        if [ -d "$path" ]; then
            ADDONS_PATHS+=("$path")
            print_info "Found: $path"
        fi
    done
    
    # Check odoo.conf
    if [ -f "/etc/odoo/odoo.conf" ]; then
        print_info "Found: /etc/odoo/odoo.conf"
        CONF_PATHS=$(grep "^addons_path" /etc/odoo/odoo.conf | cut -d'=' -f2 | tr ',' '\n')
        while IFS= read -r path; do
            path=$(echo "$path" | xargs)  # trim whitespace
            if [ -d "$path" ]; then
                if [[ ! " ${ADDONS_PATHS[@]} " =~ " ${path} " ]]; then
                    ADDONS_PATHS+=("$path")
                    print_info "Found in config: $path"
                fi
            fi
        done <<< "$CONF_PATHS"
    fi
    
    if [ ${#ADDONS_PATHS[@]} -eq 0 ]; then
        print_error "No Odoo addons directories found!"
        print_info "Please specify the path manually."
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
        return 1
    fi
    
    print_success "Found ${#ADDONS_PATHS[@]} addons directory/directories"
}

# Check if module is installed
check_module_installation() {
    print_header "Checking Module Installation"
    
    MODULE_FOUND=false
    
    for addons_path in "${ADDONS_PATHS[@]}"; do
        MODULE_PATH="$addons_path/cjdropship"
        
        if [ -d "$MODULE_PATH" ] || [ -L "$MODULE_PATH" ]; then
            MODULE_FOUND=true
            print_success "Module found at: $MODULE_PATH"
            
            # Check if it's a symlink
            if [ -L "$MODULE_PATH" ]; then
                TARGET=$(readlink -f "$MODULE_PATH")
                print_info "  → Symlink points to: $TARGET"
            fi
            
            # Check __manifest__.py
            if [ -f "$MODULE_PATH/__manifest__.py" ]; then
                print_success "  __manifest__.py exists"
            else
                print_error "  __manifest__.py is MISSING!"
                ISSUES_FOUND=$((ISSUES_FOUND + 1))
            fi
            
            # Check __init__.py
            if [ -f "$MODULE_PATH/__init__.py" ]; then
                print_success "  __init__.py exists"
            else
                print_error "  __init__.py is MISSING!"
                ISSUES_FOUND=$((ISSUES_FOUND + 1))
            fi
            
            # Check required directories
            for dir in models views controllers security data; do
                if [ -d "$MODULE_PATH/$dir" ]; then
                    print_success "  $dir/ directory exists"
                else
                    print_warning "  $dir/ directory not found"
                fi
            done
            
            # Check permissions
            if [ -r "$MODULE_PATH/__manifest__.py" ]; then
                print_success "  Files are readable"
            else
                print_error "  Permission issue: Files are not readable!"
                ISSUES_FOUND=$((ISSUES_FOUND + 1))
            fi
        fi
    done
    
    if [ "$MODULE_FOUND" = false ]; then
        print_error "Module NOT FOUND in any addons directory!"
        print_info "Expected location: [addons_path]/cjdropship/"
        print_info "Make sure you copied/symlinked the 'cjdropship' folder, not the repository folder."
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
}

# Check Python dependencies
check_dependencies() {
    print_header "Checking Python Dependencies"
    
    if command -v python3 &> /dev/null; then
        print_success "Python 3 is installed"
        
        # Check requests library
        if python3 -c "import requests" 2>/dev/null; then
            print_success "requests library is installed"
        else
            print_error "requests library is NOT installed!"
            print_info "Install it with: pip3 install requests"
            ISSUES_FOUND=$((ISSUES_FOUND + 1))
        fi
    else
        print_error "Python 3 is NOT installed!"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
}

# Check Odoo service
check_odoo_service() {
    print_header "Checking Odoo Service"
    
    if command -v systemctl &> /dev/null; then
        if systemctl list-units --type=service --all | grep -q "odoo.service"; then
            STATUS=$(systemctl is-active odoo)
            if [ "$STATUS" = "active" ]; then
                print_success "Odoo service is running"
            else
                print_warning "Odoo service is not running (status: $STATUS)"
                print_info "Start it with: sudo systemctl start odoo"
            fi
        else
            print_warning "Odoo service not found (may be running manually)"
        fi
    else
        print_warning "systemctl not available (may be using direct execution)"
    fi
}

# Validate module structure
validate_module_structure() {
    print_header "Validating Module Structure"
    
    for addons_path in "${ADDONS_PATHS[@]}"; do
        MODULE_PATH="$addons_path/cjdropship"
        
        if [ -d "$MODULE_PATH" ] || [ -L "$MODULE_PATH" ]; then
            print_info "Validating: $MODULE_PATH"
            
            # Use Python to validate manifest
            python3 <<EOF
import os
import sys

module_path = "$MODULE_PATH"
manifest_path = os.path.join(module_path, "__manifest__.py")

if not os.path.exists(manifest_path):
    print("\033[0;31m✗ __manifest__.py not found\033[0m")
    sys.exit(1)

try:
    with open(manifest_path, 'r') as f:
        content = f.read()
        manifest = eval(content)
    
    # Check required fields
    required = ['name', 'version', 'depends', 'data']
    for field in required:
        if field not in manifest:
            print(f"\033[0;31m✗ Missing required field: {field}\033[0m")
            sys.exit(1)
    
    print("\033[0;32m✓ __manifest__.py is valid\033[0m")
    print(f"\033[0;32m✓ Module name: {manifest['name']}\033[0m")
    print(f"\033[0;32m✓ Version: {manifest['version']}\033[0m")
    
    if manifest.get('installable') != True:
        print("\033[0;31m✗ installable is not True!\033[0m")
        sys.exit(1)
    else:
        print("\033[0;32m✓ installable: True\033[0m")
    
    # Check data files
    missing = []
    for data_file in manifest.get('data', []):
        full_path = os.path.join(module_path, data_file)
        if not os.path.exists(full_path):
            missing.append(data_file)
    
    if missing:
        print(f"\033[0;31m✗ {len(missing)} data files are missing:\033[0m")
        for f in missing:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"\033[0;32m✓ All {len(manifest['data'])} data files exist\033[0m")
    
except Exception as e:
    print(f"\033[0;31m✗ Error validating manifest: {e}\033[0m")
    sys.exit(1)
EOF
            
            if [ $? -ne 0 ]; then
                ISSUES_FOUND=$((ISSUES_FOUND + 1))
            fi
        fi
    done
}

# Print diagnosis
print_diagnosis() {
    print_header "Diagnosis Summary"
    
    if [ $ISSUES_FOUND -eq 0 ]; then
        echo ""
        print_success "No issues found! The module appears to be correctly installed."
        echo ""
        print_info "Next steps:"
        echo "1. Open Odoo in your browser"
        echo "2. Go to Apps"
        echo "3. Click 'Update Apps List' (you may need to remove filters)"
        echo "4. Search for 'CJDropshipping Integration'"
        echo "5. Click 'Install'"
        echo ""
    else
        echo ""
        print_error "Found $ISSUES_FOUND issue(s) that need to be fixed."
        echo ""
        print_info "Common solutions:"
        echo ""
        echo "1. Wrong directory structure:"
        echo "   ✗ /addons/odoo_cjdropship_addon/cjdropship/"
        echo "   ✓ /addons/cjdropship/"
        echo ""
        echo "2. Module not in addons path:"
        echo "   - Copy or symlink the 'cjdropship' folder to your Odoo addons directory"
        echo "   - Use the install.sh script for automated installation"
        echo ""
        echo "3. Missing dependencies:"
        echo "   pip3 install requests"
        echo ""
        echo "4. Permission issues:"
        echo "   sudo chown -R odoo:odoo /path/to/addons/cjdropship"
        echo ""
        echo "5. Need to restart Odoo:"
        echo "   sudo systemctl restart odoo"
        echo ""
    fi
}

# Main function
main() {
    print_header "CJDropshipping Module Verification"
    echo "This script will check if the module is correctly installed."
    
    find_addons_paths
    check_module_installation
    check_dependencies
    check_odoo_service
    validate_module_structure
    print_diagnosis
}

# Run main function
main
