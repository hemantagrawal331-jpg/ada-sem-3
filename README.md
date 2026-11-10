# Smart Parking Space Allocator

Semester 3 - Analysis and Design of Algorithms

Team
- Hemant Agrawal - 25293916039
- Anubhav - 25293916018

## Run

From this folder:

```
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Files

- `algorithms/min_heap.py` - priority queue, smallest score comes out first
- `algorithms/greedy.py` - scores the free slots and takes the best one for this vehicle
- `algorithms/hashing.py` - vehicle number to slot id, used on exit and find
- `algorithms/sorting.py` - insertion sort, used to list slots by distance
- `parking_lot.py` - the bays, allocate and exit
- `app.py` - Flask routes
- `templates/index.html`, `static/style.css`, `static/script.js` - the page

## Score

Score starts as the distance from the gate (1 is nearest).

- disabled driver, slot is not a disabled bay: add 20
- electric vehicle, slot is not a charging bay: add 6
- premium driver, slot is not a premium bay: add 6

20 is more than any distance in the lot, so a free disabled bay is always chosen for a disabled driver. 6 means a charging or premium bay is chosen when it is not much farther than a normal bay.

Disabled, EV, premium and bike bays are reserved. A normal car only gets a normal bay.

## Quick check

1. Car, Normal -> A2 (nearest normal bay). A1 is kept for disabled drivers.
2. Another Car, Normal -> C1. A4 is the next box in the row, but its distance is 4 and C1 is 3.
3. Electric, Normal -> A3 (charging bay, score 3, beats A2 which scores 1+6)
4. Car, Disabled -> A1
5. Car, Premium -> B3
6. Bike, Normal -> B1
7. Find and exit with the same vehicle number
