"""
Hotel Management System - Main business logic
"""
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, List
from database import Database, Room, Guest, Reservation, Payment


class HotelManager:
    """Main hotel management class"""
    
    def __init__(self, db_name: str = "hotel.db"):
        self.db = Database(db_name)
        self.room = Room(self.db)
        self.guest = Guest(self.db)
        self.reservation = Reservation(self.db)
        self.payment = Payment(self.db)
    
    def add_room(self, room_number: str, room_type: str, price_per_night: float,
                 capacity: int, amenities: str = "") -> bool:
        """Add a new room to the hotel"""
        try:
            self.room.add_room(room_number, room_type, price_per_night, capacity, amenities)
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_available_rooms(self, check_in: str, check_out: str) -> List:
        """Get available rooms for given date range"""
        return self.room.get_available_rooms(check_in, check_out)
    
    def register_guest(self, name: str, phone: str, email: str = "", address: str = "") -> int:
        """Register a new guest or return existing guest ID"""
        existing = self.guest.get_guest_by_phone(phone)
        if existing:
            return existing['guest_id']
        return self.guest.add_guest(name, phone, email, address)
    
    def make_reservation(self, guest_name: str, phone: str, room_id: int,
                        check_in: str, check_out: str, email: str = "", address: str = "") -> Optional[int]:
        """Make a reservation"""
        # Register or get guest
        guest_id = self.register_guest(guest_name, phone, email, address)
        
        # Check if room is available
        available_rooms = self.get_available_rooms(check_in, check_out)
        room_ids = [r['room_id'] for r in available_rooms]
        
        if room_id not in room_ids:
            return None
        
        # Calculate total amount
        room = self.room.get_room_by_id(room_id)
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        nights = (check_out_date - check_in_date).days
        total_amount = room['price_per_night'] * nights
        
        # Create reservation
        reservation_id = self.reservation.create_reservation(
            guest_id, room_id, check_in, check_out, total_amount
        )
        
        return reservation_id
    
    def check_in_guest(self, reservation_id: int) -> bool:
        """Check in a guest"""
        reservation = self.reservation.get_reservation_by_id(reservation_id)
        if not reservation or reservation['status'] != 'confirmed':
            return False
        
        self.reservation.check_in(reservation_id)
        return True
    
    def check_out_guest(self, reservation_id: int, payment_method: str = "cash") -> bool:
        """Check out a guest and process payment"""
        reservation = self.reservation.get_reservation_by_id(reservation_id)
        if not reservation or reservation['status'] != 'checked_in':
            return False
        
        # Process payment
        self.payment.create_payment(reservation_id, reservation['total_amount'], payment_method)
        
        # Check out
        self.reservation.check_out(reservation_id)
        return True
    
    def view_reservations(self, status: Optional[str] = None) -> List:
        """View all reservations, optionally filtered by status"""
        all_reservations = self.reservation.get_all_reservations()
        if status:
            return [r for r in all_reservations if r['status'] == status]
        return all_reservations
    
    def view_rooms(self) -> List:
        """View all rooms"""
        return self.room.get_all_rooms()
    
    def view_guests(self) -> List:
        """View all guests"""
        return self.guest.get_all_guests()
    
    def get_room_status_summary(self) -> dict:
        """Get summary of room statuses"""
        rooms = self.room.get_all_rooms()
        summary = {
            'total': len(rooms),
            'available': sum(1 for r in rooms if r['status'] == 'available'),
            'occupied': sum(1 for r in rooms if r['status'] == 'occupied'),
            'maintenance': sum(1 for r in rooms if r['status'] == 'maintenance')
        }
        return summary
    
    def cancel_reservation(self, reservation_id: int) -> bool:
        """Cancel a reservation"""
        reservation = self.reservation.get_reservation_by_id(reservation_id)
        if not reservation or reservation['status'] not in ['pending', 'confirmed']:
            return False
        
        # Cancel the reservation
        self.reservation.update_reservation_status(reservation_id, 'cancelled')
        
        # If room was occupied, make it available again
        if reservation['status'] == 'checked_in':
            self.room.update_room_status(reservation['room_id'], 'available')
        
        return True
    
    def close(self):
        """Close database connection"""
        self.db.close()

