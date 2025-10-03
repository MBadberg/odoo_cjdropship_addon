# CJDropshipping Odoo 19 Integration

Ein vollständiges Odoo 19 Addon für die Integration mit der CJDropshipping API.

## Features

✅ **Produktimport**: Importieren Sie Dropshipping-Produkte aus dem CJDropshipping-Katalog
✅ **Automatische Auftragserfüllung**: Senden Sie Bestellungen automatisch an CJDropshipping
✅ **Bestands- und Logistikabfragen**: Echtzeit-Bestandsabfragen und Tracking-Informationen
✅ **Webhook-Integration**: Automatische Status-Updates über Webhooks
✅ **Preisgestaltung**: Flexible Markup-Konfiguration (prozentual oder fest)
✅ **Synchronisation**: Automatische oder manuelle Produktsynchronisation

## Installation

### Voraussetzungen

- Odoo 19.0
- Python 3.10+
- `requests` Python-Bibliothek
- Aktives CJDropshipping-Konto mit API-Zugang

### Installationsschritte

1. Klonen Sie das Repository in Ihr Odoo-Addons-Verzeichnis:
```bash
cd /path/to/odoo/addons
git clone https://github.com/MBadberg/odoo_cjdropship_addon.git
```

2. Starten Sie Odoo mit dem Addon-Pfad:
```bash
./odoo-bin -c odoo.conf --addons-path=/path/to/odoo/addons,/path/to/odoo_cjdropship_addon
```

3. Aktualisieren Sie die App-Liste in Odoo:
   - Gehen Sie zu Apps
   - Klicken Sie auf "App-Liste aktualisieren"
   - Suchen Sie nach "CJDropshipping Integration"
   - Klicken Sie auf "Installieren"

## Konfiguration

### Schritt 1: API-Zugangsdaten einrichten

1. Navigieren Sie zu: **CJDropshipping > Konfiguration > Einstellungen**
2. Geben Sie Ihre CJDropshipping API-Zugangsdaten ein:
   - **API Email**: Ihre CJDropshipping Account-E-Mail
   - **API Password**: Ihr CJDropshipping Account-Passwort
3. Klicken Sie auf **"Verbindung testen"** um die Verbindung zu überprüfen

### Schritt 2: Produkteinstellungen konfigurieren

1. **Standard-Produkttyp**: Wählen Sie den Typ für importierte Produkte
2. **Standard-Kategorie**: Legen Sie eine Standard-Produktkategorie fest
3. **Preisaufschlag**: 
   - Wählen Sie zwischen prozentualer oder fester Aufschlagskalkulation
   - Geben Sie den gewünschten Aufschlag an (z.B. 30% oder 10€)

### Schritt 3: Synchronisationseinstellungen

- **Auto Sync Products**: Aktivieren Sie die automatische Produktsynchronisation
- **Sync Interval**: Legen Sie das Synchronisationsintervall in Stunden fest (Standard: 24)
- **Auto Fulfill Orders**: Aktivieren Sie die automatische Auftragsübermittlung an CJDropshipping

### Schritt 4: Webhook konfigurieren

1. Die Webhook-URL wird automatisch generiert
2. Kopieren Sie die URL aus: **CJDropshipping > Konfiguration > Einstellungen > Webhook Settings**
3. Konfigurieren Sie diese URL in Ihrem CJDropshipping-Dashboard

## Verwendung

### Produkte importieren

#### Methode 1: Import-Assistent
1. Gehen Sie zu **CJDropshipping > Konfiguration > Einstellungen**
2. Klicken Sie auf **"Produkte importieren"**
3. Konfigurieren Sie die Import-Einstellungen:
   - Seitennummer
   - Produkte pro Seite
   - Optional: Kategorie-Filter
4. Klicken Sie auf **"Produkte importieren"**

#### Methode 2: Manuelle Produktverwaltung
1. Navigieren Sie zu **CJDropshipping > Produkte > CJ Produkte**
2. Hier sehen Sie alle importierten CJ-Produkte
3. Verwenden Sie **"Odoo-Produkt erstellen/aktualisieren"** um Odoo-Produkte zu erstellen

### Bestellungen verwalten

#### Automatische Auftragserfüllung
Wenn aktiviert, werden Bestellungen mit CJDropshipping-Produkten automatisch an CJ gesendet, sobald sie bestätigt werden.

#### Manuelle Auftragsübermittlung
1. Öffnen Sie eine Verkaufsbestellung mit CJDropshipping-Produkten
2. Klicken Sie auf **"An CJDropshipping senden"**
3. Die Bestellung wird an CJ übermittelt und Sie erhalten eine Bestell-ID

#### Bestellstatus verfolgen
1. Gehen Sie zu **CJDropshipping > Bestellungen > CJ Bestellungen**
2. Öffnen Sie eine Bestellung
3. Verwenden Sie:
   - **"Status aktualisieren"**: Aktualisiert den Bestellstatus von CJ
   - **"Logistik abfragen"**: Ruft Tracking-Informationen ab

### Webhooks verwalten

Webhooks ermöglichen automatische Updates von CJDropshipping:

1. Navigieren Sie zu **CJDropshipping > Webhooks**
2. Hier sehen Sie alle empfangenen Webhook-Ereignisse
3. Webhooks werden automatisch verarbeitet und aktualisieren:
   - Bestellstatus
   - Tracking-Nummern
   - Bestandsinformationen

## Modulstruktur

```
cjdropship/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── cjdropship_api.py          # API-Client
│   ├── cjdropship_config.py       # Konfigurationsmodell
│   ├── cjdropship_product.py      # Produktmodell
│   ├── cjdropship_order.py        # Bestellmodell
│   ├── cjdropship_webhook.py      # Webhook-Modell
│   ├── sale_order.py              # Verkaufsbestellung-Erweiterung
│   └── product_template.py        # Produktvorlage-Erweiterung
├── controllers/
│   ├── __init__.py
│   └── webhook_controller.py      # Webhook-Endpunkt
├── wizards/
│   ├── __init__.py
│   ├── product_import_wizard.py   # Import-Assistent
│   └── product_import_wizard_views.xml
├── views/
│   ├── cjdropship_config_views.xml
│   ├── cjdropship_product_views.xml
│   ├── cjdropship_order_views.xml
│   ├── cjdropship_webhook_views.xml
│   └── cjdropship_menus.xml
├── security/
│   ├── cjdropship_security.xml
│   └── ir.model.access.csv
├── data/
│   └── cjdropship_data.xml
└── static/
    └── description/
        └── icon.png
```

## API-Endpunkte

### Webhook-Endpunkt
- **URL**: `https://your-odoo-domain.com/cjdropship/webhook/{config_id}`
- **Methode**: POST
- **Auth**: Public (keine Authentifizierung erforderlich)
- **Content-Type**: application/json

### Test-Endpunkt
- **URL**: `https://your-odoo-domain.com/cjdropship/webhook/test`
- **Methode**: GET
- **Beschreibung**: Überprüft, ob der Webhook-Endpunkt erreichbar ist

## Sicherheit

Das Addon implementiert zwei Benutzergruppen:

- **CJDropshipping User**: Kann Produkte und Bestellungen anzeigen und bearbeiten
- **CJDropshipping Manager**: Vollzugriff inklusive Konfiguration und Löschen von Datensätzen

## Fehlerbehebung

### Verbindung fehlgeschlagen
- Überprüfen Sie Ihre API-Zugangsdaten
- Stellen Sie sicher, dass Ihr Server CJDropshipping-API erreichen kann
- Prüfen Sie Firewall-Einstellungen

### Produktimport schlägt fehl
- Überprüfen Sie die API-Verbindung
- Prüfen Sie die Odoo-Logs für detaillierte Fehlermeldungen
- Stellen Sie sicher, dass die `requests`-Bibliothek installiert ist

### Webhook empfängt keine Daten
- Überprüfen Sie die Webhook-URL-Konfiguration in CJDropshipping
- Stellen Sie sicher, dass die URL von außen erreichbar ist
- Prüfen Sie die Firewall-Einstellungen

## Support und Beiträge

- **Issues**: https://github.com/MBadberg/odoo_cjdropship_addon/issues
- **Pull Requests**: Beiträge sind willkommen!

## Lizenz

LGPL-3

## API-Dokumentation

Weitere Informationen zur CJDropshipping API finden Sie unter:
https://developers.cjdropshipping.com/en/api/introduction.html

## Changelog

### Version 19.0.1.0.0
- Initiale Version
- Produktimport
- Automatische Auftragserfüllung
- Bestands- und Logistikabfragen
- Webhook-Integration