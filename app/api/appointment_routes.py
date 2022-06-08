from flask import Blueprint, jsonify, request
from app.models import db, User, Property, Appointment
from flask_login import current_user, login_required
from datetime import datetime
from app.forms import AddAppointmentForm

appointment_routes = Blueprint("appointments", __name__)

def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages


@appointment_routes.route("/", methods=["POST"])
@login_required
def add_appointment():
    form = AddAppointmentForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():

        # Check all the appointments in property to see if it overlaps
        property_id = form.data["property_id"]
        date = form.data["date"]
        time = form.data["time"]
        message = form.data["message"]

        # Check user appointment to see if overlaps
        user_appt = Appointment.query.filter(Appointment.user_id == current_user.id,  Appointment.date == date, Appointment.time == time).first()

        if user_appt:
            return {"errors": ["You already have another appointment at this timeslot"]}

        # query for to see if it is not avaliable
        exists = Appointment.query.filter(Appointment.property_id == property_id, Appointment.date == date, Appointment.time == time).first()

        if exists:
            return {"errors": ["Timeslot not avaliable"]}


        new_appointment = Appointment(
            user_id=current_user.id,
            date=date, time=time,
            message=message,
            property_id=property_id)

        db.session.add(new_appointment)
        db.session.commit()

        return {"appointment": new_appointment.to_dict()}

    return {'errors': validation_errors_to_error_messages(form.errors)}, 401
