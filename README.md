# WORK in PROGESS! Not yet working!

# CJDropshipping Odoo 19 Integration

Ein Odoo 19 Addon für die Integration mit der CJDropshipping API.

## Was macht dieses Modul?

- **Produktimport**: Importieren Sie Dropshipping-Produkte aus dem CJDropshipping-Katalog
- **Automatische Auftragserfüllung**: Senden Sie Bestellungen automatisch an CJDropshipping
- **Bestands- und Logistikabfragen**: Echtzeit-Bestandsabfragen und Tracking-Informationen
- **Webhook-Integration**: Automatische Status-Updates über Webhooks
- **Preisgestaltung**: Flexible Markup-Konfiguration (prozentual oder fest)
- **Synchronisation**: Automatische oder manuelle Produktsynchronisation

## Installation

⚠️ **Wichtig**: Nur der `cjdropship` Ordner muss ins Addons-Verzeichnis, nicht das gesamte Repository!

### Automatische Installation (Empfohlen)

```bash
# 1. Repository klonen
git clone https://github.com/MBadberg/odoo_cjdropship_addon.git
cd odoo_cjdropship_addon

# 2. Installations-Skript ausführen
./install.sh
```

### Manuelle Installation

```bash
# Repository klonen
cd /tmp
git clone https://github.com/MBadberg/odoo_cjdropship_addon.git

# Nur den cjdropship Ordner kopieren (nicht das ganze Repository!)
cp -r odoo_cjdropship_addon/cjdropship /path/to/odoo/addons/

# Abhängigkeiten installieren
pip3 install requests

# Odoo neu starten
sudo systemctl restart odoo

# Modul in Odoo installieren:
# Apps → App-Liste aktualisieren → "CJDropshipping Integration" suchen → Installieren
```

**Wichtiger Hinweis**: Die Verzeichnisstruktur muss korrekt sein:
```bash
# RICHTIG:
/path/to/odoo/addons/cjdropship/  ✅

# FALSCH:
/path/to/odoo/addons/odoo_cjdropship_addon/cjdropship/  ❌
```

## Konfiguration

1. Navigieren Sie zu: **CJDropshipping > Konfiguration > Einstellungen**
2. Geben Sie Ihre CJDropshipping API-Zugangsdaten ein
3. Klicken Sie auf **"Verbindung testen"** um die Verbindung zu überprüfen
4. Konfigurieren Sie Preisaufschlag und Synchronisationseinstellungen

## Verwendung

### Produkte importieren
- **CJDropshipping > Konfiguration > Einstellungen** → **"Produkte importieren"**
- Oder: **CJDropshipping > Produkte > CJ Produkte** → Manuell verwalten

### Bestellungen verwalten
- Automatisch: Aktivieren Sie "Auto Fulfill Orders" in den Einstellungen
- Manuell: Öffnen Sie eine Bestellung → **"An CJDropshipping senden"**

### Webhooks
- Konfigurieren Sie die Webhook-URL in Ihrem CJDropshipping-Dashboard
- Webhooks aktualisieren automatisch Bestellstatus und Tracking-Informationen

## Entwicklungsrichtlinien

**Wichtig**: Bei Änderungen am Modul dürfen KEINE zusätzlichen .md Dateien erstellt werden. Alle wichtigen Informationen gehören in diese README.md.

## Lizenz

LGPL-3
