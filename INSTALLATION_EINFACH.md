# CJDropshipping Modul - Einfache Installation (Deutsch)

## 🎯 Schnellstart - Nur 3 Schritte!

### Schritt 1: Repository herunterladen

```bash
git clone https://github.com/MBadberg/odoo_cjdropship_addon.git
cd odoo_cjdropship_addon
```

### Schritt 2: Installations-Skript ausführen

```bash
./install.sh
```

Das Skript fragt Sie nach:
- Wo Ihr Odoo installiert ist (wird meist automatisch gefunden)
- Ob Sie das Modul kopieren oder verlinken möchten
- Ob Odoo neu gestartet werden soll

**Das war's!** Das Skript macht alles automatisch.

### Schritt 3: Modul in Odoo aktivieren

1. Öffnen Sie Odoo in Ihrem Browser
2. Gehen Sie zu **Apps**
3. Klicken Sie auf **"App-Liste aktualisieren"**
4. Suchen Sie nach **"CJDropshipping Integration"**
5. Klicken Sie auf **"Installieren"**

---

## 🔍 Problem? Installation überprüfen

Wenn das Modul nicht erscheint oder als "Nicht installierbar" angezeigt wird:

```bash
./verify_installation.sh
```

Dieses Skript zeigt Ihnen genau, was das Problem ist und wie Sie es beheben.

---

## 📖 Häufige Probleme und Lösungen

### ❌ Problem 1: "Modul wird nicht in Apps angezeigt"

**Grund**: Odoo wurde nicht neu gestartet oder App-Liste nicht aktualisiert.

**Lösung**:
```bash
sudo systemctl restart odoo
```

Dann in Odoo: Apps → "App-Liste aktualisieren" klicken

---

### ❌ Problem 2: "Modul zeigt 'Nicht installierbar'"

**Grund**: Das gesamte Repository wurde kopiert, statt nur des `cjdropship` Ordners.

**Falsche Struktur**:
```
/path/to/odoo/addons/
└── odoo_cjdropship_addon/        ← Das ganze Repository (FALSCH!)
    └── cjdropship/
        ├── __manifest__.py
        └── ...
```

**Richtige Struktur**:
```
/path/to/odoo/addons/
└── cjdropship/                   ← Nur der cjdropship Ordner (RICHTIG!)
    ├── __manifest__.py
    └── ...
```

**Lösung**:
```bash
# Falsches Modul entfernen
rm -rf /path/to/odoo/addons/odoo_cjdropship_addon

# Installations-Skript erneut ausführen
./install.sh
```

---

### ❌ Problem 3: "requests Bibliothek fehlt"

**Fehlermeldung**: "No module named 'requests'"

**Lösung**:

Das Installations-Skript installiert die Bibliothek automatisch. Falls eine manuelle Installation nötig ist:

```bash
# Option 1: Mit pip3 (bevorzugt)
pip3 install requests

# Option 2: Mit apt (wenn pip3 nicht installiert ist)
sudo apt install python3-requests
```

**Hinweis**: Das `install.sh` Skript versucht automatisch beide Methoden und wählt die funktionierende aus.

Dann Odoo neu starten.

---

### ❌ Problem 4: "Keine Berechtigung zum Schreiben"

**Fehlermeldung**: "Permission denied"

**Lösung**:
```bash
# Berechtigungen setzen (ersetzen Sie /path/to/odoo/addons mit Ihrem Pfad)
sudo chown -R odoo:odoo /path/to/odoo/addons/cjdropship
```

---

## 🎓 Nach der Installation

### Konfiguration

1. Gehen Sie zu: **CJDropshipping > Konfiguration > Einstellungen**
2. Geben Sie Ihre API-Zugangsdaten ein:
   - **API Email**: Ihre CJDropshipping E-Mail
   - **API Password**: Ihr CJDropshipping Passwort
3. Klicken Sie auf **"Verbindung testen"**
4. Wenn erfolgreich, können Sie mit dem Import beginnen!

### Erster Produktimport

1. In den Einstellungen auf **"Import Products"** klicken
2. Einstellungen:
   - **Page Number**: 1
   - **Products per Page**: 10 (für den ersten Test)
   - **Create Odoo Products**: Ja
3. Klicken Sie auf **"Import Products"**
4. Warten Sie auf die Bestätigung
5. Gehen Sie zu **CJDropshipping > Products > CJ Products**

Ihre Produkte sind jetzt importiert! 🎉

---

## 📞 Weitere Hilfe benötigt?

### Dokumentation

- **Schnellstart**: Siehe `QUICKSTART.md`
- **Detaillierte Installation**: Siehe `INSTALLATION_GUIDE.md`
- **Entwickler-Doku**: Siehe `DEVELOPMENT.md`

### Kommandos zum Prüfen

```bash
# Modulstruktur prüfen
ls -l /path/to/odoo/addons/cjdropship/__manifest__.py

# Odoo-Konfiguration anzeigen
cat /etc/odoo/odoo.conf | grep addons_path

# Odoo-Logs ansehen
sudo tail -f /var/log/odoo/odoo-server.log

# Odoo-Status prüfen
sudo systemctl status odoo
```

---

## ✅ Checkliste für erfolgreiche Installation

Gehen Sie diese Punkte durch:

- [ ] Repository wurde geklont
- [ ] `install.sh` wurde ausgeführt
- [ ] Keine Fehler im Installations-Skript
- [ ] Odoo wurde neu gestartet
- [ ] App-Liste in Odoo wurde aktualisiert
- [ ] Modul "CJDropshipping Integration" erscheint in der App-Liste
- [ ] Modul zeigt NICHT "Nicht installierbar"
- [ ] Modul wurde installiert (Klick auf "Installieren")
- [ ] Konfigurationsseite ist unter "CJDropshipping > Konfiguration > Einstellungen" erreichbar

Wenn alle Punkte erfüllt sind: **Herzlichen Glückwunsch!** 🎉

---

## 💡 Profi-Tipps

### Für Entwickler: Symlink verwenden

Wenn Sie am Modul entwickeln möchten:

```bash
# Bei der Installation "2" (Symlink) wählen
./install.sh
```

Vorteile:
- ✅ Änderungen am Code sind sofort verfügbar
- ✅ Kein erneutes Kopieren nötig
- ✅ Git-Updates sind einfach (`git pull`)

### Automatische Updates

```bash
cd /opt/odoo_cjdropship_addon  # Oder wo auch immer Sie das Repo geklont haben
git pull
sudo systemctl restart odoo
```

In Odoo: Apps → Suche "CJDropshipping" → "Upgrade" klicken

---

## 🚀 Bereit zum Loslegen!

Nach erfolgreicher Installation können Sie:

- ✅ Produkte aus CJDropshipping importieren
- ✅ Automatisch Bestellungen erfüllen lassen
- ✅ Bestände synchronisieren
- ✅ Tracking-Informationen abrufen
- ✅ Webhooks für automatische Updates einrichten

Viel Erfolg mit Ihrem Dropshipping-Business! 💪
