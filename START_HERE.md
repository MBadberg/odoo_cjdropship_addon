# 🚀 START HERE - CJDropshipping Odoo Modul

## Willkommen! | Welcome!

Dies ist das CJDropshipping Integration Modul für Odoo 19.
This is the CJDropshipping Integration module for Odoo 19.

---

## 🇩🇪 Deutsche Installation (German)

### In 3 Schritten installieren:

```bash
# Schritt 1: Repository klonen (falls noch nicht geschehen)
git clone https://github.com/MBadberg/odoo_cjdropship_addon.git
cd odoo_cjdropship_addon

# Schritt 2: Automatische Installation starten
./install.sh

# Schritt 3: In Odoo installieren
# Öffnen Sie Odoo → Apps → App-Liste aktualisieren → 
# Suchen Sie "CJDropshipping Integration" → Installieren
```

### ❓ Probleme bei der Installation?

```bash
# Installation überprüfen
./verify_installation.sh
```

### 📖 Weitere Dokumentation:

- **Einfache Anleitung**: [INSTALLATION_EINFACH.md](INSTALLATION_EINFACH.md) ⭐ Empfohlen für Anfänger
- **Fehlerbehebung**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Schnellreferenz**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## 🇬🇧 English Installation

### Install in 3 steps:

```bash
# Step 1: Clone repository (if not already done)
git clone https://github.com/MBadberg/odoo_cjdropship_addon.git
cd odoo_cjdropship_addon

# Step 2: Run automated installer
./install.sh

# Step 3: Install in Odoo
# Open Odoo → Apps → Update Apps List → 
# Search "CJDropshipping Integration" → Install
```

### ❓ Having issues?

```bash
# Verify installation
./verify_installation.sh
```

### 📖 More documentation:

- **Quick Start**: [QUICKSTART.md](QUICKSTART.md) ⭐ Recommended for beginners
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Full Guide**: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

---

## ⚠️ Wichtiger Hinweis | Important Note

**Deutsch**: Nur der `cjdropship` Ordner muss ins Odoo Addons-Verzeichnis kopiert werden, nicht das gesamte Repository! Das Installations-Skript macht dies automatisch für Sie.

**English**: Only the `cjdropship` folder needs to be copied to the Odoo addons directory, not the entire repository! The installation script does this automatically for you.

---

## ✅ Was das Installations-Skript macht | What the install script does

- ✅ Findet automatisch Ihr Odoo-Verzeichnis | Automatically finds your Odoo directory
- ✅ Prüft ob Modul bereits installiert ist und bietet Deinstallation an | Checks if module is already installed and offers to uninstall
- ✅ Installiert das Modul am richtigen Ort | Installs the module in the correct location
- ✅ Installiert Python-Abhängigkeiten (pip3 oder apt) | Installs Python dependencies (pip3 or apt)
- ✅ Setzt Berechtigungen | Sets permissions
- ✅ Startet Odoo neu (optional) | Restarts Odoo (optional)

---

## 🎯 Nach der Installation | After Installation

### 1. Konfiguration | Configuration

**Deutsch**: Gehen Sie zu: **CJDropshipping → Konfiguration → Einstellungen**

**English**: Go to: **CJDropshipping → Configuration → Settings**

### 2. API-Zugangsdaten | API Credentials

- API Email: *Ihre CJDropshipping E-Mail | Your CJDropshipping email*
- API Password: *Ihr CJDropshipping Passwort | Your CJDropshipping password*

### 3. Verbindung testen | Test Connection

Klicken Sie auf "Verbindung testen" | Click "Test Connection"

### 4. Produkte importieren | Import Products

In den Einstellungen auf "Import Products" klicken
In settings, click "Import Products"

---

## 🆘 Hilfe benötigt? | Need Help?

### Automatische Diagnose | Automatic Diagnosis

```bash
./verify_installation.sh
```

Dieses Skript zeigt Ihnen genau, wo das Problem liegt.
This script shows you exactly what the problem is.

### Dokumentation | Documentation

| Deutsch | English |
|---------|---------|
| [INSTALLATION_EINFACH.md](INSTALLATION_EINFACH.md) | [QUICKSTART.md](QUICKSTART.md) |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | [DEVELOPMENT.md](DEVELOPMENT.md) |

---

## 📋 Häufige Fehler | Common Errors

| Problem | Lösung | Solution |
|---------|--------|----------|
| Modul nicht gefunden | Odoo neu starten | Restart Odoo |
| "Nicht installierbar" | `./install.sh` erneut ausführen | Run `./install.sh` again |
| requests fehlt | `pip3 install requests` | `pip3 install requests` |

---

## ✨ Features nach Installation | Features After Installation

✅ Produkte aus CJDropshipping importieren | Import products from CJDropshipping
✅ Automatische Bestellerfüllung | Automatic order fulfillment  
✅ Echtzeit-Bestandsabfragen | Real-time inventory queries
✅ Webhook-Integration | Webhook integration
✅ Preisgestaltung mit Markup | Pricing with markup
✅ Produktsynchronisation | Product synchronization

---

**Viel Erfolg! | Good luck!** 🚀
