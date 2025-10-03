# CJDropshipping Odoo Modul - Schnellreferenz

## ⚡ Installation (3 Befehle)

```bash
git clone https://github.com/MBadberg/odoo_cjdropship_addon.git
cd odoo_cjdropship_addon
./install.sh
```

Dann in Odoo: **Apps → App-Liste aktualisieren → "CJDropshipping Integration" → Installieren**

---

## 🔍 Installation überprüfen

```bash
./verify_installation.sh
```

---

## 🛠️ Häufige Befehle

### Odoo neu starten
```bash
sudo systemctl restart odoo
```

### Logs anzeigen
```bash
sudo tail -f /var/log/odoo/odoo-server.log
```

### Modul-Speicherort prüfen
```bash
ls -la /path/to/odoo/addons/cjdropship/__manifest__.py
```

### Python-Abhängigkeiten installieren
```bash
pip3 install requests
```

---

## ❌ Häufigste Fehler

### "Nicht installierbar"
**Problem**: Ganzes Repository kopiert statt nur `cjdropship/` Ordner
**Lösung**: `./install.sh` erneut ausführen

### "Modul nicht gefunden"
**Problem**: Odoo nicht neu gestartet oder App-Liste nicht aktualisiert
**Lösung**: 
```bash
sudo systemctl restart odoo
```
Dann: Apps → App-Liste aktualisieren

### "No module named 'requests'"
**Problem**: Python-Bibliothek fehlt
**Lösung**: 
```bash
pip3 install requests
sudo systemctl restart odoo
```

---

## 📂 Korrekte Struktur

✅ **RICHTIG**:
```
/path/to/odoo/addons/
└── cjdropship/
    ├── __manifest__.py
    ├── __init__.py
    └── ...
```

❌ **FALSCH**:
```
/path/to/odoo/addons/
└── odoo_cjdropship_addon/
    └── cjdropship/
        ├── __manifest__.py
        └── ...
```

---

## 🎯 Nach der Installation

### 1. Konfiguration
**CJDropshipping → Konfiguration → Einstellungen**
- API Email eingeben
- API Password eingeben
- "Verbindung testen" klicken

### 2. Erste Produkte importieren
- In Einstellungen: "Import Products" klicken
- Page Number: 1
- Products per Page: 10
- "Import Products" klicken

### 3. Produkte ansehen
**CJDropshipping → Products → CJ Products**

---

## 📞 Hilfe

| Problem | Lösung |
|---------|--------|
| Installation funktioniert nicht | `./verify_installation.sh` ausführen |
| API-Verbindung fehlgeschlagen | Zugangsdaten prüfen, Firewall prüfen |
| Import schlägt fehl | Logs prüfen: `sudo tail -f /var/log/odoo/odoo-server.log` |
| Keine Menüs sichtbar | Benutzerrechte prüfen (Verkauf, Lager) |

---

## 📖 Dokumentation

- **Einfache Anleitung**: [INSTALLATION_EINFACH.md](INSTALLATION_EINFACH.md)
- **Schnellstart**: [QUICKSTART.md](QUICKSTART.md)
- **Fehlerbehebung**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Vollständig**: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **Entwickler**: [DEVELOPMENT.md](DEVELOPMENT.md)

---

## 🔄 Update

```bash
cd /path/to/odoo_cjdropship_addon
git pull
sudo systemctl restart odoo
```

Dann in Odoo: Apps → "CJDropshipping Integration" suchen → "Upgrade" klicken

---

## ✅ Installations-Checkliste

- [ ] Repository geklont
- [ ] `./install.sh` ausgeführt
- [ ] Keine Fehler im Skript
- [ ] `./verify_installation.sh` zeigt keine Probleme
- [ ] Odoo neu gestartet
- [ ] App-Liste aktualisiert
- [ ] Modul installiert
- [ ] Menü "CJDropshipping" sichtbar
- [ ] API-Zugangsdaten konfiguriert
- [ ] Verbindungstest erfolgreich

---

**Viel Erfolg!** 🚀
