"""
Initialize sample data for testing the Hotel Management System
"""
from hotel_manager import HotelManager


def init_sample_data():
    """Add sample rooms and data to the database"""
    manager = HotelManager()
    
    print("Initializing sample data...")
    
    # Add sample rooms
    rooms = [
        ("101", "Single", 80.00, 1, "WiFi, TV, AC"),
        ("102", "Single", 80.00, 1, "WiFi, TV, AC"),
        ("201", "Double", 120.00, 2, "WiFi, TV, AC, Mini Bar"),
        ("202", "Double", 120.00, 2, "WiFi, TV, AC, Mini Bar"),
        ("301", "Suite", 200.00, 4, "WiFi, TV, AC, Mini Bar, Living Room"),
        ("302", "Suite", 200.00, 4, "WiFi, TV, AC, Mini Bar, Living Room"),
        ("401", "Presidential", 500.00, 6, "WiFi, TV, AC, Mini Bar, Living Room, Jacuzzi, Balcony"),
    ]
    
    for room_number, room_type, price, capacity, amenities in rooms:
        try:
            manager.add_room(room_number, room_type, price, capacity, amenities)
            print(f"✓ Added room {room_number}")
        except Exception as e:
            print(f"✗ Failed to add room {room_number}: {e}")
    
    print("\nSample data initialization complete!")
    print("You can now run 'python main.py' to start using the system.")
    
    manager.close()


if __name__ == "__main__":
    init_sample_data()

