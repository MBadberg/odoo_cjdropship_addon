# CJDropshipping Modul - Fehlerbehebung

## 🔍 Automatische Diagnose

Bevor Sie manuell nach Fehlern suchen, führen Sie das Diagnose-Skript aus:

```bash
./verify_installation.sh
```

Dieses Skript zeigt Ihnen automatisch:
- ✅ Was korrekt installiert ist
- ❌ Was fehlt oder falsch konfiguriert ist
- 💡 Wie Sie Probleme beheben können

---

## 🔄 Installationsfluss-Diagramm

```
Installation starten
        ↓
    Repository klonen
        ↓
    ./install.sh ausführen  ←──┐
        ↓                       │
    Erfolgreich? ──────────────┘
        ↓ Ja
    Odoo neu starten
        ↓
    In Odoo: Apps öffnen
        ↓
    "App-Liste aktualisieren" klicken
        ↓
    Nach "CJDropshipping Integration" suchen
        ↓
    Modul gefunden?
        ↓ Nein → ./verify_installation.sh ausführen
        ↓ Ja
    Status "Installierbar"?
        ↓ Nein → Siehe Problem 1 unten
        ↓ Ja
    Auf "Installieren" klicken
        ↓
    ✅ Fertig!
```

---

## ❌ Problem 1: Modul wird nicht gefunden

**Symptom**: Das Modul "CJDropshipping Integration" erscheint nicht in der App-Liste.

### Ursache 1: App-Liste nicht aktualisiert

**Lösung**:
1. In Odoo zu **Apps** gehen
2. Auf **"App-Liste aktualisieren"** klicken (oben rechts im 3-Punkt-Menü)
3. Filter entfernen (Suche löschen, alle Filter entfernen)
4. Nach "CJDropshipping" suchen

### Ursache 2: Odoo wurde nicht neu gestartet

**Lösung**:
```bash
sudo systemctl restart odoo
# oder
./odoo-bin -c odoo.conf
```

Dann App-Liste aktualisieren (siehe oben).

### Ursache 3: Modul ist nicht im Addons-Pfad

**Diagnose**:
```bash
./verify_installation.sh
```

**Lösung**:
```bash
./install.sh
```

---

## ❌ Problem 2: Modul zeigt "Nicht installierbar"

**Symptom**: Das Modul erscheint in der Liste, aber mit Status "Nicht installierbar" (grau/deaktiviert).

### Ursache: Falsche Verzeichnisstruktur

Das **gesamte Repository** wurde kopiert, statt nur des `cjdropship` Ordners.

**Falsch** ❌:
```
/path/to/odoo/addons/
└── odoo_cjdropship_addon/        ← Repository-Ordner
    └── cjdropship/               ← Modul (zu tief!)
        ├── __manifest__.py
        └── ...
```

**Richtig** ✅:
```
/path/to/odoo/addons/
└── cjdropship/                   ← Modul direkt hier
    ├── __manifest__.py
    └── ...
```

**Lösung**:
```bash
# Falsches Modul entfernen
sudo rm -rf /path/to/odoo/addons/odoo_cjdropship_addon

# Installations-Skript verwenden (findet den richtigen Pfad automatisch)
cd /path/to/odoo_cjdropship_addon
./install.sh

# Odoo neu starten
sudo systemctl restart odoo

# In Odoo: App-Liste aktualisieren
```

---

## ❌ Problem 3: "ModuleNotFoundError: No module named 'requests'"

**Symptom**: Fehler beim Installieren oder Verwenden des Moduls.

### Ursache: Python-Abhängigkeit fehlt

**Lösung**:

Das `install.sh` Skript installiert die Abhängigkeit automatisch. Falls es manuell installiert werden muss:

```bash
# Methode 1: Mit pip3 (bevorzugt)
pip3 install requests

# Methode 2: Mit apt (wenn pip3 nicht verfügbar)
sudo apt install python3-requests

# Methode 3: Mit yum (für RedHat/CentOS)
sudo yum install python3-requests

# Odoo neu starten
sudo systemctl restart odoo
```

**Für virtuelle Umgebung**:
```bash
source /path/to/venv/bin/activate
pip install requests
```

**Hinweis**: Das Installations-Skript (`./install.sh`) versucht automatisch:
1. `requests` mit pip3 zu installieren
2. Falls pip3 nicht verfügbar ist: `python3-requests` mit apt zu installieren

---

## ❌ Problem 4: "Permission denied"

**Symptom**: Fehler beim Zugriff auf Moduldateien.

### Ursache: Falsche Dateiberechtigungen

**Lösung**:
```bash
# Berechtigungen für Odoo-Benutzer setzen
sudo chown -R odoo:odoo /path/to/odoo/addons/cjdropship

# Wenn Sie nicht wissen, wer der Odoo-Benutzer ist:
ps aux | grep odoo | head -1
# Zeigt den Benutzer in der ersten Spalte

# Dann:
sudo chown -R BENUTZER:BENUTZER /path/to/odoo/addons/cjdropship
```

---

## ❌ Problem 5: Installation erfolgt, aber keine Menüeinträge sichtbar

**Symptom**: Modul ist installiert, aber Sie sehen keine "CJDropshipping" Menüs.

### Ursache 1: Benutzerrechte fehlen

**Lösung**:
1. Gehen Sie zu **Einstellungen > Benutzer & Unternehmen > Benutzer**
2. Öffnen Sie Ihren Benutzer
3. Im Tab **"Zugriffsrechte"**:
   - Setzen Sie **"Verkauf"** auf mindestens **"Benutzer: eigene Dokumente"**
   - Setzen Sie **"Lager"** auf mindestens **"Benutzer"**
4. Speichern
5. Ausloggen und wieder einloggen

### Ursache 2: Cache-Problem

**Lösung**:
1. Browser-Cache leeren (Strg+Shift+Entf)
2. Browser neu starten
3. Erneut in Odoo einloggen

---

## ❌ Problem 6: "Connection Failed" bei API-Test

**Symptom**: Fehler beim Testen der API-Verbindung in den Einstellungen.

### Ursache 1: Falsche API-Zugangsdaten

**Lösung**:
1. Überprüfen Sie Ihre CJDropshipping-Zugangsdaten
2. Stellen Sie sicher, dass Sie die **gleichen** Daten wie für das CJDropshipping-Portal verwenden
3. Achten Sie auf Groß-/Kleinschreibung und Leerzeichen

### Ursache 2: Firewall blockiert ausgehende Verbindungen

**Lösung**:
```bash
# Test, ob HTTPS-Verbindungen funktionieren
curl -I https://developers.cjdropshipping.com

# Wenn Fehler, Firewall prüfen
sudo ufw status
sudo ufw allow out 443/tcp
```

### Ursache 3: Proxy-Einstellungen

**Lösung**:
Wenn Ihr Server einen Proxy verwendet, konfigurieren Sie ihn in der Odoo-Konfiguration.

---

## ❌ Problem 7: Produktimport schlägt fehl

**Symptom**: Fehler beim Importieren von Produkten.

### Diagnose

**Schritt 1**: Testen Sie die API-Verbindung
- Gehen Sie zu **CJDropshipping > Konfiguration > Einstellungen**
- Klicken Sie auf **"Verbindung testen"**
- Wenn das fehlschlägt, siehe Problem 6

**Schritt 2**: Prüfen Sie die Odoo-Logs
```bash
sudo tail -f /var/log/odoo/odoo-server.log
```

Führen Sie den Import erneut durch und beobachten Sie die Logs.

**Häufige Fehler**:
- `JSONDecodeError`: API antwortet nicht korrekt → CJDropshipping-Status prüfen
- `KeyError`: API-Response hat sich geändert → Modul-Update benötigt
- `Timeout`: API ist langsam → Größe reduzieren (weniger Produkte pro Seite)

---

## 🔧 Diagnose-Befehle

### Modulstruktur prüfen
```bash
ls -la /path/to/odoo/addons/cjdropship/
# Sollte __manifest__.py, __init__.py, models/, views/, etc. zeigen
```

### Odoo-Konfiguration anzeigen
```bash
cat /etc/odoo/odoo.conf | grep addons_path
```

### Modul im Addons-Pfad finden
```bash
find /usr /opt /var /home -name "cjdropship" -type d 2>/dev/null
```

### Odoo-Logs live anzeigen
```bash
sudo tail -f /var/log/odoo/odoo-server.log
```

### Odoo-Status prüfen
```bash
sudo systemctl status odoo
```

### Odoo-Service neu starten
```bash
sudo systemctl restart odoo
```

### Python-Abhängigkeiten prüfen
```bash
python3 -c "import requests; print('requests: OK')"
```

### Dateiberechtigungen prüfen
```bash
ls -la /path/to/odoo/addons/cjdropship/__manifest__.py
# Sollte lesbar sein für Odoo-Benutzer
```

---

## 📋 Installations-Checkliste

Gehen Sie diese Punkte nacheinander durch:

1. [ ] Repository wurde an einen Ort geklont (z.B. `/tmp` oder `/opt`)
2. [ ] `./install.sh` wurde ausgeführt
3. [ ] Installations-Skript hat keine Fehler gemeldet
4. [ ] `./verify_installation.sh` zeigt keine Probleme
5. [ ] Modul befindet sich in `/path/to/odoo/addons/cjdropship/` (nicht tiefer!)
6. [ ] `__manifest__.py` existiert und ist lesbar
7. [ ] Python-Bibliothek `requests` ist installiert
8. [ ] Odoo wurde neu gestartet
9. [ ] App-Liste in Odoo wurde aktualisiert
10. [ ] Modul erscheint in der App-Liste
11. [ ] Modul zeigt NICHT "Nicht installierbar"
12. [ ] Modul wurde installiert (Status: "Installiert")
13. [ ] Menüeintrag "CJDropshipping" ist sichtbar
14. [ ] Einstellungsseite ist erreichbar

Wenn alle Punkte erfüllt sind: ✅ **Installation erfolgreich!**

---

## 🆘 Weitere Hilfe

### 1. Automatische Diagnose ausführen
```bash
./verify_installation.sh
```

### 2. Detaillierte Logs prüfen
```bash
# Odoo-Logs
sudo tail -100 /var/log/odoo/odoo-server.log

# System-Logs
journalctl -u odoo -n 100
```

### 3. Modul komplett neu installieren

**Sicherer Neustart**:
```bash
# 1. Modul entfernen
sudo rm -rf /path/to/odoo/addons/cjdropship

# 2. Odoo neu starten
sudo systemctl restart odoo

# 3. Neu installieren
cd /path/to/odoo_cjdropship_addon
./install.sh

# 4. Odoo erneut neu starten
sudo systemctl restart odoo

# 5. In Odoo: App-Liste aktualisieren
```

### 4. Dokumentation konsultieren

- **Deutsch**: [INSTALLATION_EINFACH.md](INSTALLATION_EINFACH.md)
- **English**: [QUICKSTART.md](QUICKSTART.md)
- **Detailliert**: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

---

## 💡 Profi-Tipps

### Test-Installation in Docker

Wenn Sie unsicher sind, testen Sie zuerst in Docker:

```bash
# Odoo 19 in Docker starten
docker run -d -p 8069:8069 --name odoo19 odoo:19

# Modul in Container kopieren
docker cp cjdropship/ odoo19:/usr/lib/python3/dist-packages/odoo/addons/

# Container neu starten
docker restart odoo19
```

### Debug-Modus aktivieren

Für detailliertere Fehlermeldungen:

```bash
# In odoo.conf
log_level = debug

# Odoo neu starten
sudo systemctl restart odoo
```

### Modul-Entwicklungsmodus

Für Entwickler, die am Modul arbeiten:

```bash
# Modul im Entwicklungsmodus aktualisieren
./odoo-bin -c odoo.conf -u cjdropship --dev=all
```

---

## ✅ Erfolgsbeispiel

So sollte eine erfolgreiche Installation aussehen:

```bash
$ ./install.sh
==========================================
CJDropshipping Odoo Module Installer
==========================================

✓ Module structure validated
✓ Odoo addons path: /opt/odoo/addons
✓ Module copied successfully
✓ Dependencies installed
✓ Permissions set
✓ Odoo restarted successfully

==========================================
Installation Complete!
==========================================

$ ./verify_installation.sh
==========================================
CJDropshipping Module Verification
==========================================

✓ Module found at: /opt/odoo/addons/cjdropship
✓ __manifest__.py exists
✓ __manifest__.py is valid
✓ Module name: CJDropshipping Integration
✓ Version: 19.0.1.0.0
✓ installable: True
✓ All 9 data files exist
✓ Python 3 is installed
✓ requests library is installed
✓ Odoo service is running

==========================================
Diagnosis Summary
==========================================

✓ No issues found! The module appears to be correctly installed.
```

Wenn Sie diese Ausgabe sehen: **Perfekt!** 🎉
