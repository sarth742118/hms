"""
Hotel Management System - Command Line Interface
"""
from datetime import datetime, timedelta
from hotel_manager import HotelManager


class HotelCLI:
    """Command Line Interface for Hotel Management System"""
    
    def __init__(self):
        self.manager = HotelManager()
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("    HOTEL MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add Room")
        print("2. View All Rooms")
        print("3. Check Room Availability")
        print("4. Make Reservation")
        print("5. View Reservations")
        print("6. Check In Guest")
        print("7. Check Out Guest")
        print("8. View Guests")
        print("9. Room Status Summary")
        print("10. Cancel Reservation")
        print("0. Exit")
        print("="*50)
    
    def add_room(self):
        """Add a new room"""
        print("\n--- Add New Room ---")
        try:
            room_number = input("Room Number: ").strip()
            room_type = input("Room Type (Single/Double/Suite/Presidential): ").strip()
            price_per_night = float(input("Price per Night: "))
            capacity = int(input("Capacity (number of guests): "))
            amenities = input("Amenities (comma-separated, optional): ").strip()
            
            if self.manager.add_room(room_number, room_type, price_per_night, capacity, amenities):
                print(f"✓ Room {room_number} added successfully!")
            else:
                print("✗ Error: Room number already exists!")
        except ValueError:
            print("✗ Error: Invalid input!")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def view_rooms(self):
        """View all rooms"""
        print("\n--- All Rooms ---")
        rooms = self.manager.view_rooms()
        if not rooms:
            print("No rooms found.")
            return
        
        print(f"{'Room #':<10} {'Type':<15} {'Price/Night':<15} {'Capacity':<10} {'Status':<12}")
        print("-" * 70)
        for room in rooms:
            print(f"{room['room_number']:<10} {room['room_type']:<15} "
                  f"${room['price_per_night']:<14.2f} {room['capacity']:<10} {room['status']:<12}")
    
    def check_availability(self):
        """Check room availability"""
        print("\n--- Check Room Availability ---")
        try:
            check_in = input("Check-in Date (YYYY-MM-DD): ").strip()
            check_out = input("Check-out Date (YYYY-MM-DD): ").strip()
            
            # Validate dates
            datetime.strptime(check_in, "%Y-%m-%d")
            datetime.strptime(check_out, "%Y-%m-%d")
            
            available_rooms = self.manager.get_available_rooms(check_in, check_out)
            
            if not available_rooms:
                print("No available rooms for the selected dates.")
                return
            
            print(f"\nAvailable Rooms ({len(available_rooms)}):")
            print(f"{'ID':<5} {'Room #':<10} {'Type':<15} {'Price/Night':<15} {'Capacity':<10}")
            print("-" * 60)
            for room in available_rooms:
                print(f"{room['room_id']:<5} {room['room_number']:<10} {room['room_type']:<15} "
                      f"${room['price_per_night']:<14.2f} {room['capacity']:<10}")
        except ValueError:
            print("✗ Error: Invalid date format! Use YYYY-MM-DD")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def make_reservation(self):
        """Make a reservation"""
        print("\n--- Make Reservation ---")
        try:
            check_in = input("Check-in Date (YYYY-MM-DD): ").strip()
            check_out = input("Check-out Date (YYYY-MM-DD): ").strip()
            
            # Validate dates
            datetime.strptime(check_in, "%Y-%m-%d")
            datetime.strptime(check_out, "%Y-%m-%d")
            
            # Show available rooms
            available_rooms = self.manager.get_available_rooms(check_in, check_out)
            if not available_rooms:
                print("No available rooms for the selected dates.")
                return
            
            print("\nAvailable Rooms:")
            for room in available_rooms:
                print(f"ID: {room['room_id']} - {room['room_number']} ({room['room_type']}) - "
                      f"${room['price_per_night']}/night")
            
            room_id = int(input("\nSelect Room ID: "))
            
            # Guest information
            name = input("Guest Name: ").strip()
            phone = input("Phone Number: ").strip()
            email = input("Email (optional): ").strip()
            address = input("Address (optional): ").strip()
            
            reservation_id = self.manager.make_reservation(
                name, phone, room_id, check_in, check_out, email, address
            )
            
            if reservation_id:
                reservation = self.manager.reservation.get_reservation_by_id(reservation_id)
                print(f"\n✓ Reservation created successfully!")
                print(f"Reservation ID: {reservation_id}")
                print(f"Total Amount: ${reservation['total_amount']:.2f}")
            else:
                print("✗ Error: Room not available or invalid room ID!")
        except ValueError:
            print("✗ Error: Invalid input!")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def view_reservations(self):
        """View all reservations"""
        print("\n--- All Reservations ---")
        reservations = self.manager.view_reservations()
        if not reservations:
            print("No reservations found.")
            return
        
        print(f"{'ID':<5} {'Guest':<20} {'Room':<10} {'Check-in':<12} {'Check-out':<12} {'Amount':<12} {'Status':<15}")
        print("-" * 100)
        for res in reservations:
            print(f"{res['reservation_id']:<5} {res['guest_name']:<20} {res['room_number']:<10} "
                  f"{res['check_in_date']:<12} {res['check_out_date']:<12} "
                  f"${res['total_amount']:<11.2f} {res['status']:<15}")
    
    def check_in_guest(self):
        """Check in a guest"""
        print("\n--- Check In Guest ---")
        try:
            reservation_id = int(input("Reservation ID: "))
            
            if self.manager.check_in_guest(reservation_id):
                print("✓ Guest checked in successfully!")
            else:
                print("✗ Error: Reservation not found or already checked in!")
        except ValueError:
            print("✗ Error: Invalid reservation ID!")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def check_out_guest(self):
        """Check out a guest"""
        print("\n--- Check Out Guest ---")
        try:
            reservation_id = int(input("Reservation ID: "))
            payment_method = input("Payment Method (cash/card/online): ").strip() or "cash"
            
            if self.manager.check_out_guest(reservation_id, payment_method):
                reservation = self.manager.reservation.get_reservation_by_id(reservation_id)
                print("✓ Guest checked out successfully!")
                print(f"Total Paid: ${reservation['total_amount']:.2f}")
            else:
                print("✗ Error: Reservation not found or guest not checked in!")
        except ValueError:
            print("✗ Error: Invalid reservation ID!")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def view_guests(self):
        """View all guests"""
        print("\n--- All Guests ---")
        guests = self.manager.view_guests()
        if not guests:
            print("No guests found.")
            return
        
        print(f"{'ID':<5} {'Name':<25} {'Phone':<15} {'Email':<30}")
        print("-" * 80)
        for guest in guests:
            print(f"{guest['guest_id']:<5} {guest['name']:<25} {guest['phone']:<15} "
                  f"{guest['email'] or 'N/A':<30}")
    
    def room_status_summary(self):
        """Display room status summary"""
        print("\n--- Room Status Summary ---")
        summary = self.manager.get_room_status_summary()
        print(f"Total Rooms: {summary['total']}")
        print(f"Available: {summary['available']}")
        print(f"Occupied: {summary['occupied']}")
        print(f"Maintenance: {summary['maintenance']}")
    
    def cancel_reservation(self):
        """Cancel a reservation"""
        print("\n--- Cancel Reservation ---")
        try:
            reservation_id = int(input("Reservation ID to cancel: "))
            
            if self.manager.cancel_reservation(reservation_id):
                print("✓ Reservation cancelled successfully!")
            else:
                print("✗ Error: Reservation not found or cannot be cancelled!")
        except ValueError:
            print("✗ Error: Invalid reservation ID!")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def run(self):
        """Run the CLI application"""
        print("Welcome to Hotel Management System!")
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "0":
                print("\nThank you for using Hotel Management System!")
                self.manager.close()
                break
            elif choice == "1":
                self.add_room()
            elif choice == "2":
                self.view_rooms()
            elif choice == "3":
                self.check_availability()
            elif choice == "4":
                self.make_reservation()
            elif choice == "5":
                self.view_reservations()
            elif choice == "6":
                self.check_in_guest()
            elif choice == "7":
                self.check_out_guest()
            elif choice == "8":
                self.view_guests()
            elif choice == "9":
                self.room_status_summary()
            elif choice == "10":
                self.cancel_reservation()
            else:
                print("✗ Invalid choice! Please try again.")
            
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    cli = HotelCLI()
    cli.run()

