---
name: mobile-forensics
description: Mobile forensics techniques for SQLite database carving, plist/binary
  property list parsing, chat app extraction (Signal, WhatsApp, Telegram, iMessage,
  Messenger), cached app data recovery, and forensic report generation. Read when
  working with mobile backups, app exports, or forensic investigations.
created_at: '2026-05-15T03:00:29.031557+00:00'
updated_at: '2026-05-15T03:00:29.031557+00:00'
---

# Mobile Forensics Techniques

## SQLite Database Carving & Recovery

### Write-Ahead Log (WAL) Recovery
- SQLite WAL files (`-wal`, `-shm`) contain uncommitted and recent transactions
- Use `sqlite3 db.sqlite ".recover" > recovered.sql` for corrupted databases
- Python approach with `sqlite3.connect()` and `PRAGMA wal_checkpoint(TRUNCATE)` before extraction
- Deleted records survive in freelist pages — `PRAGMA freelist_count` to gauge recoverable data
- Carving strategy: scan raw backup/images for SQLite magic bytes `0x53514C69746520666F726D6174203300`

### Key SQLite Queries for Chat Apps
```sql
-- WhatsApp: messages with timestamps
SELECT jid.raw_string AS chat, datetime(m.timestamp/1000, 'unixepoch', 'localtime') AS time,
       CASE m.type WHEN 0 THEN m.text_data ELSE m.media_caption END AS message,
       m.latitude, m.longitude
FROM chat_view cv JOIN jid ON cv.jid_row_id = jid._id
JOIN message m ON cv.message_row_id = m._id;

-- Signal: messages from database.sqlite
SELECT c.display_name, datetime(m.date_sent/1000, 'unixepoch', 'localtime') as ts,
       m.body, m.type, m.quote_id
FROM thread t JOIN recipient c ON t.thread_recipient_id = c._id
JOIN message m ON m.thread_id = t._id
ORDER BY m.date_sent DESC;
```

### Carving Tools & Commands
- `bulk_extractor` — carve SQLite, emails, URLs from raw images
- `foremost` / `scalpel` — file header-based carving
- `strings -n 6 backup.img | grep -E '^[0-9]{10}'` — extract epoch timestamps
- Hex-level recovery: search for `CREATE TABLE` strings to locate deleted schema

## Plist (Property List) Parsing

### Formats
- **bplist00** (binary): Apple's compact format — parse with `plistlib.loads()` in Python
- **XML plist**: `<?xml version="1.0"...` — also parseable via `plistlib`
- Common locations: `Library/Preferences/`, app `Info.plist`, iOS backups `Manifest.plist`

### Python Recipe
```python
import plistlib, pathlib

def parse_any_plist(path: str) -> dict:
    data = pathlib.Path(path).read_bytes()
    # Try binary first, fallback to XML
    try:
        return plistlib.loads(data)
    except plistlib.InvalidFileException:
        import re
        xml_start = data.find(b'<?xml')
        if xml_start >= 0:
            return plistlib.loads(data[xml_start:])
    raise ValueError(f"Could not parse plist: {path}")
```

### Forensic Value
- `com.apple.MobileBackup/Manifest.plist` — backup metadata, file listing, encryption status
- `com.apple.itunesstored.plist` — purchase history
- App group containers in `group.*.plist` — shared app data across extensions

## Chat App Extraction Techniques

### iOS Backups (iTunes/Finder)
Default location: `~/Library/Application Support/MobileSync/Backup/`
- `Manifest.db` — SQLite database mapping SHA1 filenames to app domains
- Files stored as SHA1 hashes; use `Manifest.db` to resolve filenames
- Key paths:
  - WhatsApp: `ChatStorage.sqlite`, `ContactsV2.sqlite`
  - Signal: `Signal.sqlite`, `database.sqlite`
  - Telegram: `tgdata.db` (encrypted in newer versions)
  - iMessage: `chat.db` at `3d0d7e5fb2ce288813306e4d4636395e047a3d28`
  - Facebook Messenger: `lightspeed-*.db`

### Android Backups (ADB)
- Full backup: `adb backup -apk -shared -all -system -f backup.ab`
- Decrypt/convert: `dd if=backup.ab bs=24 skip=1 | zlib-flate -uncompress | tar xf -`
- Databases in `apps/<package>/db/`
- WhatsApp: `msgstore.db`, `wa.db` (contacts)
- Signal: `database` (unencrypted SQLite)
- Telegram: `cache4.db` (varies by version)

### Extraction Script Template
```python
import sqlite3, json, datetime, pathlib

class ChatExtractor:
    def __init__(self, db_path: str):
        self.db = pathlib.Path(db_path)
        self.conn = sqlite3.connect(str(self.db))
        self.conn.row_factory = sqlite3.Row

    def export_json(self, query: str, output_path: str):
        rows = [dict(r) for r in self.conn.execute(query)]
        pathlib.Path(output_path).write_text(
            json.dumps(rows, indent=2, default=str)
        )
        return len(rows)
```

## Forensic Report Structure

1. **Case Summary** — device info, backup source, scope
2. **Methodology** — tools used, carving techniques, chain of custody notes
3. **Findings by Artifact** — grouped by app/artifact type with timestamps
4. **Timeline** — reconstructed sequence of events across all sources
5. **Recovery Recommendations** — data still recoverable, tools to try next
6. **Raw Artifact Index** — file listing with hashes for verification

## Research Sources (to monitor)
- magnetforensics.com/blog
- github.com/abrignoni (iOS/Android forensics tools)
- github.com/RealityNet (WhatsApp forensics)
- sans.org/digital-forensics
- elcomsoft.com/blog
- dfir.blog
- belkasoft.com/blog
