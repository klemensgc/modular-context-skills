#!/usr/bin/env python3
"""
WhatsApp macOS Database Extractor

Reads the ChatStorage.sqlite database from WhatsApp Desktop on macOS
and exports all chat data to a structured JSON file for analysis.

Usage:
    python extract.py                              # Export all chats
    python extract.py --shared-with "+48537990116" # Only groups shared with this person
    python extract.py --groups-only                # Only group chats
    python extract.py --db-path /path/to/db        # Custom database path
"""

import argparse
import json
import os
import shutil
import sqlite3
import tempfile
from datetime import datetime, timezone

# iOS/macOS Core Data epoch starts at 2001-01-01 00:00:00 UTC
CORE_DATA_EPOCH_OFFSET = 978307200

DEFAULT_DB_PATH = os.path.expanduser(
    "~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite"
)
DEFAULT_CONTACTS_PATH = os.path.expanduser(
    "~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ContactsV2.sqlite"
)

# Message types: 0=text, 1=image, 2=video, 3=voice, 5=location, 6=system/group event,
# 7=link, 8=document, 10=missed call, 14=deleted, 15=sticker
TEXT_TYPES = {0, 7}  # text and link previews — include message content
MEDIA_TYPES = {1: "image", 2: "video", 3: "voice", 4: "contact", 5: "location",
               8: "document", 9: "audio", 15: "sticker", 23: "poll"}
SYSTEM_TYPES = {6, 10, 14, 59, 66}


def convert_timestamp(core_data_ts):
    """Convert Core Data timestamp to ISO 8601 string."""
    if core_data_ts is None:
        return None
    unix_ts = core_data_ts + CORE_DATA_EPOCH_OFFSET
    return datetime.fromtimestamp(unix_ts, tz=timezone.utc).isoformat()


def load_contacts(contacts_path):
    """Load contact name mapping and LID→JID mapping from ContactsV2.sqlite."""
    contacts = {}
    lid_to_jid = {}
    if not os.path.exists(contacts_path):
        return contacts, lid_to_jid
    try:
        tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        tmp.close()
        shutil.copy2(contacts_path, tmp.name)
        conn = sqlite3.connect(tmp.name)
        cursor = conn.execute(
            "SELECT ZWHATSAPPID, ZFULLNAME, ZPHONENUMBER, ZLID FROM ZWAADDRESSBOOKCONTACT "
            "WHERE ZWHATSAPPID IS NOT NULL"
        )
        for jid, name, phone, lid in cursor:
            if name:
                contacts[jid] = {"name": name, "phone": phone}
            if lid:
                lid_to_jid[lid] = jid
                # Also add the contact under their LID for direct lookup
                if name:
                    contacts[lid] = {"name": name, "phone": phone}
        conn.close()
        os.unlink(tmp.name)
    except Exception as e:
        print(f"Warning: Could not read contacts database: {e}")
    return contacts, lid_to_jid


def resolve_sender(msg_row, contacts, group_members, push_names, lid_to_jid):
    """Resolve sender name from available sources.

    Priority: contacts DB (address book name) > push_names table >
    group member contact name > phone number from JID.
    Handles both regular JIDs and LIDs (Linked Identities).
    """
    is_from_me, from_jid, group_member_pk = (
        msg_row["is_from_me"], msg_row["from_jid"], msg_row["group_member_pk"]
    )

    if is_from_me:
        return "(me)"

    # Get the sender's JID — either directly or via group member FK
    sender_jid = None
    if group_member_pk and group_member_pk in group_members:
        sender_jid = group_members[group_member_pk].get("jid")
    if not sender_jid and from_jid and from_jid.endswith("@s.whatsapp.net"):
        sender_jid = from_jid

    # If sender_jid is a LID, resolve to the real JID
    if sender_jid and sender_jid.endswith("@lid"):
        sender_jid = lid_to_jid.get(sender_jid, sender_jid)

    # 1. Try contacts database (address book names — most reliable)
    if sender_jid and sender_jid in contacts:
        return contacts[sender_jid]["name"]

    # 2. Try profile push names table (WhatsApp display names)
    if sender_jid and sender_jid in push_names:
        return push_names[sender_jid]

    # 3. Try group member contact name
    if group_member_pk and group_member_pk in group_members:
        member = group_members[group_member_pk]
        if member.get("contact_name"):
            return member["contact_name"]

    # 4. Fallback: extract phone number from JID
    if sender_jid and "@" in sender_jid:
        return sender_jid.split("@")[0]

    return "(unknown)"


def extract(db_path, contacts_path, shared_with=None, groups_only=False, days=None):
    """Extract WhatsApp data from ChatStorage.sqlite."""
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        print("Make sure WhatsApp Desktop is installed and synced.")
        return None

    # Copy to temp file to avoid WAL lock conflicts
    tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
    tmp.close()
    shutil.copy2(db_path, tmp.name)
    # Also copy WAL and SHM if they exist for consistency
    for ext in ["-wal", "-shm"]:
        src = db_path + ext
        if os.path.exists(src):
            shutil.copy2(src, tmp.name + ext)

    conn = sqlite3.connect(tmp.name)
    conn.row_factory = sqlite3.Row

    # Load contacts for name resolution (also builds LID→JID mapping)
    contacts, lid_to_jid = load_contacts(contacts_path)

    # Load profile push names (WhatsApp display names)
    push_names = {}
    for row in conn.execute("SELECT ZJID, ZPUSHNAME FROM ZWAPROFILEPUSHNAME WHERE ZPUSHNAME IS NOT NULL"):
        push_names[row["ZJID"]] = row["ZPUSHNAME"]

    # Load all group members indexed by PK
    group_members = {}
    for row in conn.execute(
        "SELECT Z_PK, ZCHATSESSION, ZMEMBERJID, ZCONTACTNAME, ZFIRSTNAME, ZISACTIVE, ZISADMIN "
        "FROM ZWAGROUPMEMBER"
    ):
        group_members[row["Z_PK"]] = {
            "chat_session": row["ZCHATSESSION"],
            "jid": row["ZMEMBERJID"],
            "contact_name": row["ZCONTACTNAME"] or row["ZFIRSTNAME"],
            "is_active": row["ZISACTIVE"],
            "is_admin": row["ZISADMIN"],
        }

    # Build chat session → participants mapping
    chat_participants = {}
    for pk, member in group_members.items():
        cs = member["chat_session"]
        if cs not in chat_participants:
            chat_participants[cs] = []
        # Resolve name: contacts DB > push names > group member name > JID
        jid = member["jid"]
        # Resolve LID to real JID if possible
        resolved_jid = lid_to_jid.get(jid, jid) if jid and jid.endswith("@lid") else jid
        name = None
        if resolved_jid and resolved_jid in contacts:
            name = contacts[resolved_jid]["name"]
        if not name and jid and jid in contacts:
            name = contacts[jid]["name"]
        if not name and resolved_jid and resolved_jid in push_names:
            name = push_names[resolved_jid]
        if not name and jid and jid in push_names:
            name = push_names[jid]
        if not name:
            name = member["contact_name"]
        if not name and resolved_jid and "@" in resolved_jid:
            name = resolved_jid.split("@")[0]
        if not name and jid:
            name = jid.split("@")[0]
        chat_participants[cs].append({
            "name": name or "(unknown)",
            "jid": member["jid"],
            "is_admin": bool(member["is_admin"]),
        })

    # Determine which chat sessions to include
    chat_filter_ids = None

    if shared_with:
        # Normalize phone: strip +, spaces, dashes
        phone_normalized = shared_with.replace("+", "").replace(" ", "").replace("-", "")
        shared_jid = f"{phone_normalized}@s.whatsapp.net"

        # Find the owner's JID by looking at messages they sent
        owner_row = conn.execute(
            "SELECT ZTOJID FROM ZWAMESSAGE WHERE ZISFROMME = 1 AND ZTOJID IS NOT NULL "
            "AND ZTOJID LIKE '%@g.us' LIMIT 1"
        ).fetchone()

        # Find owner JID from group membership
        owner_jid = None
        if owner_row:
            # In group messages from me, ZTOJID is the group. Look at ZFROMJID for received messages.
            pass

        # Find groups where the shared_with person is a member
        shared_groups = set()
        for pk, member in group_members.items():
            if member["jid"] == shared_jid:
                shared_groups.add(member["chat_session"])

        if not shared_groups:
            print(f"Warning: No groups found with member {shared_with} ({shared_jid})")
            print("Falling back to all chats.")
        else:
            chat_filter_ids = shared_groups
            print(f"Found {len(shared_groups)} groups shared with {shared_with}")

    # Load chat sessions
    chats_query = """
        SELECT Z_PK, ZCONTACTJID, ZPARTNERNAME, ZMESSAGECOUNTER,
               ZLASTMESSAGEDATE, ZLASTMESSAGETEXT, ZSESSIONTYPE
        FROM ZWACHATSESSION
        WHERE ZMESSAGECOUNTER > 0
        ORDER BY ZLASTMESSAGEDATE DESC
    """
    chat_rows = conn.execute(chats_query).fetchall()

    result_chats = []
    total_messages = 0
    all_participants = set()
    date_min = None
    date_max = None

    for chat_row in chat_rows:
        chat_pk = chat_row["Z_PK"]
        contact_jid = chat_row["ZCONTACTJID"] or ""
        is_group = contact_jid.endswith("@g.us")

        if groups_only and not is_group:
            continue
        if chat_filter_ids is not None and chat_pk not in chat_filter_ids:
            continue

        chat_name = chat_row["ZPARTNERNAME"] or contact_jid.split("@")[0] or f"chat_{chat_pk}"

        # Get participants for this chat
        participants = chat_participants.get(chat_pk, [])
        for p in participants:
            all_participants.add(p["name"])

        # Load messages for this chat
        if days:
            # Filter to messages from the last N days
            from datetime import timedelta
            cutoff_ts = (datetime.now(tz=timezone.utc) - timedelta(days=days)).timestamp() - CORE_DATA_EPOCH_OFFSET
            msg_rows = conn.execute(
                """SELECT ZMESSAGEDATE, ZISFROMME, ZMESSAGETYPE, ZPUSHNAME,
                          ZFROMJID, ZTEXT, ZGROUPMEMBER, ZSTARRED
                   FROM ZWAMESSAGE
                   WHERE ZCHATSESSION = ? AND ZMESSAGEDATE >= ?
                   ORDER BY ZMESSAGEDATE ASC""",
                (chat_pk, cutoff_ts)
            ).fetchall()
        else:
            msg_rows = conn.execute(
                """SELECT ZMESSAGEDATE, ZISFROMME, ZMESSAGETYPE, ZPUSHNAME,
                          ZFROMJID, ZTEXT, ZGROUPMEMBER, ZSTARRED
                   FROM ZWAMESSAGE
                   WHERE ZCHATSESSION = ?
                   ORDER BY ZMESSAGEDATE ASC""",
                (chat_pk,)
            ).fetchall()

        messages = []
        first_msg_ts = None
        last_msg_ts = None

        for msg in msg_rows:
            ts = convert_timestamp(msg["ZMESSAGEDATE"])
            msg_type_id = msg["ZMESSAGETYPE"] or 0
            is_from_me = bool(msg["ZISFROMME"])

            # Determine message type label
            if msg_type_id in TEXT_TYPES:
                type_label = "text"
            elif msg_type_id in MEDIA_TYPES:
                type_label = MEDIA_TYPES[msg_type_id]
            elif msg_type_id in SYSTEM_TYPES:
                type_label = "system"
            else:
                type_label = f"other_{msg_type_id}"

            msg_data = {
                "is_from_me": is_from_me,
                "push_name": msg["ZPUSHNAME"],
                "from_jid": msg["ZFROMJID"],
                "group_member_pk": msg["ZGROUPMEMBER"],
            }
            sender = resolve_sender(msg_data, contacts, group_members, push_names, lid_to_jid)

            content = msg["ZTEXT"] or ""
            if type_label != "text" and type_label != "system" and not content:
                content = f"[{type_label}]"

            message_obj = {
                "timestamp": ts,
                "sender": sender,
                "is_from_me": is_from_me,
                "content": content,
                "type": type_label,
            }
            if msg["ZSTARRED"]:
                message_obj["starred"] = True

            messages.append(message_obj)

            if ts:
                if first_msg_ts is None:
                    first_msg_ts = ts
                last_msg_ts = ts
                # Track global date range
                if date_min is None or ts < date_min:
                    date_min = ts
                if date_max is None or ts > date_max:
                    date_max = ts

        total_messages += len(messages)

        chat_obj = {
            "name": chat_name,
            "jid": contact_jid,
            "is_group": is_group,
            "message_count": len(messages),
            "first_message": first_msg_ts,
            "last_message": last_msg_ts,
        }
        if is_group and participants:
            # Deduplicate participant names (same person can have JID + LID entries)
            seen_names = []
            for p in participants:
                if p["name"] not in seen_names:
                    seen_names.append(p["name"])
            chat_obj["participants"] = seen_names
        chat_obj["messages"] = messages

        result_chats.append(chat_obj)

    conn.close()
    os.unlink(tmp.name)
    for ext in ["-wal", "-shm"]:
        p = tmp.name + ext
        if os.path.exists(p):
            os.unlink(p)

    # Build final export
    export = {
        "exported_at": datetime.now(tz=timezone.utc).isoformat(),
        "date_range": {
            "from": date_min,
            "to": date_max,
        },
        "summary": {
            "total_messages": total_messages,
            "total_chats": len(result_chats),
            "total_groups": sum(1 for c in result_chats if c["is_group"]),
            "total_direct": sum(1 for c in result_chats if not c["is_group"]),
            "total_participants": len(all_participants),
        },
        "chats": result_chats,
    }

    if shared_with:
        export["filter"] = {"shared_with": shared_with}

    return export


def main():
    parser = argparse.ArgumentParser(
        description="Extract WhatsApp data from macOS Desktop database"
    )
    parser.add_argument(
        "--db-path", default=DEFAULT_DB_PATH,
        help="Path to ChatStorage.sqlite (default: WhatsApp Desktop location)"
    )
    parser.add_argument(
        "--contacts-path", default=DEFAULT_CONTACTS_PATH,
        help="Path to ContactsV2.sqlite (default: WhatsApp Desktop location)"
    )
    parser.add_argument(
        "--shared-with",
        help='Phone number to filter — only groups shared with this person (e.g. "+48537990116")'
    )
    parser.add_argument(
        "--groups-only", action="store_true",
        help="Only export group chats, skip direct messages"
    )
    parser.add_argument(
        "--days", type=int, default=None,
        help="Only export messages from the last N days (default: all)"
    )
    parser.add_argument(
        "--output", default="data/whatsapp_export.json",
        help="Output JSON file path (default: data/whatsapp_export.json)"
    )
    args = parser.parse_args()

    print(f"Reading database from: {args.db_path}")
    data = extract(args.db_path, args.contacts_path, args.shared_with, args.groups_only, args.days)

    if data is None:
        return

    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nExported to: {args.output}")
    print(f"  {data['summary']['total_chats']} chats ({data['summary']['total_groups']} groups, {data['summary']['total_direct']} direct)")
    print(f"  {data['summary']['total_messages']} messages")
    print(f"  {data['summary']['total_participants']} unique participants")
    print(f"  Date range: {data['date_range']['from'][:10] if data['date_range']['from'] else '?'} to {data['date_range']['to'][:10] if data['date_range']['to'] else '?'}")
    print(f"\nOpen this project in Claude Code and ask about your data!")


if __name__ == "__main__":
    main()
