import sqlite3
import json
from datetime import datetime
import pandas as pd
from contextlib import contextmanager
from functools import lru_cache
import os


class GrievanceDatabase:
    def __init__(self, db_path="data/grievances.db"):
        self.db_path = db_path

        # Ensure data folder exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.init_database()

    # --------------------------------------------------
    # DB CONNECTION
    # --------------------------------------------------
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    # --------------------------------------------------
    # INIT DATABASE
    # --------------------------------------------------
    def init_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS complaints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticket_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT,
                    complaint_text TEXT NOT NULL,
                    category TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    department TEXT NOT NULL,
                    sentiment_label TEXT,
                    sentiment_score REAL,
                    keywords TEXT,
                    resolution_time INTEGER,
                    status TEXT DEFAULT 'Pending',
                    submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    category TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    count INTEGER DEFAULT 1,
                    UNIQUE(date, category, priority)
                )
            """)

            # Indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_ticket ON complaints(ticket_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON complaints(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_priority ON complaints(priority)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON complaints(category)")

            conn.commit()

    # --------------------------------------------------
    # ADD COMPLAINT
    # --------------------------------------------------
    def add_complaint(self, complaint):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO complaints (
                        ticket_id, name, email, phone,
                        complaint_text, category, priority,
                        department, sentiment_label, sentiment_score,
                        keywords, resolution_time, status, submitted_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    complaint["ticket_id"],
                    complaint["name"],
                    complaint["email"],
                    complaint["phone"],
                    complaint["complaint_text"],
                    complaint["category"],
                    complaint["priority"],
                    complaint["department"],
                    complaint["sentiment_label"],
                    complaint["sentiment_score"],
                    complaint["keywords"],
                    complaint["resolution_time"],
                    complaint.get("status", "Pending"),
                    complaint["submitted_at"]
                ))

                today = datetime.now().date().isoformat()
                cursor.execute("""
                    INSERT INTO analytics (date, category, priority, count)
                    VALUES (?, ?, ?, 1)
                    ON CONFLICT(date, category, priority)
                    DO UPDATE SET count = count + 1
                """, (today, complaint["category"], complaint["priority"]))

                conn.commit()
                self.get_statistics.cache_clear()
                return True

            except sqlite3.IntegrityError:
                return False

    # --------------------------------------------------
    # GET ALL COMPLAINTS (ADMIN / DASHBOARD)
    # --------------------------------------------------
    def get_all_complaints(self, limit=500):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM complaints
                ORDER BY submitted_at DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()

        return [dict(row) for row in rows]

    # --------------------------------------------------
    # GET COMPLAINT BY TICKET (TRACKING FIXED ✅)
    # --------------------------------------------------
    def get_complaint_by_ticket(self, ticket_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM complaints WHERE ticket_id = ?",
                (ticket_id,)
            )
            row = cursor.fetchone()

        if not row:
            return None

        return dict(row)

    # --------------------------------------------------
    # UPDATE STATUS (ADMIN)
    # --------------------------------------------------
    def update_complaint_status(self, ticket_id, new_status):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE complaints
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE ticket_id = ?
            """, (new_status, ticket_id))
            conn.commit()
            self.get_statistics.cache_clear()

        return cursor.rowcount > 0

    # --------------------------------------------------
    # STATISTICS (DASHBOARD)
    # --------------------------------------------------
    @lru_cache(maxsize=1)
    def get_statistics(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            stats = {}

            cursor.execute("SELECT COUNT(*) FROM complaints")
            stats["total_complaints"] = cursor.fetchone()[0]

            cursor.execute("SELECT status, COUNT(*) FROM complaints GROUP BY status")
            stats["by_status"] = dict(cursor.fetchall())

            cursor.execute("SELECT category, COUNT(*) FROM complaints GROUP BY category")
            stats["by_category"] = dict(cursor.fetchall())

            cursor.execute("SELECT priority, COUNT(*) FROM complaints GROUP BY priority")
            stats["by_priority"] = dict(cursor.fetchall())

            cursor.execute("""
                SELECT date, count FROM analytics
                ORDER BY date ASC
            """)
            stats["recent_trend"] = dict(cursor.fetchall())

        return stats

    # --------------------------------------------------
    # SEARCH (OPTIONAL)
    # --------------------------------------------------
    def search_complaints(self, query):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM complaints
                WHERE complaint_text LIKE ? OR ticket_id LIKE ?
                ORDER BY submitted_at DESC
                LIMIT 50
            """, (f"%{query}%", f"%{query}%"))
            rows = cursor.fetchall()

        return [dict(row) for row in rows]

    # --------------------------------------------------
    # DELETE ALL (ADMIN ONLY)
    # --------------------------------------------------
    def delete_all_complaints(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM complaints")
            cursor.execute("DELETE FROM analytics")
            conn.commit()
            self.get_statistics.cache_clear()
