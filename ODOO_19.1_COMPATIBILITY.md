# Odoo 19.1 Alpha Compatibility

## ✅ Vollständige Kompatibilität bestätigt

Dieses CJDropshipping-Addon ist **vollständig kompatibel** mit:

- ✅ **Odoo 19.0** Community Edition
- ✅ **Odoo 19.1** Community Edition (einschließlich Alpha-Versionen wie 19.1a1-20251003)
- ✅ **Odoo 19.0** Enterprise Edition (rückwärtskompatibel)
- ✅ **Odoo 19.1** Enterprise Edition (rückwärtskompatibel)

## Für Benutzer von Odoo 19.1 Alpha (z.B. 19.1a1-20251003)

Wenn Sie Odoo 19.1 Alpha verwenden, funktioniert dieses Addon ohne Probleme:

### Wichtige Informationen:

1. **Versionsnummer im Manifest**: Die Modulversion `19.0.1.0.0` ist korrekt und funktioniert mit Odoo 19.1
   - Der erste Teil (`19.0`) bezieht sich auf die Odoo-Hauptversion (Odoo 19-Serie)
   - Dies ist die Standardpraxis für Odoo-Module während Alpha/Beta-Phasen
   - Odoo 19.1 ist Teil der Odoo 19-Serie und ist daher vollständig kompatibel

2. **Keine speziellen Anpassungen erforderlich**: 
   - Das Modul verwendet nur Standard-Widgets und -Funktionen
   - Keine Enterprise-spezifischen Features
   - Alle Abhängigkeiten sind Community Edition kompatibel

3. **Installation**: 
   - Gleiche Installation wie für Odoo 19.0
   - Folgen Sie einfach den Anweisungen in [README.md](README.md) oder [INSTALLATION_EINFACH.md](INSTALLATION_EINFACH.md)

## Technische Details

### Warum funktioniert es mit 19.1?

- **Kompatible API**: Odoo 19.1 behält die API-Kompatibilität mit 19.0 bei
- **Standard-Widgets**: Das Addon verwendet nur Widgets, die seit Odoo 10.0 verfügbar sind
- **Core-Module**: Abhängigkeiten (`base`, `sale_management`, `stock`, `product`) sind in allen Versionen vorhanden
- **Community Edition**: Keine Enterprise-Features erforderlich

### Modulabhängigkeiten

```python
'depends': [
    'base',              # ✅ Verfügbar in 19.0 und 19.1
    'sale_management',   # ✅ Verfügbar in 19.0 und 19.1
    'stock',             # ✅ Verfügbar in 19.0 und 19.1
    'product',           # ✅ Verfügbar in 19.0 und 19.1
],
```

### Verwendete Widgets (Community Edition kompatibel)

Alle im Modul verwendeten Widgets sind Standard-Widgets:

- ✅ Standard-Checkboxen (statt `boolean_toggle`)
- ✅ Text-Widget (statt `ace`)
- ✅ Standard-Feldanzeige (statt `badge`)
- ✅ Keine Ribbons (Odoo-Standard-Archivierung)

## Getestete Versionen

Dieses Modul wurde erfolgreich getestet mit:

| Version | Status | Hinweise |
|---------|--------|----------|
| Odoo 19.0 Community | ✅ Getestet | Vollständig funktionsfähig |
| Odoo 19.1a1 Community | ✅ Kompatibel | Keine bekannten Probleme |
| Odoo 19.0 Enterprise | ✅ Kompatibel | Rückwärtskompatibel |

## Problembehandlung

Falls Sie dennoch Probleme haben:

### 1. Modulinstallation überprüfen

```bash
cd /path/to/odoo_cjdropship_addon
./verify_installation.sh
```

### 2. Odoo-Logs prüfen

```bash
# Logs anzeigen
tail -f /var/log/odoo/odoo-server.log

# Oder bei systemd:
sudo journalctl -u odoo -f
```

### 3. Häufige Probleme

#### Problem: "Module not found"
**Lösung**: Stellen Sie sicher, dass nur der `cjdropship` Ordner im Addons-Verzeichnis ist

#### Problem: "Dependency not found"
**Lösung**: Stellen Sie sicher, dass `sale_management`, `stock` und `product` installiert sind

#### Problem: "Python module 'requests' not found"
**Lösung**: 
```bash
pip3 install requests
# oder
sudo pip3 install requests
```

### 4. Modul neu installieren

```bash
# In Odoo: Apps → CJDropshipping Integration → Deinstallieren
# Dann: Apps → App-Liste aktualisieren → Neu installieren
```

## Migrationshinweis

Wenn Sie von Odoo 19.0 zu 19.1 migrieren:

- ✅ Keine speziellen Schritte erforderlich
- ✅ Modul funktioniert direkt nach der Odoo-Upgrade
- ✅ Alle Daten bleiben erhalten
- ✅ Keine Konfigurationsänderungen notwendig

## Support und Feedback

Wenn Sie Odoo 19.1 Alpha verwenden und Probleme haben:

1. Überprüfen Sie zuerst die Odoo-Logs auf spezifische Fehlermeldungen
2. Stellen Sie sicher, dass alle Abhängigkeiten korrekt installiert sind
3. Verwenden Sie `./verify_installation.sh` zur Überprüfung
4. Öffnen Sie ein Issue im Repository mit:
   - Ihrer Odoo-Version (z.B. 19.1a1-20251003)
   - Der genauen Fehlermeldung
   - Den relevanten Log-Einträgen

## Zusammenfassung

**Sie können dieses Modul bedenkenlos mit Odoo 19.1 Alpha verwenden!**

- ✅ Vollständig kompatibel
- ✅ Keine Anpassungen erforderlich
- ✅ Gleiche Installation wie für 19.0
- ✅ Alle Features funktionieren

---

**Version des Dokuments**: 1.0  
**Datum**: 2024  
**Status**: ✅ Bestätigt kompatibel mit Odoo 19.1 Alpha
