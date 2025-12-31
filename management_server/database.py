"""
Database Management for MareArts ANPR Server
SQLite database for storing detection history
"""
import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from pathlib import Path
import config


class ANPRDatabase:
    """SQLite database for ANPR detection history"""
    
    def __init__(self, db_path: Path = config.DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database schema"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    num_plates INTEGER DEFAULT 0,
                    plates TEXT,  -- JSON array of plate texts
                    confidences TEXT,  -- JSON array of confidences
                    bboxes TEXT,  -- JSON array of bounding boxes
                    processing_time REAL,
                    detector_time REAL,
                    ocr_time REAL,
                    image_path TEXT,
                    thumbnail_path TEXT,
                    success INTEGER DEFAULT 1
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON detections(timestamp DESC)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_success 
                ON detections(success)
            """)
            
            conn.commit()
    
    def add_detection(
        self,
        plates: List[str],
        confidences: List[float],
        bboxes: List[List[int]],
        processing_time: float,
        detector_time: float,
        ocr_time: float,
        image_path: Optional[str] = None,
        thumbnail_path: Optional[str] = None,
        success: bool = True
    ) -> int:
        """Add new detection to database"""
        timestamp = datetime.now().isoformat()
        
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO detections (
                    timestamp, num_plates, plates, confidences, bboxes,
                    processing_time, detector_time, ocr_time,
                    image_path, thumbnail_path, success
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp,
                len(plates),
                json.dumps(plates),
                json.dumps(confidences),
                json.dumps(bboxes),
                processing_time,
                detector_time,
                ocr_time,
                image_path,
                thumbnail_path,
                1 if success else 0
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_history(
        self,
        limit: int = 100,
        offset: int = 0,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> List[Dict]:
        """Get detection history with optional date filtering"""
        # Ensure table exists
        self.init_database()
        
        query = "SELECT * FROM detections WHERE 1=1"
        params = []
        
        if date_from:
            # Add time to include full day
            query += " AND date(timestamp) >= ?"
            params.append(date_from)
        
        if date_to:
            # Add time to include full day
            query += " AND date(timestamp) <= ?"
            params.append(date_to)
        
        query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            
            results = []
            for row in rows:
                results.append({
                    'id': row['id'],
                    'timestamp': row['timestamp'],
                    'num_plates': row['num_plates'],
                    'plates': json.loads(row['plates']) if row['plates'] else [],
                    'confidences': json.loads(row['confidences']) if row['confidences'] else [],
                    'bboxes': json.loads(row['bboxes']) if row['bboxes'] else [],
                    'processing_time': row['processing_time'],
                    'detector_time': row['detector_time'],
                    'ocr_time': row['ocr_time'],
                    'image_path': row['image_path'],
                    'thumbnail_path': row['thumbnail_path'],
                    'success': bool(row['success'])
                })
            
            return results
    
    def get_detection_by_id(self, detection_id: int) -> Optional[Dict]:
        """Get specific detection by ID"""
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM detections WHERE id = ?",
                (detection_id,)
            ).fetchone()
            
            if not row:
                return None
            
            return {
                'id': row['id'],
                'timestamp': row['timestamp'],
                'num_plates': row['num_plates'],
                'plates': json.loads(row['plates']) if row['plates'] else [],
                'confidences': json.loads(row['confidences']) if row['confidences'] else [],
                'bboxes': json.loads(row['bboxes']) if row['bboxes'] else [],
                'processing_time': row['processing_time'],
                'detector_time': row['detector_time'],
                'ocr_time': row['ocr_time'],
                'image_path': row['image_path'],
                'thumbnail_path': row['thumbnail_path'],
                'success': bool(row['success'])
            }
    
    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        with self.get_connection() as conn:
            # Ensure table exists
            self.init_database()
            
            # Total detections
            total = conn.execute(
                "SELECT COUNT(*) as count FROM detections"
            ).fetchone()['count']
            
            # Total plates detected
            total_plates = conn.execute(
                "SELECT SUM(num_plates) as total FROM detections"
            ).fetchone()['total'] or 0
            
            # Average processing time
            avg_time = conn.execute(
                "SELECT AVG(processing_time) as avg FROM detections"
            ).fetchone()['avg'] or 0
            
            # Average confidence
            confidences_rows = conn.execute(
                "SELECT confidences FROM detections WHERE confidences IS NOT NULL"
            ).fetchall()
            
            all_confidences = []
            for row in confidences_rows:
                confs = json.loads(row['confidences'])
                all_confidences.extend(confs)
            
            avg_conf = sum(all_confidences) / len(all_confidences) if all_confidences else 0
            
            # Today's count
            today = datetime.now().date().isoformat()
            today_count = conn.execute(
                "SELECT COUNT(*) as count FROM detections WHERE date(timestamp) = ?",
                (today,)
            ).fetchone()['count']
            
            # Success rate
            success_count = conn.execute(
                "SELECT COUNT(*) as count FROM detections WHERE success = 1"
            ).fetchone()['count']
            
            success_rate = (success_count / total * 100) if total > 0 else 0
            
            return {
                'total_detections': total,
                'total_plates_detected': total_plates,
                'avg_processing_time': round(avg_time, 4),
                'avg_confidence': round(avg_conf, 2),
                'today_count': today_count,
                'success_rate': round(success_rate, 2)
            }
    
    def get_daily_stats(self, days: int = 7) -> List[Dict]:
        """Get daily statistics for the last N days"""
        start_date = (datetime.now() - timedelta(days=days)).date().isoformat()
        
        with self.get_connection() as conn:
            rows = conn.execute("""
                SELECT 
                    date(timestamp) as date,
                    COUNT(*) as count,
                    SUM(num_plates) as total_plates,
                    AVG(processing_time) as avg_time
                FROM detections
                WHERE date(timestamp) >= ?
                GROUP BY date(timestamp)
                ORDER BY date DESC
            """, (start_date,)).fetchall()
            
            return [dict(row) for row in rows]
    
    def cleanup_old_entries(self, days: int = 30):
        """Remove entries older than specified days"""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with self.get_connection() as conn:
            conn.execute(
                "DELETE FROM detections WHERE timestamp < ?",
                (cutoff_date,)
            )
            conn.commit()
    
    def clear_all(self):
        """Clear all detection history (use with caution!)"""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM detections")
            conn.commit()


# Global database instance
db = ANPRDatabase()

