# Changelog & Releasenotes

Alle grundlegenden Änderungen an diesem Projekt werden in dieser Datei dokumentiert. 
Wir beibehalten eine chronologische Liste der wichtigsten Meilensteine, damit du nie den Überblick verlierst.

## [Unreleased] - Aktuell
### Hinzugefügt / Geändert / Entfernt
- Skripte `find_forms.py` und `remove_forms.py` zur Analyse und Bereinigung von Kontaktformularen implementiert.
- Kontaktformulare aus den HTML-Dateien im Verzeichnis `2.1/public/` entfernt.
- Nicht mehr benötigte Dateien und Ordner (z.B. Caches, alte Uploads, wp-includes/js/css) aus `2.1/public/` bereinigt.
---

## [1.0.0] - 2026-02-22 (Beispiel für einen Meilenstein)
### Hinzugefügt
- Initiale Version des Website Scrapings.
- Grundstruktur des Projekts aufgebaut.

<br>

---

# 🛠️ Kurzanleitung: Vorherige Git-Versionen wiederherstellen

Da du Git nutzt, speichert das System im Hintergrund jeden "Commit" (also jede gespeicherte Version deines Codes). Hier ist eine einfache Anleitung, wie du dich in der Zeit zurückbewegen kannst, wenn mal etwas kaputtgeht.

### 1. Historie ansehen (Was ist passiert?)
Öffne dein Terminal (z.B. in VS Code) im Projektordner und tippe:
```bash
git log --oneline
```
Das zeigt dir eine kurze Liste aller gespeicherten Versionen an. Ganz vorne steht immer eine **Commit-ID** (ein 7-stelliger Code, z.B. `a1b2c3d`) gefolgt von deiner Commit-Nachricht.

### 2. Eine alte Version nur "ansehen" (Gefahrlos)
Wenn du nur schauen willst, wie der Code letzte Woche aussah, kopiere die Commit-ID aus dem `git log` und tippe:
```bash
git checkout <commit-id>
# Beispiel: git checkout a1b2c3d
```
**Wie komme ich wieder zurück zum Jetzt?**
Einfach wieder den Hauptzweig auschecken:
```bash
git checkout main
# (oder 'git checkout master')
```

### 3. Nur EINE bestimmte Datei wiederherstellen
Du hast z.B. nur die Datei `index.html` kaputtgemacht und willst den Stand von gestern für diese EINE Datei?
```bash
# Holt den Zustand der Datei aus dem alten Commit zurück ins Heute:
git checkout <commit-id> -- pfad/zur/datei.html

# Danach musst du diese Änderung nur noch normal committen:
git commit -m "index.html wiederhergestellt"
```

### 4. Das KOMPLETTE Projekt auf eine alte Version zurücksetzen
**Achtung:** Wenn die neuesten Änderungen wirklich komplett gelöscht werden sollen, kannst du dein Projekt hart auf eine ältere Version zurücksetzen:
```bash
git reset --hard <commit-id>
```
*(Wichtig: Alles, was nach dieser `<commit-id>` passiert ist und nicht gepusht war, wird dauerhaft gelöscht! Nutze das nur, wenn du dir sicher bist.)*

**Die sichere Variante (Revert):**
Wenn du die fehlerhaften Änderungen behalten, aber ihre Wirkung umkehren willst (es entsteht ein neuer "Rückgängig"-Commit):
```bash
git revert <commit-id>
```

---

# 📜 Versionsverlauf (Dokumentenhistorie)

| Datum | Version | Autor | Änderung |
| :--- | :--- | :--- | :--- |
| 2026-02-22 | 1.0 | Antigravity | Initiale Erstellung (Changelog-Struktur & Git-Anleitung) |
