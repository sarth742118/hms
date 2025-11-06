# Hotel Management System

A comprehensive hotel management system built with Python, Flask, and SQLite. This system provides both a **modern web interface** and a **command-line interface** for managing rooms, guests, reservations, and payments efficiently.

## Features

- **Room Management**
  - Add new rooms with details (number, type, price, capacity, amenities)
  - View all rooms and their status
  - Check room availability for specific dates
  - Room status tracking (available, occupied, maintenance)

- **Guest Management**
  - Register new guests
  - View guest information
  - Automatic guest lookup by phone number

- **Reservation System**
  - Make new reservations with date validation
  - View all reservations with detailed information
  - Check availability before booking
  - Automatic total amount calculation
  - Cancel reservations

- **Check-in/Check-out**
  - Easy check-in process
  - Check-out with payment processing
  - Automatic room status updates

- **Reporting**
  - Room status summary
  - Reservation history
  - Payment tracking

## Installation

1. Make sure you have Python 3.7 or higher installed
2. Clone or download this repository
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web Application (Recommended)

1. **Initialize Sample Data (Optional)**
   ```bash
   python init_sample_data.py
   ```
   This will add sample rooms to get you started quickly.

2. **Run the Web Server**
   ```bash
   python app.py
   ```

3. **Access the Application**
   - Open your web browser and navigate to: `http://localhost:5000`
   - The web interface provides a modern, user-friendly experience with:
     - Beautiful dashboard with statistics
     - Easy room management
     - Intuitive reservation system
     - Real-time availability checking
     - Responsive design for mobile devices

### Command-Line Interface (CLI)

For command-line usage:

```bash
python main.py
```

### Web Interface Features

The web application includes:

1. **Dashboard** - Overview with statistics and recent reservations
2. **Room Management**
   - View all rooms with status
   - Add new rooms
   - Check room availability for specific dates
3. **Reservation System**
   - Create new reservations with real-time availability
   - View all reservations with filtering options
   - Check in/check out guests
   - Cancel reservations
4. **Guest Management** - View all registered guests
5. **Quick Actions** - Easy access to common operations

### CLI Menu Options (Command-Line Interface)

1. **Add Room** - Add a new room to the hotel inventory
2. **View All Rooms** - Display all rooms with their details
3. **Check Room Availability** - Check which rooms are available for specific dates
4. **Make Reservation** - Create a new reservation for a guest
5. **View Reservations** - Display all reservations
6. **Check In Guest** - Check in a guest using their reservation ID
7. **Check Out Guest** - Check out a guest and process payment
8. **View Guests** - Display all registered guests
9. **Room Status Summary** - View summary of room statuses
10. **Cancel Reservation** - Cancel an existing reservation

## Database Schema

The system uses SQLite database with the following tables:

- **rooms** - Room information and status
- **guests** - Guest information
- **reservations** - Booking details
- **payments** - Payment records

## Example Workflow

1. **Add Rooms**: First, add rooms to your hotel inventory
   ```
   Room Number: 101
   Room Type: Double
   Price per Night: 150.00
   Capacity: 2
   ```

2. **Make Reservation**: When a guest wants to book
   ```
   Check-in Date: 2024-01-15
   Check-out Date: 2024-01-18
   Select Room: 101
   Guest Name: John Doe
   Phone: +1234567890
   ```

3. **Check In**: On the check-in date
   ```
   Reservation ID: 1
   ```

4. **Check Out**: On the check-out date
   ```
   Reservation ID: 1
   Payment Method: card
   ```

## Project Structure

```
hotel-management-system/
│
├── app.py                  # Flask web application
├── database.py            # Database models and setup
├── hotel_manager.py       # Main business logic
├── main.py                # CLI interface
├── init_sample_data.py    # Sample data initialization
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── hotel.db              # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── rooms.html
│   ├── add_room.html
│   ├── check_availability.html
│   ├── reservations.html
│   ├── new_reservation.html
│   ├── checkout.html
│   └── guests.html
└── static/               # Static files
    ├── css/
    │   └── style.css     # Modern styling
    └── js/
        └── main.js       # JavaScript functionality
```

## Features in Detail

### Room Management
- Support for different room types (Single, Double, Suite, Presidential)
- Price per night configuration
- Capacity tracking
- Amenities listing
- Status management (available, occupied, maintenance)

### Reservation System
- Date conflict detection
- Automatic price calculation based on number of nights
- Reservation status tracking (pending, confirmed, checked_in, checked_out, cancelled)

### Payment Processing
- Payment method tracking (cash, card, online)
- Payment status management
- Automatic payment creation on check-out

## Features Highlights

### Web Interface
- **Modern UI** - Beautiful, responsive design with gradient colors and smooth animations
- **Dashboard** - Real-time statistics and overview
- **Interactive Forms** - User-friendly forms with validation
- **Real-time Updates** - Dynamic availability checking
- **Mobile Responsive** - Works on all devices

### Technical Features
- **SQLite Database** - Lightweight, no server setup required
- **Flask Framework** - Modern Python web framework
- **RESTful Design** - Clean URL structure
- **Flash Messages** - User feedback for actions
- **Form Validation** - Client and server-side validation

## Future Enhancements

Potential improvements for the system:
- User authentication and role-based access
- Email notifications for reservations
- Reports generation (PDF/Excel)
- Multi-hotel support
- Advanced search and filtering
- Guest loyalty program
- Room service management
- Calendar view for reservations
- Payment gateway integration

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to fork this project and submit pull requests for any improvements!

## Support

For issues or questions, please check the code comments or create an issue in the repository.

