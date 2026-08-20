from dataclasses import dataclass


@dataclass(frozen=True)
class Incident:
    slug: str
    method: str
    path: str
    summary: str
    owner: str


INCIDENTS = (
    Incident("unknown-employee", "GET", "/api/v1/employees/999999", "Unknown employee dereferenced", "people-operations"),
    Incident("badge-expiry", "GET", "/api/v1/employees/481516/badge", "Badge expiry compared with wrong type", "security"),
    Incident("quota-zero", "GET", "/api/v1/mdr/481516/quota?minutes=0", "Zero-minute quota calculation", "mdr"),
    Incident("corrupt-number", "POST", "/api/v1/mdr/bins/01FC/refine", "Corrupt macrodata converted to decimal", "mdr"),
    Incident("bin-overflow", "GET", "/api/v1/mdr/bins/99ZZ", "Bin index beyond manifest", "mdr"),
    Incident("missing-department", "GET", "/api/v1/departments/coil-of-doom", "Unregistered department lookup", "floor-admin"),
    Incident("decimal-json", "GET", "/api/v1/payroll/481516/statement", "Decimal encoded by standard JSON encoder", "payroll"),
    Incident("empty-wellness", "GET", "/api/v1/wellness/481516/latest", "Empty wellness history aggregated", "wellness"),
    Incident("corrupt-token", "POST", "/api/v1/security/sessions/validate", "Session bytes decoded as UTF-8", "security"),
    Incident("naive-overtime", "GET", "/api/v1/timecards/481516/overtime", "Naive shift timestamp treated as zoned", "payroll"),
    Incident("elevator-state", "POST", "/api/v1/elevators/7/transitions", "Illegal elevator state transition", "security"),
    Incident("perpetuity-file", "GET", "/api/v1/perpetuity-wing/portraits/ambrose", "Portrait asset missing from disk", "archives"),
    Incident("empty-music", "POST", "/api/v1/incentives/music-dance-experience", "Empty music catalog selected", "employee-experience"),
    Incident("waffle-date", "POST", "/api/v1/incentives/waffle-party", "Malformed waffle party date", "employee-experience"),
    Incident("goat-mutation", "POST", "/api/v1/mammalians-nurturable/feeding-round", "Goat roster mutated during iteration", "mammalians-nurturable"),
    Incident("break-room-recursion", "POST", "/api/v1/break-room/sessions/481516/repeat", "Compunction statement recursion overflow", "security"),
    Incident("clearance-none", "GET", "/api/v1/security/clearance/481516", "Missing clearance compared to integer", "security"),
    Incident("printer-protocol", "POST", "/api/v1/optics-design/printers/blue/queue", "Binary printer protocol concatenated with text", "optics-design"),
    Incident("handbook-template", "GET", "/api/v1/handbook/values/9", "Handbook template placeholder absent", "legal"),
    Incident("fingertrap-stock", "POST", "/api/v1/incentives/finger-traps/reserve", "Negative finger-trap inventory", "employee-experience"),
    Incident("duplicate-retirement", "POST", "/api/v1/retirements", "Duplicate retirement inserted", "people-operations"),
    Incident("payroll-rate", "POST", "/api/v1/payroll/481516/calculate", "Decimal salary multiplied by float rate", "payroll"),
    Incident("protocol-enum", "POST", "/api/v1/emergency/protocols/activate", "Unknown emergency protocol parsed", "security"),
    Incident("floor-coordinate", "GET", "/api/v1/floors/severed/rooms/mind", "Malformed floor coordinate unpacked", "floor-admin"),
    Incident("optics-payload", "POST", "/api/v1/optics-design/transmissions/decrypt", "Invalid encrypted payload decoded", "optics-design"),
    Incident("outie-contact", "GET", "/api/v1/employees/481516/outie-contact", "Severed worker requests forbidden outie data", "people-operations"),
    Incident("board-message", "GET", "/api/v1/board/messages/latest", "Missing board speaker invoked", "executive"),
    Incident("cold-harbor", "POST", "/api/v1/mdr/files/cold-harbor/project", "Projection exponential overflows", "mdr"),
    Incident("export-column", "GET", "/api/v1/exports/timecards.csv", "Export row lacks cost center", "data-platform"),
    Incident("interdepartmental-timeout", "POST", "/api/v1/departments/optics-design/messages", "Interdepartmental message exceeds deadline", "platform"),
)


BY_SLUG = {incident.slug: incident for incident in INCIDENTS}
