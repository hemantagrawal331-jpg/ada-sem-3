# Lot data, plus entry and exit.
# greedy.py picks the slot (it uses the min heap).
# hashing.py stores vehicle number -> slot id.
# sorting.py orders the slots by distance for the page.

from algorithms.greedy import choose_slot
from algorithms.hashing import HashTable
from algorithms.sorting import insertion_sort


# distance is how far the bay is from the gate. 1 is the nearest.
# it is not the same as the row order on the page.
SLOTS = [
    # row A
    {"id": "A1", "type": "disabled", "distance": 2, "status": "free", "vehicle": None},
    {"id": "A2", "type": "normal", "distance": 1, "status": "free", "vehicle": None},
    {"id": "A3", "type": "ev", "distance": 3, "status": "free", "vehicle": None},
    {"id": "A4", "type": "normal", "distance": 4, "status": "free", "vehicle": None},
    # row B
    {"id": "B1", "type": "bike", "distance": 1, "status": "free", "vehicle": None},
    {"id": "B2", "type": "bike", "distance": 4, "status": "free", "vehicle": None},
    {"id": "B3", "type": "premium", "distance": 2, "status": "free", "vehicle": None},
    {"id": "B4", "type": "normal", "distance": 5, "status": "free", "vehicle": None},
    # row C
    {"id": "C1", "type": "normal", "distance": 3, "status": "free", "vehicle": None},
    {"id": "C2", "type": "normal", "distance": 6, "status": "free", "vehicle": None},
    {"id": "C3", "type": "ev", "distance": 5, "status": "free", "vehicle": None},
    {"id": "C4", "type": "premium", "distance": 4, "status": "free", "vehicle": None},
    # row D
    {"id": "D1", "type": "normal", "distance": 7, "status": "free", "vehicle": None},
    {"id": "D2", "type": "disabled", "distance": 6, "status": "free", "vehicle": None},
    {"id": "D3", "type": "normal", "distance": 8, "status": "free", "vehicle": None},
    {"id": "D4", "type": "bike", "distance": 5, "status": "free", "vehicle": None},
]

# vehicle number -> slot id
vehicle_table = HashTable()

# slot id -> the slot dict (same objects as in SLOTS)
slot_table = HashTable()
for slot in SLOTS:
    slot_table.put(slot["id"], slot)


def clean_number(number):
    return str(number).strip().upper()


def distance_of(slot):
    return slot["distance"]


def get_state():
    ordered = insertion_sort(SLOTS, distance_of)

    parked = []
    for slot in SLOTS:
        if slot["vehicle"] is not None:
            parked.append({
                "number": slot["vehicle"]["number"],
                "slot_id": slot["id"],
                "type": slot["vehicle"]["type"],
                "priority": slot["vehicle"]["priority"],
            })

    return {
        "slots": SLOTS,
        "by_distance": ordered,
        "parked": parked,
    }


def allocate(number, vtype, priority):
    number = clean_number(number)
    vtype = str(vtype).strip().lower()
    priority = str(priority).strip().lower()

    if number == "":
        return {"ok": False, "message": "Enter the vehicle number"}

    if vtype not in ("car", "bike", "ev"):
        return {"ok": False, "message": "Select a vehicle type"}

    if priority not in ("normal", "disabled", "premium"):
        return {"ok": False, "message": "Select a priority"}

    # hash lookup, so we don't give the same vehicle two slots
    if vehicle_table.get(number) is not None:
        return {"ok": False, "message": "This vehicle is already parked"}

    vehicle = {
        "number": number,
        "type": vtype,
        "priority": priority,
    }

    choice = choose_slot(vehicle, SLOTS)
    if choice is None:
        return {"ok": False, "message": "No suitable slot is free"}

    slot = choice["slot"]
    slot["status"] = "occupied"
    slot["vehicle"] = vehicle
    vehicle_table.put(number, slot["id"])

    return {
        "ok": True,
        "message": "Parked at " + slot["id"] + " (score " + str(choice["score"]) + ")",
        "slot_id": slot["id"],
        "score": choice["score"],
        "compared": choice["compared"],
    }


def release(number):
    number = clean_number(number)
    if number == "":
        return {"ok": False, "message": "Enter the vehicle number"}

    slot_id = vehicle_table.get(number)
    if slot_id is None:
        return {"ok": False, "message": "This vehicle is not in the lot"}

    slot = slot_table.get(slot_id)
    slot["status"] = "free"
    slot["vehicle"] = None
    vehicle_table.remove(number)

    return {"ok": True, "message": "Slot " + slot_id + " is free now"}


def find(number):
    number = clean_number(number)
    if number == "":
        return {"ok": False, "message": "Enter the vehicle number"}

    slot_id = vehicle_table.get(number)
    if slot_id is None:
        return {"ok": False, "message": number + " is not parked"}

    return {"ok": True, "message": number + " is at " + slot_id, "slot_id": slot_id}
