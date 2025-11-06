"""
Database models and setup for Hotel Management System
"""
import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple


class Database:
    """Database manager for hotel management system"""
    
    def __init__(self, db_name: str = "hotel.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        """Create all necessary database tables"""
        cursor = self.conn.cursor()
        
        # Rooms table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT UNIQUE NOT NULL,
                room_type TEXT NOT NULL,
                price_per_night REAL NOT NULL,
                capacity INTEGER NOT NULL,
                amenities TEXT,
                status TEXT DEFAULT 'available' CHECK(status IN ('available', 'occupied', 'maintenance'))
            )
        """)
        
        # Guests table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guests (
                guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT NOT NULL,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Reservations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                guest_id INTEGER NOT NULL,
                room_id INTEGER NOT NULL,
                check_in_date DATE NOT NULL,
                check_out_date DATE NOT NULL,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled')),
                total_amount REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (guest_id) REFERENCES guests(guest_id),
                FOREIGN KEY (room_id) REFERENCES rooms(room_id)
            )
        """)
        
        # Payments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                reservation_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT NOT NULL,
                payment_status TEXT DEFAULT 'pending' CHECK(payment_status IN ('pending', 'completed', 'refunded')),
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (reservation_id) REFERENCES reservations(reservation_id)
            )
        """)
        
        self.conn.commit()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Execute a SELECT query and return results"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT, UPDATE, or DELETE query and return last row id"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor.lastrowid
    
    def close(self):
        """Close database connection"""
        self.conn.close()


class Room:
    """Room model"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def add_room(self, room_number: str, room_type: str, price_per_night: float, 
                 capacity: int, amenities: str = "", status: str = "available") -> int:
        """Add a new room to the database"""
        query = """
            INSERT INTO rooms (room_number, room_type, price_per_night, capacity, amenities, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        return self.db.execute_update(query, (room_number, room_type, price_per_night, capacity, amenities, status))
    
    def get_all_rooms(self) -> List[sqlite3.Row]:
        """Get all rooms"""
        return self.db.execute_query("SELECT * FROM rooms ORDER BY room_number")
    
    def get_available_rooms(self, check_in: str, check_out: str) -> List[sqlite3.Row]:
        """Get available rooms for given dates"""
        query = """
            SELECT r.* FROM rooms r
            WHERE r.status = 'available'
            AND r.room_id NOT IN (
                SELECT room_id FROM reservations
                WHERE status IN ('confirmed', 'checked_in')
                AND (
                    (check_in_date <= ? AND check_out_date > ?) OR
                    (check_in_date < ? AND check_out_date >= ?) OR
                    (check_in_date >= ? AND check_out_date <= ?)
                )
            )
            ORDER BY r.room_number
        """
        return self.db.execute_query(query, (check_in, check_in, check_out, check_out, check_in, check_out))
    
    def get_room_by_id(self, room_id: int) -> Optional[sqlite3.Row]:
        """Get room by ID"""
        result = self.db.execute_query("SELECT * FROM rooms WHERE room_id = ?", (room_id,))
        return result[0] if result else None
    
    def update_room_status(self, room_id: int, status: str):
        """Update room status"""
        query = "UPDATE rooms SET status = ? WHERE room_id = ?"
        self.db.execute_update(query, (status, room_id))


class Guest:
    """Guest model"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def add_guest(self, name: str, phone: str, email: str = "", address: str = "") -> int:
        """Add a new guest"""
        query = """
            INSERT INTO guests (name, email, phone, address)
            VALUES (?, ?, ?, ?)
        """
        return self.db.execute_update(query, (name, email, phone, address))
    
    def get_guest_by_id(self, guest_id: int) -> Optional[sqlite3.Row]:
        """Get guest by ID"""
        result = self.db.execute_query("SELECT * FROM guests WHERE guest_id = ?", (guest_id,))
        return result[0] if result else None
    
    def get_guest_by_phone(self, phone: str) -> Optional[sqlite3.Row]:
        """Get guest by phone number"""
        result = self.db.execute_query("SELECT * FROM guests WHERE phone = ?", (phone,))
        return result[0] if result else None
    
    def get_all_guests(self) -> List[sqlite3.Row]:
        """Get all guests"""
        return self.db.execute_query("SELECT * FROM guests ORDER BY name")


class Reservation:
    """Reservation model"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def create_reservation(self, guest_id: int, room_id: int, check_in_date: str, 
                          check_out_date: str, total_amount: float) -> int:
        """Create a new reservation"""
        query = """
            INSERT INTO reservations (guest_id, room_id, check_in_date, check_out_date, total_amount, status)
            VALUES (?, ?, ?, ?, ?, 'confirmed')
        """
        return self.db.execute_update(query, (guest_id, room_id, check_in_date, check_out_date, total_amount))
    
    def get_reservation_by_id(self, reservation_id: int) -> Optional[sqlite3.Row]:
        """Get reservation by ID"""
        query = """
            SELECT r.*, g.name as guest_name, g.phone as guest_phone,
                   rm.room_number, rm.room_type, rm.price_per_night
            FROM reservations r
            JOIN guests g ON r.guest_id = g.guest_id
            JOIN rooms rm ON r.room_id = rm.room_id
            WHERE r.reservation_id = ?
        """
        result = self.db.execute_query(query, (reservation_id,))
        return result[0] if result else None
    
    def get_all_reservations(self) -> List[sqlite3.Row]:
        """Get all reservations"""
        query = """
            SELECT r.*, g.name as guest_name, g.phone as guest_phone,
                   rm.room_number, rm.room_type
            FROM reservations r
            JOIN guests g ON r.guest_id = g.guest_id
            JOIN rooms rm ON r.room_id = rm.room_id
            ORDER BY r.created_at DESC
        """
        return self.db.execute_query(query)
    
    def update_reservation_status(self, reservation_id: int, status: str):
        """Update reservation status"""
        query = "UPDATE reservations SET status = ? WHERE reservation_id = ?"
        self.db.execute_update(query, (status, reservation_id))
    
    def check_in(self, reservation_id: int):
        """Check in a guest"""
        self.update_reservation_status(reservation_id, "checked_in")
        reservation = self.get_reservation_by_id(reservation_id)
        if reservation:
            Room(self.db).update_room_status(reservation['room_id'], 'occupied')
    
    def check_out(self, reservation_id: int):
        """Check out a guest"""
        self.update_reservation_status(reservation_id, "checked_out")
        reservation = self.get_reservation_by_id(reservation_id)
        if reservation:
            Room(self.db).update_room_status(reservation['room_id'], 'available')


class Payment:
    """Payment model"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def create_payment(self, reservation_id: int, amount: float, payment_method: str) -> int:
        """Create a payment record"""
        query = """
            INSERT INTO payments (reservation_id, amount, payment_method, payment_status)
            VALUES (?, ?, ?, 'completed')
        """
        return self.db.execute_update(query, (reservation_id, amount, payment_method))
    
    def get_payments_by_reservation(self, reservation_id: int) -> List[sqlite3.Row]:
        """Get all payments for a reservation"""
        return self.db.execute_query(
            "SELECT * FROM payments WHERE reservation_id = ? ORDER BY payment_date",
            (reservation_id,)
        )

