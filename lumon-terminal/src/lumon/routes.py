from flask import Blueprint, jsonify, request

from .incidents import INCIDENTS
from .services import interdepartmental
from .services import severed_floor as floor


api = Blueprint("api", __name__, url_prefix="/api/v1")


@api.get("")
def route_manifest():
    return jsonify(
        name="Lumon Industries Severed Floor API",
        departments=["Macrodata Refinement", "Optics and Design", "Wellness", "Security"],
        demo_incidents=[{"slug": item.slug, "method": item.method, "path": item.path} for item in INCIDENTS],
    )


@api.get("/employees/<employee_id>")
def employee(employee_id):
    return floor.load_employee(employee_id)


@api.get("/employees/<employee_id>/badge")
def badge(employee_id):
    return floor.badge_status(employee_id)


@api.get("/mdr/<employee_id>/quota")
def quota(employee_id):
    return floor.quota_velocity(employee_id, request.args.get("minutes", type=int, default=60))


@api.post("/mdr/bins/<bin_id>/refine")
def refine(bin_id):
    return floor.refine_macrodata(bin_id)


@api.get("/mdr/bins/<bin_id>")
def macrodata_bin(bin_id):
    return floor.lookup_bin(bin_id)


@api.get("/departments/<code>")
def department(code):
    return floor.department_manifest(code)


@api.get("/payroll/<employee_id>/statement")
def statement(employee_id):
    return floor.payroll_statement(employee_id), 200, {"Content-Type": "application/json"}


@api.get("/wellness/<employee_id>/latest")
def wellness(employee_id):
    return floor.latest_wellness_session(employee_id)


@api.post("/security/sessions/validate")
def validate_session():
    return floor.validate_security_session()


@api.get("/timecards/<employee_id>/overtime")
def overtime(employee_id):
    return floor.calculate_overtime(employee_id)


@api.post("/elevators/<elevator_id>/transitions")
def elevator_transition(elevator_id):
    return floor.transition_elevator(elevator_id)


@api.get("/perpetuity-wing/portraits/<slug>")
def portrait(slug):
    return floor.load_perpetuity_portrait(slug)


@api.post("/incentives/music-dance-experience")
def music_dance_experience():
    return floor.select_music_dance_experience()


@api.post("/incentives/waffle-party")
def waffle_party():
    return floor.schedule_waffle_party()


@api.post("/mammalians-nurturable/feeding-round")
def feeding_round():
    return floor.complete_feeding_round()


@api.post("/break-room/sessions/<employee_id>/repeat")
def break_room_repeat(employee_id):
    return {"employee_id": employee_id, "statement": floor.repeat_compunction_statement()}


@api.get("/security/clearance/<employee_id>")
def clearance(employee_id):
    return floor.security_clearance(employee_id)


@api.post("/optics-design/printers/<printer>/queue")
def printer_queue(printer):
    return floor.queue_printer_job(printer)


@api.get("/handbook/values/<int:value_number>")
def handbook(value_number):
    return floor.handbook_value(value_number)


@api.post("/incentives/finger-traps/reserve")
def finger_traps():
    return floor.reserve_finger_traps()


@api.post("/retirements")
def retirement():
    return floor.create_retirement(), 201


@api.post("/payroll/<employee_id>/calculate")
def payroll(employee_id):
    return floor.calculate_payroll(employee_id)


@api.post("/emergency/protocols/activate")
def emergency_protocol():
    return floor.activate_emergency_protocol()


@api.get("/floors/severed/rooms/<room>")
def room_location(room):
    return floor.locate_floor_room(room)


@api.post("/optics-design/transmissions/decrypt")
def decrypt_transmission():
    return floor.decrypt_optics_transmission()


@api.get("/employees/<employee_id>/outie-contact")
def outie_contact(employee_id):
    return floor.outie_contact_details(employee_id)


@api.get("/board/messages/latest")
def board_message():
    return floor.latest_board_message()


@api.post("/mdr/files/cold-harbor/project")
def cold_harbor_projection():
    return floor.project_cold_harbor_completion()


@api.get("/exports/timecards.csv")
def timecard_export():
    return floor.export_timecards(), 200, {"Content-Type": "text/csv"}


@api.post("/departments/optics-design/messages")
def interdepartmental_message():
    return interdepartmental.deliver_message()
