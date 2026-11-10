# Greedy allocation.
# For the vehicle that just arrived, pick the best free slot right now.
# We do not keep a slot aside for a vehicle that might come later.
# The min heap is only there to take out the lowest score.

from algorithms.min_heap import MinHeap


def can_park(vehicle, slot):
    if slot["status"] != "free":
        return False

    vtype = vehicle["type"]
    priority = vehicle["priority"]
    stype = slot["type"]

    # bike bays and bikes only match each other
    if vtype == "bike" or stype == "bike":
        return vtype == "bike" and stype == "bike"

    # these bays stay reserved
    if stype == "disabled":
        return priority == "disabled"
    if stype == "ev":
        return vtype == "ev"
    if stype == "premium":
        return priority == "premium"

    # normal bay: any car can use it
    return True


def slot_score(vehicle, slot):
    # lower score is a better slot
    score = slot["distance"]

    # bikes have only one kind of bay, so closest bike bay wins
    if vehicle["type"] == "bike":
        return score

    # add a penalty when the vehicle does not get its preferred bay
    # 20 is bigger than any distance in this lot, so a free disabled bay
    # always beats a normal bay for a disabled driver
    if vehicle["priority"] == "disabled":
        if slot["type"] != "disabled":
            score = score + 20
    elif vehicle["type"] == "ev":
        if slot["type"] != "ev":
            score = score + 6
    elif vehicle["priority"] == "premium":
        if slot["type"] != "premium":
            score = score + 6

    return score


def choose_slot(vehicle, slots):
    # score depends on this vehicle, so a fresh heap is built every time
    heap = MinHeap()
    compared = []

    for slot in slots:
        if not can_park(vehicle, slot):
            continue

        score = slot_score(vehicle, slot)
        heap.insert((score, slot["id"], slot))
        compared.append({
            "id": slot["id"],
            "type": slot["type"],
            "distance": slot["distance"],
            "score": score,
        })

    if heap.is_empty():
        return None

    best = heap.extract_min()
    return {
        "slot": best[2],
        "score": best[0],
        "compared": compared,
    }
