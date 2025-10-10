# WORK in PROGESS! Not yet working!

# CJDropshipping Odoo 19 Integration

Ein Odoo 19 Addon für die Integration mit der CJDropshipping API.

## Was macht dieses Modul?

### Kernfunktionen

- **Produktimport**: Importieren Sie Dropshipping-Produkte aus dem CJDropshipping-Katalog mit Wizard-Unterstützung
- **Automatische Auftragserfüllung**: Senden Sie Bestellungen automatisch oder manuell an CJDropshipping
- **Bestands- und Logistikabfragen**: Echtzeit-Bestandsabfragen und Tracking-Informationen via API
- **Webhook-Integration**: Automatische Status-Updates für Bestellungen, Tracking und Inventar
- **Preisgestaltung**: Flexible Markup-Konfiguration (prozentual oder fest)
- **Synchronisation**: Automatische oder manuelle Produktsynchronisation mit konfigurierbaren Intervallen

### Module und Modelle

Das Addon besteht aus folgenden Hauptkomponenten:

- **cjdropship.config**: Konfiguration für API-Zugangsdaten, Synchronisationseinstellungen, Preisaufschläge und Webhooks
- **cjdropship.product**: Verwaltung importierter CJDropshipping-Produkte mit Preisen, Lagerbeständen und Versandinformationen
- **cjdropship.order**: Bestellverwaltung mit Status-Tracking, Versandmethoden und Logistics-Informationen
- **cjdropship.webhook**: Webhook-Logging und -Verarbeitung für automatische Updates
- **product.template / sale.order**: Erweiterungen der Standard-Odoo-Modelle für CJDropshipping-Integration

### API-Funktionen

Die Integration bietet vollständige API-Anbindung:

- Produktlisten und -details abrufen
- Produktvarianten und Kategorien verwalten
- Lagerbestände abfragen
- Bestellungen erstellen und abrufen
- Versandmethoden ermitteln
- Logistik- und Tracking-Informationen abfragen

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

### Grundkonfiguration

1. Navigieren Sie zu: **CJDropshipping > Konfiguration > Einstellungen**
2. Geben Sie Ihre CJDropshipping API-Zugangsdaten ein:
   - **API Email**: Ihre CJDropshipping Account-Email
   - **API Password**: Ihr CJDropshipping Account-Passwort
3. Klicken Sie auf **"Verbindung testen"** um die Verbindung zu überprüfen

### Produkteinstellungen

- **Default Product Type**: Produkttyp für importierte Artikel (Consumable/Service/Storable Product)
- **Default Product Category**: Standard-Kategorie für importierte Produkte
- **Price Markup Type**: Aufschlagsart (Fixed Amount oder Percentage)
- **Price Markup**: Aufschlagswert (z.B. 30.0 für 30% oder fester Betrag)

### Synchronisationseinstellungen

- **Auto Sync Products**: Automatische Synchronisation von Lagerbeständen und Preisen aktivieren
- **Sync Interval**: Intervall in Stunden für automatische Synchronisation (Standard: 24h)
- **Auto Fulfill Orders**: Automatisches Senden bestätigter Bestellungen an CJDropshipping

### Webhook-Konfiguration

- **Webhook Enabled**: Webhooks aktivieren/deaktivieren
- **Webhook URL**: Wird automatisch generiert (Format: `https://ihre-domain.com/cjdropship/webhook/<config_id>`)
- Diese URL muss in Ihrem CJDropshipping-Dashboard eingetragen werden für automatische Status-Updates

## Verwendung

### Produkte importieren

Es gibt mehrere Wege, Produkte zu importieren:

**Wizard-basierter Import:**
1. Navigieren Sie zu **CJDropshipping > Konfiguration > Einstellungen**
2. Klicken Sie auf **"Produkte importieren"**
3. Wählen Sie im Wizard:
   - **Configuration**: Die zu verwendende API-Konfiguration
   - **Category Filter**: (Optional) Filtern nach CJ-Kategorie
   - **Page Number**: Seitenzahl der Produktliste
   - **Products per Page**: Anzahl Produkte pro Seite (1-100, Standard: 20)
   - **Create Odoo Products Immediately**: Automatische Erstellung von Odoo-Produkten
4. Klicken Sie auf **"Import Products"**

**Manuelle Verwaltung:**
- **CJDropshipping > Produkte > CJ Produkte** → Direkte Verwaltung importierter Produkte
- Über die Listenansicht können Sie:
  - Importierte Produkte durchsuchen
  - Odoo-Produkte aus CJ-Produkten erstellen (Button "Create Odoo Product")
  - Produktinformationen aktualisieren
  - Preise und Lagerbestände synchronisieren

### Bestellungen verwalten

**Automatische Auftragserfüllung:**
1. Aktivieren Sie in den Einstellungen: **"Auto Fulfill Orders"**
2. Bestätigte Verkaufsaufträge werden automatisch an CJDropshipping gesendet
3. Status-Updates erfolgen automatisch via Webhooks

**Manuelle Auftragserfüllung:**
1. Öffnen Sie eine Verkaufsbestellung in Odoo
2. Klicken Sie auf **"An CJDropshipping senden"**
3. Das System erstellt automatisch einen CJDropshipping-Auftrag
4. Verfolgen Sie den Status unter **CJDropshipping > Bestellungen > CJ Bestellungen**

**Bestellstatus-Übersicht:**
- **Draft**: Auftrag in Vorbereitung
- **Submitted to CJ**: An CJDropshipping gesendet
- **Processing**: In Bearbeitung bei CJ
- **Shipped**: Versandt mit Tracking-Nummer
- **Delivered**: Zugestellt
- **Cancelled**: Storniert
- **Error**: Fehler aufgetreten (siehe Fehlermeldung)

### Webhooks

Webhooks ermöglichen automatische Updates von CJDropshipping:

**Konfiguration:**
1. Kopieren Sie die Webhook-URL aus den Einstellungen
2. Tragen Sie die URL in Ihrem CJDropshipping-Dashboard ein
3. Aktivieren Sie die gewünschten Event-Typen

**Unterstützte Webhook-Typen:**
- **Order Status Update**: Automatische Aktualisierung des Bestellstatus
- **Tracking Update**: Neue Tracking-Nummern und Versandstatus
- **Inventory Update**: Lagerbestandsänderungen

**Webhook-Logs anzeigen:**
- **CJDropshipping > Technisch > Webhooks** (wenn Developer-Modus aktiv)
- Zeigt alle empfangenen Webhooks mit Payload und Verarbeitungsstatus

## Technische Details

### Datenbankmodelle

**cjdropship.config** - Konfigurationsmodell
- Felder: api_email, api_password, auto_sync_products, sync_interval, auto_fulfill_orders, price_markup_type, price_markup, webhook_enabled, connection_status
- Methoden: get_api_client(), action_test_connection(), action_sync_products()

**cjdropship.product** - Produktmodell
- Felder: cj_product_id, cj_product_name, cj_product_sku, cj_variant_id, cj_price, selling_price, cj_stock_qty, shipping_weight, product_tmpl_id
- Constraint: Unique(cj_product_id, cj_variant_id)
- Methoden: action_create_odoo_product(), action_sync_from_cj(), action_bulk_create_products()

**cjdropship.order** - Bestellmodell  
- Felder: cj_order_id, cj_order_num, sale_order_id, state, tracking_number, shipping_method, shipping_cost, logistics_info
- Constraint: Unique(cj_order_id)
- Status-Workflow: draft → submitted → processing → shipped → delivered
- Methoden: action_submit_to_cj(), action_update_status(), action_query_logistics()

**cjdropship.webhook** - Webhook-Log
- Felder: webhook_type, cj_order_id, event, payload, headers, processed, error_message
- Methoden: action_process_webhook(), _process_order_status_update(), _process_tracking_update(), _process_inventory_update()

### API-Client (CJDropshippingAPI)

Die Klasse `CJDropshippingAPI` in `models/cjdropship_api.py` bietet:

**Authentifizierung:**
- Automatische Token-Verwaltung
- Token-Erneuerung bei Ablauf

**Produkt-Methoden:**
- `get_product_list(page, page_size, category_id)` - Produktliste abrufen
- `get_product_detail(product_id)` - Produktdetails abrufen
- `get_product_variant(product_id)` - Produktvarianten abrufen
- `get_product_inventory(product_id, variant_id)` - Lagerbestand abrufen
- `get_categories()` - Produktkategorien abrufen

**Bestell-Methoden:**
- `create_order(order_data)` - Bestellung erstellen
- `get_order_detail(order_id)` - Bestelldetails abrufen
- `get_order_list(page, page_size)` - Bestellliste abrufen
- `query_logistics(order_id)` - Tracking-Informationen abrufen

**Versand-Methoden:**
- `get_shipping_methods(product_list, country_code)` - Verfügbare Versandmethoden ermitteln

### Webhook-Controller

Endpoint: `/cjdropship/webhook/<config_id>`
- Methode: POST
- Content-Type: application/json
- Authentication: public (validiert config_id)
- Test-Endpoint: `/cjdropship/webhook/test` (GET)

### Sicherheit

- Zugriffskontrolle über `security/cjdropship_security.xml`
- Gruppenbasierte Berechtigungen (CJDropship User / Manager)
- Record Rules für mandantenfähigen Betrieb
- API-Credentials werden verschlüsselt in der Datenbank gespeichert

### Abhängigkeiten

**Odoo-Module:**
- base
- mail
- sale_management
- stock
- product

**Python-Pakete:**
- requests (für API-Kommunikation)

## Entwicklungsrichtlinien

**Wichtig**: Bei Änderungen am Modul dürfen KEINE zusätzlichen .md Dateien erstellt werden. Alle wichtigen Informationen gehören in diese README.md.

### Code-Qualität

- Alle Python-Dateien sind mit Pylint 10/10 bewertet
- Logging statt Print-Statements verwenden
- Docstrings für alle Funktionen und Methoden
- Maximum 5 Verschachtelungsebenen
- Zeilenlänge max. 100 Zeichen (PEP 8)

### Verifikationsskripte

Das Repository enthält Verifikationsskripte zur Code-Validierung:

- `verify_models_simple.py` - Einfache Modellprüfung (5 Hauptmodelle)
- `verify_models_comprehensive.py` - Umfassende Modellprüfung inkl. XML/CSV-Referenzen
- `verify_installation.sh` - Installationsprüfung für Odoo-Umgebungen

Ausführen vor jedem Commit:
```bash
python3 verify_models_simple.py
python3 verify_models_comprehensive.py
```

### Entwicklungssetup

**Symlink-Installation für Entwicklung:**
```bash
ln -s /pfad/zum/repo/cjdropship /pfad/zu/odoo/addons/cjdropship
```

**Modul-Update nach Code-Änderungen:**
```bash
# In Odoo
Apps > CJDropshipping Integration > Upgrade
# Oder via CLI
odoo-bin -u cjdropship -d your_database
```

## Lizenz

LGPL-3
