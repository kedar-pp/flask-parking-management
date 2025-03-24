from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import ParkingSlot, User ,db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.username != 'admin':
        flash('Access denied: Admins only!')
        return redirect(url_for('dashboard'))

    slots = ParkingSlot.query.all()
    users = User.query.all()
    return render_template('admin.html', slots=slots, users=users)

@admin_bp.route('/registered_users')
@login_required
def registered_users():
    if current_user.username != 'admin':
        flash('Access denied: Admins only!')
        return redirect(url_for('dashboard'))
    users = User.query.all()
    return render_template('registered_users.html', users=users)

@admin_bp.route('/release_slot/<int:slot_id>', methods=['POST'])
@login_required
def admin_release_slot(slot_id):
    if current_user.username != 'admin':
        flash('Access denied: Admins only!')
        return redirect(url_for('dashboard'))
    slot = ParkingSlot.query.get(slot_id)
    if slot and slot.status == "booked":
        slot.status = "available"
        slot.booked_by = None
        db.session.commit()
        flash('Slot released successfully!')
    else:
        flash('Slot is already available!')
    return redirect(url_for('admin.admin_dashboard'))