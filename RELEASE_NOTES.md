# Release Notes - CJDropshipping Odoo Integration

## Version 19.1.0.0.1 (2025-01-XX)

### Bugfixes
- **🔧 Kritischer Fix**: Behoben: "Invalid field 'category_id' in 'res.groups'" Fehler beim Installieren
  - Entfernt: `category_id` Feld aus res.groups (in Odoo 19 nicht mehr unterstützt)
  - Entfernt: ir.module.category Definition (in Odoo 19 obsolet)
  - Verbessert: Gruppen-Namen verwenden jetzt "/" Separator für bessere UI-Organisation
  - Kompatibilität: Vollständig kompatibel mit Odoo 19.0 und 19.1

## Version 19.1.0.0.0

### Initiale Version
- Vollständige Integration mit CJDropshipping API
- Produktimport aus dem CJDropshipping-Katalog
- Automatische Auftragserfüllung
- Bestands- und Logistikabfragen
- Webhook-Integration für automatische Status-Updates
- Community Edition Kompatibilität (Odoo 19.0 und 19.1)
- Unterstützung für Odoo 19.1 Alpha-Versionen

### Features
- ✅ **Produktverwaltung**: Import und Synchronisation von Dropshipping-Produkten
- ✅ **Bestellverwaltung**: Automatische oder manuelle Auftragsübermittlung an CJDropshipping
- ✅ **Preisgestaltung**: Flexible Markup-Konfiguration (prozentual oder fest)
- ✅ **API-Integration**: Vollständige CJDropshipping API v1 Unterstützung
- ✅ **Webhook-Support**: Echtzeit-Updates für Bestellstatus und Tracking
- ✅ **Berechtigungssystem**: Zwei Benutzergruppen (User und Manager)
- ✅ **Mehrsprachig**: Deutsche und englische Oberfläche

### Technische Details
- **Python-Abhängigkeiten**: requests
- **Odoo-Versionen**: 19.0, 19.1 (Community Edition)
- **Lizenz**: LGPL-3
- **Modelle**: 5 Haupt-Modelle (Config, Product, Order, Webhook, API)
- **Sicherheit**: Row-level und Field-level Security

### Fixes und Verbesserungen
- Enterprise-Widgets durch Community-kompatible Widgets ersetzt
- Vollständige Odoo 19.1 Alpha Kompatibilität
- Umfassende Modellverifikation
- Automatische Installations-Skripte
- Verifikations-Skripte für Installation

---

## Geplante Features (Zukünftige Versionen)

- [ ] Bulk-Import von Produkten
- [ ] Erweiterte Preis-Regeln
- [ ] Multi-Währung Support
- [ ] Inventar-Synchronisation
- [ ] Automatische Produkt-Updates
- [ ] Dashboard und Reporting
