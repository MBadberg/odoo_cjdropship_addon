# CJDropshipping Odoo 19 Integration

Ein vollständiges Odoo 19 Addon für die Integration mit der CJDropshipping API.

> **✅ COMMUNITY EDITION KOMPATIBEL!** Dieses Addon funktioniert vollständig mit Odoo Community Edition 19.0 und 19.1 (inkl. alpha). Alle Enterprise-spezifischen Widgets wurden entfernt.

> **✅ ODOO 19.1 ALPHA UNTERSTÜTZT!** Vollständige Kompatibilität mit Odoo 19.1 Alpha-Versionen (z.B. 19.1a1-20251003) bestätigt.

> **✅ ALLE MODELLE VERIFIZIERT!** Umfassende Verifikation bestätigt: Alle 5 Odoo-Modelle sind korrekt definiert und konfiguriert. Das Modul ist installationsbereit.

---

## 🚀 Schnellstart - In 3 Schritten installieren

```bash
# 1. Repository klonen
git clone https://github.com/MBadberg/odoo_cjdropship_addon.git
cd odoo_cjdropship_addon

# 2. Automatisches Installations-Skript ausführen
./install.sh

# 3. Modul in Odoo aktivieren (Apps → App-Liste aktualisieren → "CJDropshipping Integration" installieren)
```

**Probleme bei der Installation?** Führen Sie `./verify_installation.sh` aus, um die Installation zu überprüfen.

---

## Features

✅ **Produktimport**: Importieren Sie Dropshipping-Produkte aus dem CJDropshipping-Katalog
✅ **Automatische Auftragserfüllung**: Senden Sie Bestellungen automatisch an CJDropshipping
✅ **Bestands- und Logistikabfragen**: Echtzeit-Bestandsabfragen und Tracking-Informationen
✅ **Webhook-Integration**: Automatische Status-Updates über Webhooks
✅ **Preisgestaltung**: Flexible Markup-Konfiguration (prozentual oder fest)
✅ **Synchronisation**: Automatische oder manuelle Produktsynchronisation

## Installation

⚠️ **Wichtig**: Nur der `cjdropship` Ordner muss ins Addons-Verzeichnis, nicht das gesamte Repository!

### 🚀 Automatische Installation (Empfohlen)

Die einfachste und schnellste Methode:

```bash
# 1. Repository klonen
git clone https://github.com/MBadberg/odoo_cjdropship_addon.git
cd odoo_cjdropship_addon

# 2. Installations-Skript ausführen
./install.sh
```

Das Skript führt automatisch folgende Schritte aus:
- ✅ Findet Ihr Odoo Addons-Verzeichnis
- ✅ Installiert das Modul (Kopie oder Symlink)
- ✅ Installiert Python-Abhängigkeiten (`requests`)
- ✅ Setzt die richtigen Berechtigungen
- ✅ Startet Odoo neu (optional)

### 🔍 Installation überprüfen

Nachdem Sie das Modul installiert haben, überprüfen Sie die Installation:

```bash
./verify_installation.sh
```

Dieses Skript prüft:
- ✅ Ob das Modul am richtigen Ort installiert ist
- ✅ Ob alle erforderlichen Dateien vorhanden sind
- ✅ Ob Python-Abhängigkeiten installiert sind
- ✅ Ob die Modulstruktur korrekt ist

### 📋 Manuelle Installation

Falls Sie die automatische Installation nicht verwenden möchten:

#### Voraussetzungen

- Odoo 19.0 oder 19.1 (Community Edition)
- Python 3.10+
- `requests` Python-Bibliothek
- Aktives CJDropshipping-Konto mit API-Zugang

#### Schritt 1: Modul kopieren

```bash
# Repository klonen
cd /tmp
git clone https://github.com/MBadberg/odoo_cjdropship_addon.git

# Nur den cjdropship Ordner kopieren (nicht das ganze Repository!)
cp -r odoo_cjdropship_addon/cjdropship /path/to/odoo/addons/
```

#### Schritt 2: Abhängigkeiten installieren

```bash
# Mit pip3 (bevorzugt)
pip3 install requests

# Alternativ mit apt (wenn pip3 nicht verfügbar)
sudo apt install python3-requests
```

**Hinweis**: Das `install.sh` Skript installiert Abhängigkeiten automatisch.

#### Schritt 3: Odoo neu starten

```bash
sudo systemctl restart odoo
# oder
./odoo-bin -c odoo.conf
```

#### Schritt 4: Modul in Odoo installieren

1. Öffnen Sie Odoo in Ihrem Browser
2. Gehen Sie zu **Apps**
3. Klicken Sie auf **"App-Liste aktualisieren"** (ggf. Filter entfernen)
4. Suchen Sie nach **"CJDropshipping Integration"**
5. Klicken Sie auf **"Installieren"**

### ❗ Häufige Fehler

**Problem**: Modul wird als "Nicht installierbar" angezeigt

**Lösung**: Das gesamte Repository wurde kopiert, statt nur des `cjdropship` Ordners.

```bash
# FALSCH - Modul ist zu tief verschachtelt
/path/to/odoo/addons/odoo_cjdropship_addon/cjdropship/  ❌

# RICHTIG - Modul ist direkt im addons Verzeichnis
/path/to/odoo/addons/cjdropship/  ✅
```

**Lösung**: Entfernen Sie das falsch installierte Modul und führen Sie `./install.sh` aus oder kopieren Sie nur den `cjdropship` Ordner.

---

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

### Best Practices

#### Produktmanagement
- Synchronisieren Sie Produkte regelmäßig, um Preise und Bestände aktuell zu halten
- Nutzen Sie Kategorien zur Organisation Ihrer Produkte
- Prüfen Sie importierte Produkte vor der Veröffentlichung im Shop

#### Bestellverwaltung
- Aktivieren Sie automatische Auftragserfüllung für einen reibungslosen Ablauf
- Überwachen Sie Bestellstatus regelmäßig über die CJ Bestellungen-Übersicht
- Nutzen Sie Webhooks für Echtzeit-Updates

#### Performance
- Führen Sie Bulk-Operationen außerhalb der Stoßzeiten durch
- Archivieren Sie alte Webhook-Einträge regelmäßig
- Beachten Sie die API-Rate-Limits von CJDropshipping

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

## Modulverifikation

Das Modul wurde umfassend verifiziert. Sie können die Modulstruktur jederzeit selbst überprüfen:

```bash
# Einfache Verifikation (schnell)
python3 verify_models_simple.py

# Umfassende Verifikation (detailliert)
python3 verify_models_comprehensive.py
```

Beide Skripte überprüfen:
- ✅ Alle 5 Odoo-Modelle sind definiert
- ✅ Alle Modelle haben korrekte `_name` Attribute
- ✅ Alle Imports sind korrekt
- ✅ Alle XML-Referenzen sind gültig
- ✅ Alle CSV-Zugriffsrechte sind definiert

Die Verifikation bestätigt die korrekte Installation aller Komponenten.

## Fehlerbehebung

### Modul wird als "Nicht installierbar" angezeigt

**Problem**: Das Modul erscheint in der App-Liste, zeigt aber den Status "Nicht installierbar".

**Lösung**: 
1. Stellen Sie sicher, dass nur der `cjdropship` Ordner im Addons-Verzeichnis liegt, nicht das gesamte Repository
2. Die Verzeichnisstruktur sollte sein:
   ```
   /path/to/odoo/addons/
   └── cjdropship/
       ├── __init__.py
       ├── __manifest__.py
       ├── models/
       ├── views/
       └── ...
   ```
3. **NICHT** so:
   ```
   /path/to/odoo/addons/
   └── odoo_cjdropship_addon/
       └── cjdropship/
           ├── __init__.py
           └── ...
   ```
4. Starten Sie Odoo neu und aktualisieren Sie die App-Liste

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

### Python-Abhängigkeiten fehlen
Wenn `requests` nicht installiert ist:
```bash
pip3 install requests
# oder
sudo apt install python3-requests
```

### Logs überprüfen
Bei Problemen prüfen Sie die Odoo-Logs:
```bash
sudo tail -f /var/log/odoo/odoo-server.log
```

## Support und Beiträge

- **Issues**: https://github.com/MBadberg/odoo_cjdropship_addon/issues
- **Pull Requests**: Beiträge sind willkommen!

### Beiträge (Contributing)

Wir freuen uns über Beiträge zur Verbesserung dieses Addons!

#### Wie Sie beitragen können:
1. Forken Sie das Repository
2. Erstellen Sie einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Committen Sie Ihre Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Pushen Sie zum Branch (`git push origin feature/AmazingFeature`)
5. Öffnen Sie einen Pull Request

#### Code-Standards:
- Folgen Sie den Odoo-Entwicklungsrichtlinien
- Kommentieren Sie komplexen Code
- Testen Sie Ihre Änderungen gründlich
- Aktualisieren Sie die Dokumentation bei Bedarf

## Entwickler-Informationen

### Architektur

Das Addon besteht aus folgenden Hauptkomponenten:

1. **API-Client** (`cjdropship_api.py`): Handhabt alle Kommunikation mit der CJDropshipping API
2. **Konfiguration** (`cjdropship_config.py`): Speichert API-Zugangsdaten und Einstellungen
3. **Produkte** (`cjdropship_product.py`): Verwaltet importierte CJ-Produkte
4. **Bestellungen** (`cjdropship_order.py`): Verarbeitet Bestellungen an CJDropshipping
5. **Webhooks** (`cjdropship_webhook.py`): Empfängt und verarbeitet Webhook-Events

### Extension Points

Das Addon kann über folgende Mechanismen erweitert werden:

- **Modell-Vererbung**: Erweitern Sie `sale.order` oder `product.template` für zusätzliche Felder
- **API-Methoden**: Fügen Sie neue API-Endpunkte in `cjdropship_api.py` hinzu
- **Webhook-Handler**: Erweitern Sie die Webhook-Verarbeitung für zusätzliche Events
- **Wizards**: Erstellen Sie neue Assistenten für spezielle Import-/Export-Aufgaben

### Testing

```bash
# Modulstruktur prüfen
python3 verify_models_simple.py

# Detaillierte Verifikation
python3 verify_models_comprehensive.py

# Installation prüfen
./verify_installation.sh
```

## Lizenz

LGPL-3

## API-Dokumentation

Weitere Informationen zur CJDropshipping API finden Sie unter:
https://developers.cjdropshipping.com/en/api/introduction.html

## Changelog

Für detaillierte Release Notes und Changelog siehe [RELEASE_NOTES.md](RELEASE_NOTES.md).