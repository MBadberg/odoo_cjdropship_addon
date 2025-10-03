#!/bin/bash
#########################################################################
# CJDropshipping Odoo Module - Automated Installation Script
#########################################################################
# This script automates the installation of the CJDropshipping module
# for Odoo 19. It handles directory structure, permissions, and validation.
#########################################################################

set -e  # Exit on error

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

# Check if script is run from correct directory
check_directory() {
    if [ ! -d "cjdropship" ]; then
        print_error "The 'cjdropship' directory was not found."
        print_error "Please run this script from the repository root directory."
        exit 1
    fi
    
    if [ ! -f "cjdropship/__manifest__.py" ]; then
        print_error "Invalid module structure: __manifest__.py not found."
        exit 1
    fi
    
    print_success "Module structure validated"
}

# Detect Odoo installation
detect_odoo() {
    print_header "Detecting Odoo Installation"
    
    ODOO_ADDONS_PATH=""
    
    # Common Odoo installation paths
    COMMON_PATHS=(
        "/opt/odoo/addons"
        "/opt/odoo/custom/addons"
        "/usr/lib/python3/dist-packages/odoo/addons"
        "/var/lib/odoo/addons"
        "$HOME/odoo/addons"
    )
    
    # Check common paths
    for path in "${COMMON_PATHS[@]}"; do
        if [ -d "$path" ]; then
            print_info "Found Odoo addons directory: $path"
            ODOO_ADDONS_PATH="$path"
            break
        fi
    done
    
    # Check odoo.conf
    if [ -f "/etc/odoo/odoo.conf" ]; then
        CONF_ADDONS=$(grep "^addons_path" /etc/odoo/odoo.conf | cut -d'=' -f2 | tr ',' '\n' | head -1 | xargs)
        if [ -n "$CONF_ADDONS" ] && [ -d "$CONF_ADDONS" ]; then
            print_info "Found addons path in odoo.conf: $CONF_ADDONS"
            ODOO_ADDONS_PATH="$CONF_ADDONS"
        fi
    fi
    
    # Ask user if not found
    if [ -z "$ODOO_ADDONS_PATH" ]; then
        print_warning "Could not automatically detect Odoo addons directory."
        echo ""
        read -p "Please enter the full path to your Odoo addons directory: " USER_PATH
        
        if [ ! -d "$USER_PATH" ]; then
            print_error "Directory does not exist: $USER_PATH"
            exit 1
        fi
        
        ODOO_ADDONS_PATH="$USER_PATH"
    fi
    
    print_success "Odoo addons path: $ODOO_ADDONS_PATH"
}

# Install module
install_module() {
    print_header "Installing CJDropshipping Module"
    
    MODULE_TARGET="$ODOO_ADDONS_PATH/cjdropship"
    
    # Check if module already exists
    if [ -d "$MODULE_TARGET" ] || [ -L "$MODULE_TARGET" ]; then
        print_warning "Module already exists at: $MODULE_TARGET"
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Installation cancelled."
            exit 0
        fi
        
        print_info "Removing existing module..."
        rm -rf "$MODULE_TARGET"
    fi
    
    # Choose installation method
    echo ""
    echo "Choose installation method:"
    echo "1) Copy module (recommended for production)"
    echo "2) Create symlink (recommended for development)"
    read -p "Enter choice (1 or 2): " -n 1 -r
    echo
    
    if [[ $REPLY == "1" ]]; then
        print_info "Copying module to $MODULE_TARGET..."
        cp -r "cjdropship" "$MODULE_TARGET"
        print_success "Module copied successfully"
    elif [[ $REPLY == "2" ]]; then
        SOURCE_PATH=$(pwd)/cjdropship
        print_info "Creating symlink from $MODULE_TARGET to $SOURCE_PATH..."
        ln -s "$SOURCE_PATH" "$MODULE_TARGET"
        print_success "Symlink created successfully"
    else
        print_error "Invalid choice. Installation cancelled."
        exit 1
    fi
}

# Install Python dependencies
install_dependencies() {
    print_header "Installing Python Dependencies"
    
    if command -v pip3 &> /dev/null; then
        print_info "Installing requests library..."
        pip3 install requests --quiet || print_warning "Failed to install requests (may need sudo)"
        print_success "Dependencies installed"
    else
        print_warning "pip3 not found. Please install 'requests' manually:"
        echo "  pip3 install requests"
    fi
}

# Set permissions
set_permissions() {
    print_header "Setting Permissions"
    
    MODULE_TARGET="$ODOO_ADDONS_PATH/cjdropship"
    
    # Detect Odoo user
    ODOO_USER=""
    if id "odoo" &>/dev/null; then
        ODOO_USER="odoo"
    elif id "openerp" &>/dev/null; then
        ODOO_USER="openerp"
    fi
    
    if [ -n "$ODOO_USER" ]; then
        read -p "Set ownership to '$ODOO_USER' user? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Setting ownership to $ODOO_USER..."
            sudo chown -R "$ODOO_USER:$ODOO_USER" "$MODULE_TARGET" || print_warning "Failed to set ownership (may need sudo)"
            print_success "Permissions set"
        fi
    else
        print_warning "Odoo user not detected. Please set permissions manually if needed."
    fi
}

# Restart Odoo
restart_odoo() {
    print_header "Restarting Odoo"
    
    # Check if Odoo service exists
    if systemctl list-units --type=service | grep -q odoo; then
        read -p "Restart Odoo service now? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Restarting Odoo..."
            sudo systemctl restart odoo && print_success "Odoo restarted successfully" || print_warning "Failed to restart Odoo (may need sudo)"
        fi
    else
        print_warning "Odoo service not found."
        print_info "Please restart Odoo manually:"
        echo "  ./odoo-bin -c odoo.conf"
        echo "  or"
        echo "  sudo systemctl restart odoo"
    fi
}

# Print next steps
print_next_steps() {
    print_header "Installation Complete!"
    
    echo ""
    print_success "The CJDropshipping module has been installed successfully."
    echo ""
    print_info "Next steps:"
    echo ""
    echo "1. Open Odoo in your browser"
    echo "2. Go to Apps menu"
    echo "3. Click 'Update Apps List' (remove filters to show all apps)"
    echo "4. Search for 'CJDropshipping Integration'"
    echo "5. Click 'Install'"
    echo ""
    echo "After installation:"
    echo "- Go to: CJDropshipping > Configuration > Settings"
    echo "- Enter your API credentials"
    echo "- Test the connection"
    echo "- Start importing products!"
    echo ""
    print_info "For detailed documentation, see:"
    echo "  - README.md"
    echo "  - QUICKSTART.md"
    echo "  - INSTALLATION_GUIDE.md"
    echo ""
}

# Main installation flow
main() {
    print_header "CJDropshipping Odoo Module Installer"
    
    echo ""
    print_info "This script will install the CJDropshipping module for Odoo 19."
    print_warning "Make sure you have backed up your Odoo installation before proceeding."
    echo ""
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installation cancelled."
        exit 0
    fi
    
    check_directory
    detect_odoo
    install_module
    install_dependencies
    set_permissions
    restart_odoo
    print_next_steps
}

# Run main function
main
