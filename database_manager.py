"""
🗄️ D64 Converter - Database Manager
=======================================
İşlenmiş dosyalar için Excel-style veritabanı sistemi
Dosya işlem geçmişi, format dönüşüm sonuçları ve istatistikleri takip eder.

Features:
- SQLite veritabanı
- Excel export/import
- JSON export
- İstatistik raporları
- Dosya hash tracking
- Format başarı oranları
"""

import sqlite3
import json
import os
import hashlib
import datetime
from typing import Dict, List, Optional, Tuple
import csv

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

class DatabaseManager:
    """İşlenmiş dosyalar için veritabanı yöneticisi"""
    
    def __init__(self, db_path: str = "logs/processed_files.db"):
        """
        Database Manager başlatma
        
        Args:
            db_path: SQLite veritabanı dosya yolu
        """
        self.db_path = db_path
        self.ensure_database_dir()
        self.init_database()
    
    def ensure_database_dir(self):
        """Veritabanı dizinini oluştur"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def init_database(self):
        """Veritabanı tablolarını oluştur"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Ana dosya tablosu
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processed_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_hash TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    source_format TEXT NOT NULL,
                    start_address INTEGER,
                    end_address INTEGER,
                    processing_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    success_count INTEGER DEFAULT 0,
                    failure_count INTEGER DEFAULT 0,
                    last_processed DATETIME DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    UNIQUE(file_hash)
                )
            """)
            
            # Format dönüşüm sonuçları
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS format_conversions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_id INTEGER,
                    target_format TEXT NOT NULL,
                    assembly_format TEXT,
                    success BOOLEAN NOT NULL,
                    output_size INTEGER,
                    processing_time REAL,
                    error_message TEXT,
                    output_path TEXT,
                    conversion_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (file_id) REFERENCES processed_files (id)
                )
            """)
            
            # İstatistik özeti
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stat_type TEXT NOT NULL,
                    stat_key TEXT NOT NULL,
                    stat_value REAL NOT NULL,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(stat_type, stat_key)
                )
            """)
            
            conn.commit()
    
    def calculate_file_hash(self, file_path: str) -> str:
        """Dosya hash'i hesapla"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""
    
    def add_processed_file(self, filename: str, file_path: str, 
                          source_format: str, start_address: int = None, 
                          end_address: int = None, notes: str = "") -> int:
        """İşlenmiş dosyayı veritabanına ekle"""
        
        file_hash = self.calculate_file_hash(file_path)
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Mevcut dosyayı kontrol et
            cursor.execute("SELECT id FROM processed_files WHERE file_hash = ?", (file_hash,))
            existing = cursor.fetchone()
            
            if existing:
                # Mevcut dosyayı güncelle
                cursor.execute("""
                    UPDATE processed_files 
                    SET last_processed = CURRENT_TIMESTAMP, notes = ?
                    WHERE id = ?
                """, (notes, existing[0]))
                return existing[0]
            else:
                # Yeni dosya ekle
                cursor.execute("""
                    INSERT INTO processed_files 
                    (filename, file_path, file_hash, file_size, source_format, 
                     start_address, end_address, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (filename, file_path, file_hash, file_size, source_format,
                     start_address, end_address, notes))
                
                return cursor.lastrowid
    
    def add_format_conversion(self, file_id: int, target_format: str, 
                            success: bool, output_size: int = 0,
                            processing_time: float = 0.0, error_message: str = "",
                            output_path: str = "", assembly_format: str = ""):
        """Format dönüşüm sonucu ekle"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO format_conversions 
                (file_id, target_format, assembly_format, success, output_size,
                 processing_time, error_message, output_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (file_id, target_format, assembly_format, success, output_size,
                 processing_time, error_message, output_path))
            
            # Ana dosya tablosundaki sayaçları güncelle
            if success:
                cursor.execute("""
                    UPDATE processed_files 
                    SET success_count = success_count + 1,
                        last_processed = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (file_id,))
            else:
                cursor.execute("""
                    UPDATE processed_files 
                    SET failure_count = failure_count + 1,
                        last_processed = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (file_id,))
    
    def get_file_history(self, filename: str = None, file_hash: str = None) -> List[Dict]:
        """Dosya işlem geçmişini getir"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if file_hash:
                query = """
                    SELECT pf.*, 
                           GROUP_CONCAT(fc.target_format || ':' || fc.success) as conversions
                    FROM processed_files pf
                    LEFT JOIN format_conversions fc ON pf.id = fc.file_id
                    WHERE pf.file_hash = ?
                    GROUP BY pf.id
                """
                cursor.execute(query, (file_hash,))
            elif filename:
                query = """
                    SELECT pf.*, 
                           GROUP_CONCAT(fc.target_format || ':' || fc.success) as conversions
                    FROM processed_files pf
                    LEFT JOIN format_conversions fc ON pf.id = fc.file_id
                    WHERE pf.filename LIKE ?
                    GROUP BY pf.id
                """
                cursor.execute(query, (f"%{filename}%",))
            else:
                query = """
                    SELECT pf.*, 
                           GROUP_CONCAT(fc.target_format || ':' || fc.success) as conversions
                    FROM processed_files pf
                    LEFT JOIN format_conversions fc ON pf.id = fc.file_id
                    GROUP BY pf.id
                    ORDER BY pf.last_processed DESC
                """
                cursor.execute(query)
            
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                row_dict = dict(zip(columns, row))
                results.append(row_dict)
            
            return results
    
    def get_statistics(self) -> Dict:
        """İstatistikleri getir"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Toplam dosya sayısı
            cursor.execute("SELECT COUNT(*) FROM processed_files")
            stats['total_files'] = cursor.fetchone()[0]
            
            # Format başarı oranları
            cursor.execute("""
                SELECT target_format, 
                       SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count,
                       COUNT(*) as total_count,
                       ROUND(AVG(CASE WHEN success = 1 THEN 1.0 ELSE 0.0 END) * 100, 2) as success_rate
                FROM format_conversions 
                GROUP BY target_format
            """)
            
            format_stats = {}
            for row in cursor.fetchall():
                format_name, success_count, total_count, success_rate = row
                format_stats[format_name] = {
                    'success_count': success_count,
                    'total_count': total_count,
                    'success_rate': success_rate
                }
            
            stats['format_stats'] = format_stats
            
            # Assembly format istatistikleri
            cursor.execute("""
                SELECT assembly_format, 
                       SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count,
                       COUNT(*) as total_count
                FROM format_conversions 
                WHERE assembly_format IS NOT NULL AND assembly_format != ''
                GROUP BY assembly_format
            """)
            
            assembly_stats = {}
            for row in cursor.fetchall():
                asm_format, success_count, total_count = row
                assembly_stats[asm_format] = {
                    'success_count': success_count,
                    'total_count': total_count
                }
            
            stats['assembly_stats'] = assembly_stats
            
            # Son işlenen dosyalar
            cursor.execute("""
                SELECT filename, processing_date, success_count, failure_count
                FROM processed_files 
                ORDER BY last_processed DESC 
                LIMIT 10
            """)
            
            recent_files = []
            for row in cursor.fetchall():
                recent_files.append({
                    'filename': row[0],
                    'processing_date': row[1],
                    'success_count': row[2],
                    'failure_count': row[3]
                })
            
            stats['recent_files'] = recent_files
            
            return stats
    
    def export_to_excel(self, output_path: str) -> bool:
        """Excel formatında dışa aktar"""
        
        if not PANDAS_AVAILABLE:
            print("⚠️ pandas kütüphanesi bulunamadı - Excel export edilemiyor")
            return False
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Ana dosya tablosu
                files_df = pd.read_sql_query("""
                    SELECT filename, file_path, file_size, source_format, 
                           start_address, end_address, processing_date,
                           success_count, failure_count, last_processed, notes
                    FROM processed_files 
                    ORDER BY last_processed DESC
                """, conn)
                
                # Format dönüşümleri
                conversions_df = pd.read_sql_query("""
                    SELECT pf.filename, fc.target_format, fc.assembly_format,
                           fc.success, fc.output_size, fc.processing_time,
                           fc.error_message, fc.conversion_date
                    FROM format_conversions fc
                    JOIN processed_files pf ON fc.file_id = pf.id
                    ORDER BY fc.conversion_date DESC
                """, conn)
            
            # Excel yazma
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                files_df.to_excel(writer, sheet_name='Processed Files', index=False)
                conversions_df.to_excel(writer, sheet_name='Format Conversions', index=False)
                
                # İstatistik sayfası
                stats = self.get_statistics()
                stats_data = []
                
                for format_name, format_stat in stats.get('format_stats', {}).items():
                    stats_data.append({
                        'Format': format_name,
                        'Success Count': format_stat['success_count'],
                        'Total Count': format_stat['total_count'],
                        'Success Rate %': format_stat['success_rate']
                    })
                
                if stats_data:
                    stats_df = pd.DataFrame(stats_data)
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)
            
            return True
            
        except Exception as e:
            print(f"❌ Excel export hatası: {e}")
            return False
    
    def export_to_csv(self, output_dir: str) -> bool:
        """CSV formatında dışa aktar"""
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Processed files CSV
                cursor.execute("""
                    SELECT filename, file_path, file_size, source_format, 
                           start_address, end_address, processing_date,
                           success_count, failure_count, last_processed, notes
                    FROM processed_files 
                    ORDER BY last_processed DESC
                """)
                
                with open(os.path.join(output_dir, 'processed_files.csv'), 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Filename', 'File Path', 'File Size', 'Source Format',
                                   'Start Address', 'End Address', 'Processing Date',
                                   'Success Count', 'Failure Count', 'Last Processed', 'Notes'])
                    writer.writerows(cursor.fetchall())
                
                # Format conversions CSV
                cursor.execute("""
                    SELECT pf.filename, fc.target_format, fc.assembly_format,
                           fc.success, fc.output_size, fc.processing_time,
                           fc.error_message, fc.conversion_date
                    FROM format_conversions fc
                    JOIN processed_files pf ON fc.file_id = pf.id
                    ORDER BY fc.conversion_date DESC
                """)
                
                with open(os.path.join(output_dir, 'format_conversions.csv'), 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Filename', 'Target Format', 'Assembly Format',
                                   'Success', 'Output Size', 'Processing Time',
                                   'Error Message', 'Conversion Date'])
                    writer.writerows(cursor.fetchall())
            
            return True
            
        except Exception as e:
            print(f"❌ CSV export hatası: {e}")
            return False
    
    def export_to_json(self, output_path: str) -> bool:
        """JSON formatında dışa aktar"""
        
        try:
            data = {
                'export_date': datetime.datetime.now().isoformat(),
                'statistics': self.get_statistics(),
                'files': self.get_file_history()
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"❌ JSON export hatası: {e}")
            return False
    
    def cleanup_old_records(self, days: int = 30) -> int:
        """Eski kayıtları temizle"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 30 günden eski kayıtları sil
            cursor.execute("""
                DELETE FROM format_conversions 
                WHERE conversion_date < datetime('now', '-{} days')
            """.format(days))
            
            deleted_conversions = cursor.rowcount
            
            cursor.execute("""
                DELETE FROM processed_files 
                WHERE processing_date < datetime('now', '-{} days')
                AND id NOT IN (SELECT DISTINCT file_id FROM format_conversions)
            """.format(days))
            
            deleted_files = cursor.rowcount
            
            return deleted_conversions + deleted_files
    
    def search_files(self, search_term: str, search_type: str = "filename") -> List[Dict]:
        """Dosya arama"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if search_type == "filename":
                query = """
                    SELECT * FROM processed_files 
                    WHERE filename LIKE ?
                    ORDER BY last_processed DESC
                """
                cursor.execute(query, (f"%{search_term}%",))
            elif search_type == "format":
                query = """
                    SELECT DISTINCT pf.* FROM processed_files pf
                    JOIN format_conversions fc ON pf.id = fc.file_id
                    WHERE fc.target_format LIKE ?
                    ORDER BY pf.last_processed DESC
                """
                cursor.execute(query, (f"%{search_term}%",))
            elif search_type == "notes":
                query = """
                    SELECT * FROM processed_files 
                    WHERE notes LIKE ?
                    ORDER BY last_processed DESC
                """
                cursor.execute(query, (f"%{search_term}%",))
            
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                row_dict = dict(zip(columns, row))
                results.append(row_dict)
            
            return results

# Test fonksiyonu
if __name__ == "__main__":
    print("🗄️ D64 Converter Database Manager Test")
    print("=" * 50)
    
    db = DatabaseManager()
    
    # Test data
    file_id = db.add_processed_file(
        filename="test.prg",
        file_path="test_files/test.prg",
        source_format="PRG",
        start_address=0x0801,
        end_address=0x1000,
        notes="Test dosyası"
    )
    
    print(f"✅ Dosya eklendi: ID {file_id}")
    
    # Format dönüşüm testi
    db.add_format_conversion(
        file_id=file_id,
        target_format="ASM",
        assembly_format="ACME",
        success=True,
        output_size=1024,
        processing_time=0.5
    )
    
    print("✅ Format dönüşümü eklendi")
    
    # İstatistikleri görüntüle
    stats = db.get_statistics()
    print(f"📊 Toplam dosya: {stats['total_files']}")
    print(f"📊 Format istatistikleri: {stats['format_stats']}")
    
    print("✅ Database Manager test tamamlandı")
