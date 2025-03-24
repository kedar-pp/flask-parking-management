from flask import Blueprint, render_template, request, redirect, flash, url_for 
from flask_login import login_required, current_user
from models import db, ParkingSlot

booking_bp = Blueprint('booking', __name__)

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     slots = ParkingSlot.query.all()
#     return render_template('dashboard.html', slots=slots)

@booking_bp.route('/book_slot/<int:slot_id>', methods=['POST'])
@login_required
def book_slot(slot_id):
    slot = ParkingSlot.query.get(slot_id)
    
    if slot and slot.status == "available":
        slot.status = "booked"
        slot.booked_by = current_user.id
        db.session.commit()
        flash('Parking slot reserved successfully!')
    else:
        flash('Slot is not available!')

    return redirect(url_for('dashboard'))

@booking_bp.route('/release_slot/<int:slot_id>', methods=['POST'])
@login_required
def release_slot(slot_id):
    slot = ParkingSlot.query.get(slot_id)

    if slot and slot.booked_by == current_user.id:
        slot.status = "available"
        slot.booked_by = None
        db.session.commit()
        flash('Slot released successfully!')

    return redirect('/dashboard')
