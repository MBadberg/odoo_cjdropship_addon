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

# Uninstall module from Odoo if already installed
uninstall_from_odoo() {
    print_header "Checking for Existing Module Installation"
    
    # Try to find odoo-bin
    ODOO_BIN=""
    POSSIBLE_ODOO_BINS=(
        "/opt/odoo/odoo-bin"
        "/usr/bin/odoo"
        "/usr/local/bin/odoo"
        "$HOME/odoo/odoo-bin"
    )
    
    for bin in "${POSSIBLE_ODOO_BINS[@]}"; do
        if [ -f "$bin" ]; then
            ODOO_BIN="$bin"
            break
        fi
    done
    
    # Try to find odoo.conf
    ODOO_CONF=""
    POSSIBLE_CONFIGS=(
        "/etc/odoo/odoo.conf"
        "/opt/odoo/odoo.conf"
        "$HOME/odoo/odoo.conf"
    )
    
    for conf in "${POSSIBLE_CONFIGS[@]}"; do
        if [ -f "$conf" ]; then
            ODOO_CONF="$conf"
            break
        fi
    done
    
    # Check if module is installed in Odoo
    if [ -n "$ODOO_BIN" ] && [ -n "$ODOO_CONF" ]; then
        print_info "Checking if module is already installed in Odoo..."
        
        # Try to check module installation status
        MODULE_INSTALLED=$(python3 -c "
try:
    import psycopg2
    import configparser
    
    config = configparser.ConfigParser()
    config.read('$ODOO_CONF')
    
    db_name = config.get('options', 'db_name', fallback=None)
    if not db_name:
        # Try to get first database
        db_host = config.get('options', 'db_host', fallback='localhost')
        db_port = config.get('options', 'db_port', fallback='5432')
        db_user = config.get('options', 'db_user', fallback='odoo')
        db_password = config.get('options', 'db_password', fallback='odoo')
        
        conn = psycopg2.connect(host=db_host, port=db_port, user=db_user, password=db_password, dbname='postgres')
        cur = conn.cursor()
        cur.execute(\"SELECT datname FROM pg_database WHERE datistemplate = false AND datname NOT IN ('postgres') ORDER BY datname LIMIT 1\")
        result = cur.fetchone()
        if result:
            db_name = result[0]
        cur.close()
        conn.close()
    
    if db_name:
        db_host = config.get('options', 'db_host', fallback='localhost')
        db_port = config.get('options', 'db_port', fallback='5432')
        db_user = config.get('options', 'db_user', fallback='odoo')
        db_password = config.get('options', 'db_password', fallback='odoo')
        
        conn = psycopg2.connect(host=db_host, port=db_port, user=db_user, password=db_password, dbname=db_name)
        cur = conn.cursor()
        cur.execute(\"SELECT state FROM ir_module_module WHERE name='cjdropship'\")
        result = cur.fetchone()
        if result and result[0] == 'installed':
            print('installed')
        cur.close()
        conn.close()
except Exception as e:
    pass
" 2>/dev/null)
        
        if [ "$MODULE_INSTALLED" = "installed" ]; then
            print_warning "Module is currently installed in Odoo database."
            read -p "Do you want to uninstall it from Odoo before reinstalling? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                print_info "Uninstalling module from Odoo..."
                
                # Get database name from config
                DB_NAME=$(python3 -c "
try:
    import configparser
    config = configparser.ConfigParser()
    config.read('$ODOO_CONF')
    db_name = config.get('options', 'db_name', fallback='')
    if db_name:
        print(db_name)
    else:
        import psycopg2
        db_host = config.get('options', 'db_host', fallback='localhost')
        db_port = config.get('options', 'db_port', fallback='5432')
        db_user = config.get('options', 'db_user', fallback='odoo')
        db_password = config.get('options', 'db_password', fallback='odoo')
        conn = psycopg2.connect(host=db_host, port=db_port, user=db_user, password=db_password, dbname='postgres')
        cur = conn.cursor()
        cur.execute(\"SELECT datname FROM pg_database WHERE datistemplate = false AND datname NOT IN ('postgres') ORDER BY datname LIMIT 1\")
        result = cur.fetchone()
        if result:
            print(result[0])
        cur.close()
        conn.close()
except:
    pass
" 2>/dev/null)
                
                if [ -n "$DB_NAME" ]; then
                    sudo -u odoo "$ODOO_BIN" -c "$ODOO_CONF" -d "$DB_NAME" -u cjdropship --uninstall 2>/dev/null || \
                    "$ODOO_BIN" -c "$ODOO_CONF" -d "$DB_NAME" -u cjdropship --uninstall 2>/dev/null || \
                    print_warning "Could not automatically uninstall. Please uninstall manually from Odoo UI."
                    
                    print_success "Module uninstalled from Odoo"
                else
                    print_warning "Could not determine database name. Please uninstall manually from Odoo UI."
                fi
            fi
        else
            print_info "Module is not currently installed in Odoo."
        fi
    else
        print_info "Could not detect Odoo installation for automatic uninstall check."
        print_info "If module is already installed in Odoo, please uninstall it manually before proceeding."
    fi
}

# Install module
install_module() {
    print_header "Installing CJDropshipping Module"
    
    MODULE_TARGET="$ODOO_ADDONS_PATH/cjdropship"
    
    # Always remove existing module if it exists (no confirmation needed)
    if [ -d "$MODULE_TARGET" ] || [ -L "$MODULE_TARGET" ]; then
        print_warning "Module already exists at: $MODULE_TARGET"
        print_info "Removing existing module..."
        rm -rf "$MODULE_TARGET"
        print_success "Existing module removed"
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
    
    # Check if requests is already installed
    if python3 -c "import requests" 2>/dev/null; then
        print_success "requests library is already installed"
        return 0
    fi
    
    # Try pip3 first
    if command -v pip3 &> /dev/null; then
        print_info "Installing requests library with pip3..."
        if pip3 install requests --quiet 2>/dev/null; then
            print_success "Dependencies installed with pip3"
            return 0
        elif sudo pip3 install requests --quiet 2>/dev/null; then
            print_success "Dependencies installed with pip3 (sudo)"
            return 0
        else
            print_warning "Failed to install with pip3, trying alternative methods..."
        fi
    else
        print_warning "pip3 not found."
    fi
    
    # Fallback to apt install if pip3 failed or is not available
    if command -v apt &> /dev/null || command -v apt-get &> /dev/null; then
        print_info "Attempting to install python3-requests via apt..."
        
        if sudo apt update -qq 2>/dev/null && sudo apt install -y python3-requests -qq 2>/dev/null; then
            print_success "Dependencies installed with apt (python3-requests)"
            return 0
        else
            print_warning "Failed to install with apt (may need sudo or internet connection)"
        fi
    fi
    
    # If all methods failed
    print_error "Could not install 'requests' library automatically."
    echo ""
    print_info "Please install it manually using one of these methods:"
    echo "  1. pip3 install requests"
    echo "  2. sudo pip3 install requests"
    echo "  3. sudo apt install python3-requests"
    echo "  4. sudo yum install python3-requests (for RedHat/CentOS)"
    echo ""
    
    read -p "Do you want to continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installation cancelled."
        exit 1
    fi
}

# Set permissions
set_permissions() {
    print_header "Setting Permissions"
    
    MODULE_TARGET="$ODOO_ADDONS_PATH/cjdropship"
    
    # Set ownership to root user
    print_info "Setting ownership to root..."
    if sudo chown -R root:root "$MODULE_TARGET" 2>/dev/null; then
        print_success "Permissions set to root:root"
    else
        print_warning "Failed to set ownership to root (may need sudo)"
        print_info "You can manually set permissions with: sudo chown -R root:root $MODULE_TARGET"
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
    print_info "For detailed documentation, see README.md"
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
    uninstall_from_odoo
    install_module
    install_dependencies
    set_permissions
    restart_odoo
    print_next_steps
}

# Run main function
main
