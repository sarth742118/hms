"""
Hotel Management System - Flask Web Application
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
from hotel_manager import HotelManager
import os
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()  # For flash messages

# Initialize hotel manager
manager = HotelManager()


@app.route('/')
def index():
    """Dashboard/home page"""
    summary = manager.get_room_status_summary()
    recent_reservations = manager.view_reservations()[:5]  # Last 5 reservations
    
    # Calculate statistics
    total_revenue = sum(r['total_amount'] for r in manager.view_reservations() 
                       if r['status'] == 'checked_out')
    active_reservations = len([r for r in manager.view_reservations() 
                              if r['status'] in ['confirmed', 'checked_in']])
    
    stats = {
        'total_rooms': summary['total'],
        'available_rooms': summary['available'],
        'occupied_rooms': summary['occupied'],
        'maintenance_rooms': summary['maintenance'],
        'total_revenue': total_revenue,
        'active_reservations': active_reservations
    }
    
    return render_template('index.html', stats=stats, recent_reservations=recent_reservations)


@app.route('/rooms')
def rooms():
    """View all rooms"""
    status_filter = request.args.get('status', '')
    all_rooms = manager.view_rooms()
    
    # Filter by status if provided
    if status_filter:
        all_rooms = [r for r in all_rooms if r['status'] == status_filter]
    
    return render_template('rooms.html', rooms=all_rooms, status_filter=status_filter)


@app.route('/rooms/add', methods=['GET', 'POST'])
def add_room():
    """Add a new room"""
    if request.method == 'POST':
        try:
            room_number = request.form.get('room_number')
            room_type = request.form.get('room_type')
            price_per_night = float(request.form.get('price_per_night'))
            capacity = int(request.form.get('capacity'))
            amenities = request.form.get('amenities', '')
            status = request.form.get('status', 'available')
            
            # Use the room model directly to pass status
            room_id = manager.room.add_room(room_number, room_type, price_per_night, capacity, amenities, status)
            if room_id:
                flash('Room added successfully!', 'success')
                return redirect(url_for('rooms'))
            else:
                flash('Error: Room number already exists!', 'error')
        except sqlite3.IntegrityError:
            flash('Error: Room number already exists!', 'error')
        except ValueError:
            flash('Error: Invalid input values!', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('add_room.html')


@app.route('/rooms/check_availability', methods=['GET', 'POST'])
def check_availability():
    """Check room availability"""
    available_rooms = []
    check_in = ""
    check_out = ""
    
    if request.method == 'POST':
        check_in = request.form.get('check_in')
        check_out = request.form.get('check_out')
        
        if check_in and check_out:
            try:
                # Validate dates
                datetime.strptime(check_in, "%Y-%m-%d")
                datetime.strptime(check_out, "%Y-%m-%d")
                available_rooms = manager.get_available_rooms(check_in, check_out)
            except ValueError:
                flash('Error: Invalid date format! Use YYYY-MM-DD', 'error')
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
    
    return render_template('check_availability.html', 
                         available_rooms=available_rooms, 
                         check_in=check_in, 
                         check_out=check_out)


@app.route('/reservations')
def reservations():
    """View all reservations"""
    status_filter = request.args.get('status', '')
    all_reservations = manager.view_reservations(status_filter if status_filter else None)
    return render_template('reservations.html', reservations=all_reservations, 
                         status_filter=status_filter)


@app.route('/reservations/new', methods=['GET', 'POST'])
def new_reservation():
    """Create a new reservation"""
    if request.method == 'POST':
        try:
            check_in = request.form.get('check_in')
            check_out = request.form.get('check_out')
            room_id = int(request.form.get('room_id'))
            guest_name = request.form.get('guest_name')
            phone = request.form.get('phone')
            email = request.form.get('email', '')
            address = request.form.get('address', '')
            
            # Validate dates
            datetime.strptime(check_in, "%Y-%m-%d")
            datetime.strptime(check_out, "%Y-%m-%d")
            
            reservation_id = manager.make_reservation(
                guest_name, phone, room_id, check_in, check_out, email, address
            )
            
            if reservation_id:
                reservation = manager.reservation.get_reservation_by_id(reservation_id)
                flash(f'Reservation created successfully! Reservation ID: {reservation_id}, Total: ${reservation["total_amount"]:.2f}', 'success')
                return redirect(url_for('reservations'))
            else:
                flash('Error: Room not available or invalid room ID!', 'error')
        except ValueError as e:
            flash(f'Error: Invalid input - {str(e)}', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    # Get available rooms based on form dates or default dates
    check_in = request.form.get('check_in') if request.method == 'POST' else None
    check_out = request.form.get('check_out') if request.method == 'POST' else None
    
    if not check_in or not check_out:
        today = datetime.now().strftime("%Y-%m-%d")
        next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        check_in = today
        check_out = next_week
    
    available_rooms = manager.get_available_rooms(check_in, check_out)
    
    return render_template('new_reservation.html', available_rooms=available_rooms,
                         default_check_in=check_in, default_check_out=check_out)


@app.route('/reservations/<int:reservation_id>/checkin', methods=['POST'])
def check_in(reservation_id):
    """Check in a guest"""
    if manager.check_in_guest(reservation_id):
        flash('Guest checked in successfully!', 'success')
    else:
        flash('Error: Reservation not found or already checked in!', 'error')
    return redirect(url_for('reservations'))


@app.route('/reservations/<int:reservation_id>/checkout', methods=['GET', 'POST'])
def check_out(reservation_id):
    """Check out a guest"""
    reservation = manager.reservation.get_reservation_by_id(reservation_id)
    
    if not reservation:
        flash('Error: Reservation not found!', 'error')
        return redirect(url_for('reservations'))
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method', 'cash')
        
        if manager.check_out_guest(reservation_id, payment_method):
            flash(f'Guest checked out successfully! Total paid: ${reservation["total_amount"]:.2f}', 'success')
            return redirect(url_for('reservations'))
        else:
            flash('Error: Guest not checked in!', 'error')
    
    return render_template('checkout.html', reservation=reservation)


@app.route('/reservations/<int:reservation_id>/cancel', methods=['POST'])
def cancel_reservation(reservation_id):
    """Cancel a reservation"""
    if manager.cancel_reservation(reservation_id):
        flash('Reservation cancelled successfully!', 'success')
    else:
        flash('Error: Reservation not found or cannot be cancelled!', 'error')
    return redirect(url_for('reservations'))


@app.route('/guests')
def guests():
    """View all guests"""
    all_guests = manager.view_guests()
    return render_template('guests.html', guests=all_guests)


@app.route('/rooms/<int:room_id>/update_status', methods=['POST'])
def update_room_status(room_id):
    """Update room status"""
    new_status = request.form.get('status')
    
    if new_status not in ['available', 'occupied', 'maintenance']:
        flash('Error: Invalid room status!', 'error')
        return redirect(url_for('rooms'))
    
    try:
        manager.room.update_room_status(room_id, new_status)
        flash(f'Room status updated to {new_status}!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('rooms'))


@app.route('/api/available_rooms')
def api_available_rooms():
    """API endpoint to get available rooms for AJAX requests"""
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')
    
    if not check_in or not check_out:
        return jsonify({'error': 'Missing check_in or check_out parameters'}), 400
    
    try:
        available_rooms = manager.get_available_rooms(check_in, check_out)
        rooms_data = [{
            'room_id': room['room_id'],
            'room_number': room['room_number'],
            'room_type': room['room_type'],
            'price_per_night': room['price_per_night'],
            'capacity': room['capacity']
        } for room in available_rooms]
        return jsonify({'rooms': rooms_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Open browser automatically
    import webbrowser
    from threading import Timer
    
    def open_browser():
        webbrowser.open('http://localhost:5000')
    
    # Wait a moment for server to start, then open browser
    Timer(1.5, open_browser).start()
    
    print("\n" + "="*60)
    print("  Hotel Management System - Starting Web Server")
    print("="*60)
    print("  Server running at: http://localhost:5000")
    print("  Browser will open automatically...")
    print("  Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)

