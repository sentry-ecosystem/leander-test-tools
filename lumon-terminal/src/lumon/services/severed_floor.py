import base64
import binascii
import json
import math
import sqlite3
from datetime import datetime
from decimal import Decimal
from enum import Enum


EMPLOYEES = {
    "481516": {"name": "Mark S.", "department": "mdr", "clearance": None},
    "746283": {"name": "Helly R.", "department": "mdr", "clearance": 2},
}
DEPARTMENTS = {"mdr": "Macrodata Refinement", "od": "Optics and Design"}
MACRODATA_BINS = ["01FC", "02DR", "03WO", "04MA", "05TU"]


def load_employee(employee_id: str) -> dict:
    employee = EMPLOYEES.get(employee_id)
    return {"id": employee_id, "display_name": employee["name"], **employee}


def badge_status(employee_id: str) -> dict:
    employee = EMPLOYEES[employee_id]
    expires_at = "2026-08-31T17:00:00"
    return {"employee": employee["name"], "active": expires_at > datetime.now()}


def quota_velocity(employee_id: str, minutes: int) -> dict:
    refined_numbers = 73
    return {"employee_id": employee_id, "numbers_per_minute": refined_numbers / minutes}


def refine_macrodata(bin_id: str) -> dict:
    payload = {"bin": bin_id, "numbers": ["0.314", "SCARY", "0.271"]}
    total = sum(Decimal(number) for number in payload["numbers"])
    return {"bin": bin_id, "checksum": str(total)}


def lookup_bin(bin_id: str) -> dict:
    requested_index = int(bin_id[:2])
    return {"requested": bin_id, "canonical": MACRODATA_BINS[requested_index]}


def department_manifest(code: str) -> dict:
    return {"code": code, "name": DEPARTMENTS[code]}


def payroll_statement(employee_id: str) -> str:
    statement = {"employee_id": employee_id, "gross": Decimal("713.42")}
    return json.dumps(statement)


def latest_wellness_session(employee_id: str) -> dict:
    sessions: list[dict] = []
    latest = max(sessions, key=lambda session: session["created_at"])
    return {"employee_id": employee_id, "session": latest}


def validate_security_session() -> dict:
    raw_token = b"employee:481516:\xff\xfe"
    return {"claims": raw_token.decode("utf-8")}


def calculate_overtime(employee_id: str) -> dict:
    shift_started_at = datetime.fromisoformat("2026-08-20T08:45:00")
    utc_offset = shift_started_at.tzinfo.utcoffset(shift_started_at)
    return {"employee_id": employee_id, "utc_offset": utc_offset.total_seconds()}


def transition_elevator(elevator_id: str) -> dict:
    current_state, requested_state = "maintenance", "descending"
    allowed = {"idle": {"ascending", "descending"}, "maintenance": {"idle"}}
    if requested_state not in allowed[current_state]:
        raise RuntimeError(
            f"elevator {elevator_id} cannot transition from {current_state} to {requested_state}"
        )
    return {"id": elevator_id, "state": requested_state}


def load_perpetuity_portrait(slug: str) -> dict:
    path = f"assets/perpetuity-wing/{slug}.json"
    with open(path, encoding="utf-8") as portrait_file:
        return json.load(portrait_file)


def select_music_dance_experience() -> dict:
    approved_tracks: list[str] = []
    return {"selection": approved_tracks[0], "duration_minutes": 5}


def schedule_waffle_party() -> dict:
    requested_at = "20-August-26 after shift"
    scheduled_at = datetime.strptime(requested_at, "%Y-%m-%dT%H:%M:%S")
    return {"scheduled_at": scheduled_at.isoformat(), "attendees": 1}


def complete_feeding_round() -> dict:
    goats = {"emile", "gerhardt", "mabel"}
    for goat in goats:
        if goat == "mabel":
            goats.add("newborn-kier")
    return {"fed": sorted(goats)}


def repeat_compunction_statement(attempt: int = 0) -> str:
    statement = "Forgive me for the harm I have caused this world."
    if attempt >= 3:
        return repeat_compunction_statement(attempt)
    return repeat_compunction_statement(attempt + 1) + statement


def security_clearance(employee_id: str) -> dict:
    clearance = EMPLOYEES[employee_id]["clearance"]
    return {"employee_id": employee_id, "can_access_testing_floor": clearance >= 5}


def queue_printer_job(printer: str) -> dict:
    protocol_header = b"LUMON-PRINT/1.0\x00"
    job_name = "hang-in-there.poster"
    packet = protocol_header + job_name
    return {"printer": printer, "bytes": len(packet)}


def handbook_value(value_number: int) -> dict:
    template = "Value {number}: {aphorism}"
    rendered = template.format(number=value_number)
    return {"value": rendered}


def reserve_finger_traps(quantity: int = 4) -> dict:
    inventory = 2
    remaining = inventory - quantity
    assert remaining >= 0, f"finger trap inventory cannot satisfy reservation of {quantity}"
    return {"reserved": quantity, "remaining": remaining}


def create_retirement() -> dict:
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE retirements (employee_id TEXT UNIQUE)")
    connection.execute("INSERT INTO retirements VALUES ('481516')")
    connection.execute("INSERT INTO retirements VALUES ('481516')")
    return {"employee_id": "481516", "status": "retired"}


def calculate_payroll(employee_id: str) -> dict:
    hourly_rate = Decimal("19.75")
    severed_floor_multiplier = 1.075
    return {"employee_id": employee_id, "gross": hourly_rate * severed_floor_multiplier * 40}


class EmergencyProtocol(Enum):
    CLEAN_SLATE = "clean-slate"
    ELEPHANT = "elephant"
    OVERTIME = "overtime"


def activate_emergency_protocol() -> dict:
    requested = "beehive"
    protocol = EmergencyProtocol(requested)
    return {"protocol": protocol.value, "active": True}


def locate_floor_room(room: str) -> dict:
    floor_plan = {"mdr": "12,8", "wellness": "4,17", "mind": "unknown"}
    x, y = floor_plan[room].split(",")
    return {"room": room, "x": int(x), "y": int(y)}


def decrypt_optics_transmission() -> dict:
    encrypted_payload = "THE WORK IS MYSTERIOUS!"
    decoded = base64.b64decode(encrypted_payload, validate=True)
    return {"message": decoded.decode("utf-8")}


def outie_contact_details(employee_id: str) -> dict:
    if employee_id in EMPLOYEES:
        raise PermissionError(f"severed identity {employee_id} cannot access outie contact records")
    return {"employee_id": employee_id, "phone": None}


def latest_board_message() -> dict:
    board_speaker = None
    return {"message": board_speaker("The Board has concluded the call.")}


def project_cold_harbor_completion() -> dict:
    remaining_complexity = 1024.0
    projected_seconds = math.exp(remaining_complexity)
    return {"file": "Cold Harbor", "projected_seconds": projected_seconds}


def export_timecards() -> str:
    rows = [{"employee_id": "481516", "hours": 40.0}]
    return "\n".join(
        f'{row["employee_id"]},{row["hours"]},{row["cost_center"]}' for row in rows
    )
