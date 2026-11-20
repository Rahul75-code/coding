"""
We are building a program to manage equipment bookings at a sports facility. The facility has multiple 
pieces of equipment, such as
treadmills and rowing machines, and members can reserve them for specific time periods.

Definitions:
- An "equipment" is an object representing a reservable item. It has properties for the ID and name.
- A "reservation" is an object representing a member booking for a specific piece of equipment over a 
time period. Times are represented
  as integers in minutes from the start of the day.
- A "FacilityManager" is the class used to manage all equipment and reservations.

To begin with, we present you with two tasks:
1-1) Read through and understand the code below. Please take as much time as necessary, and feel free 
to run the code.
1-2) One of the tests is failing due to a bug in the code. Make the necessary changes to FacilityManager
 to fix the bug.
"""
"""
We are updating our system to support richer reservation queries. Facility managers need to look up all active reservations made by a
specific member, and equipment coordinators need a quick summary of how each piece of equipment is being used.

2-1) Add get_reservations_for_member() to FacilityManager.
     This function takes a member's name and returns a list of all their active reservations. If the member has no active reservations, 
     return an empty list.

2-2) Add get_equipment_summary() to FacilityManager.
     This function takes an equipment ID and returns a map with the following keys:
     - "total_reservations": the number of active reservations for that equipment.
     - "total_minutes": the total duration in minutes across all active reservations for that equipment.
     If the equipment has no active reservations, both values should be 0.

To assist you in testing these new functions, we have provided the test_get_reservations_for_member and test_get_equipment_summary 
functions.
"""
"""
The facility requires a minimum turnaround time of 30 minutes between
reservations for the same piece of equipment, to allow for cleaning
and sanitisation between members.

A piece of equipment is unavailable if the requested period overlaps
an active reservation, or if there is less than 30 minutes between
the requested period and any active reservation before or after it.

3) Add get_available_equipment() to FacilityManager.
   This function takes a requested start and end time and returns a
   sorted list of equipment IDs (ascending) that are fully available
   for the requested period, including the required 30-minute turnaround
   on either side.
   If no equipment is available, return an empty list.

To assist you in testing this new function, we have provided the
test_get_available_equipment function.

"""



import unittest
from enum import Enum


class ReservationStatus(Enum):
    """
    ReservationStatus represents the current state of a reservation.
    ACTIVE is the default status when a reservation is created.
    CANCELLED is set when a reservation is cancelled.
    """
    ACTIVE = 1
    CANCELLED = 2


class Equipment:
    """Data about a single piece of reservable equipment."""
    def __init__(self, equipment_id: int, name: str):
        self.equipment_id = equipment_id
        self.name = name

    def __str__(self):
        return "Equipment ID: %d, Name: %s" % (self.equipment_id, self.name)


class Reservation:
    """Data about a single equipment reservation."""
    def __init__(self, reservation_id: int, member_name: str,
                 equipment_id: int, start_time: int, end_time: int):
        self.reservation_id = reservation_id
        self.member_name = member_name
        self.equipment_id = equipment_id
        self.start_time = start_time    # minutes from start of day, e.g. 480 = 8:00 AM
        self.end_time = end_time        # minutes from start of day
        self.status = ReservationStatus.ACTIVE

    def get_duration(self) -> int:
        return self.end_time - self.start_time

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.reservation_id == other.reservation_id

    def __str__(self):
        return (
            "Reservation ID: %d, Member: %s, Equipment ID: %d, "
            "Start: %d, End: %d, Status: %s"
            % (self.reservation_id, self.member_name, self.equipment_id,
               self.start_time, self.end_time, self.status)
        )


class FacilityManager:
    """
    Manages equipment reservations for a sports facility.
    Equipment is identified by equipment_id.
    Reservations are stored and can be queried or cancelled.
    Two reservations conflict if they overlap in time for the same equipment.
    """
    def __init__(self):
        self.equipment_list = []
        self.reservations = []

    def add_equipment(self, equipment: Equipment):
        """Adds a piece of equipment to the facility inventory."""
        self.equipment_list.append(equipment)

    def make_reservation(self, reservation: Reservation) -> bool:
        """
        Makes a reservation if the equipment is available for the requested period.
        Returns True if successfully reserved, False if the equipment is unavailable.
        """
        if not self._is_available(reservation.equipment_id,
                                  reservation.start_time,
                                  reservation.end_time):
            return False
        self.reservations.append(reservation)
        return True

    def _is_available(self, equipment_id: int, start_time: int, end_time: int) -> bool:
        for res in self.reservations:
            if res.equipment_id == equipment_id and res.status == ReservationStatus.ACTIVE:
                if start_time < res.end_time and end_time > res.start_time:
                    return False
        return True

    def cancel_reservation(self, reservation_id: int) -> bool:
        """
        Cancels an active reservation by ID.
        Returns True if found and cancelled, False otherwise.
        """
        for res in self.reservations:
            if res.reservation_id == reservation_id:
                res.status = ReservationStatus.CANCELLED
                return True
        return False

    def get_reservations_for_equipment(self, equipment_id: int) -> list:
        """Returns all active reservations for a given piece of equipment."""
        return [res for res in self.reservations
                if res.equipment_id == equipment_id
                and res.status == ReservationStatus.ACTIVE]

    def get_reservations_for_member(self, member_name: str) -> list:
        """Returns a list of all active reservations matching a specific member's name."""
        return [
            res for res in self.reservations
            if res.member_name == member_name and res.status == ReservationStatus.ACTIVE
        ]

    def get_equipment_summary(self, equipment_id: int) -> dict:
        """Computes a summary of total active bookings and operational minutes for an item."""
        active_res = [
            res for res in self.reservations
            if res.equipment_id == equipment_id and res.status == ReservationStatus.ACTIVE
        ]
        
        # Calculate total duration by calling get_duration() on matching entries
        total_mins = sum(res.get_duration() for res in active_res)
        
        return {
            "total_reservations": len(active_res),
            "total_minutes": total_mins
        }

    def get_available_equipment(self, start_time: int, end_time: int) -> list:
        """Returns a list of equipment IDs sorted in ascending order that are fully available

        during the requested period, ensuring a 30-minute turnaround gap on either side.
        """
        available_ids = []

        # Loop through every piece of equipment registered in the inventory
        for equip in self.equipment_list:
            is_equip_free = True
            
            # Check this equipment against all existing reservations
            for res in self.reservations:
                if res.equipment_id == equip.equipment_id and res.status == ReservationStatus.ACTIVE:
                    # Enforce the 30-minute turnaround policy:
                    # An active reservation cannot start within 30 minutes of our request ending,
                    # AND it cannot end within 30 minutes of our request starting.
                    if start_time < (res.end_time + 30) and end_time > (res.start_time - 30):
                        is_equip_free = False
                        break
            
            if is_equip_free:
                available_ids.append(equip.equipment_id)

        # Return the collection sorted in ascending order
        return sorted(available_ids)


class TestSuite(unittest.TestCase):
    # These tests are not meant to be exhaustive, and primarily show usage.

    def test_make_reservation(self):
        manager = FacilityManager()
        res = Reservation(101, "Alice Johnson", 1, 480, 600)
        self.assertTrue(manager.make_reservation(res))
        self.assertEqual(len(manager.reservations), 1)

    def test_conflict_detected(self):
        manager = FacilityManager()
        res1 = Reservation(101, "Alice Johnson", 1, 480, 600)
        res2 = Reservation(102, "Bob Smith", 1, 540, 660)
        manager.make_reservation(res1)
        self.assertFalse(manager.make_reservation(res2))

    def test_different_equipment_no_conflict(self):
        manager = FacilityManager()
        res1 = Reservation(101, "Alice Johnson", 1, 480, 600)
        res2 = Reservation(102, "Bob Smith", 2, 480, 600)
        self.assertTrue(manager.make_reservation(res1))
        self.assertTrue(manager.make_reservation(res2))

    def test_cancelled_reservation_frees_slot(self):
        manager = FacilityManager()
        res1 = Reservation(101, "Alice Johnson", 1, 480, 600)
        manager.make_reservation(res1)
        manager.cancel_reservation(101)
        # After cancellation, the same slot should be bookable again
        res2 = Reservation(102, "Bob Smith", 1, 480, 600)
        self.assertTrue(manager.make_reservation(res2))

        def test_get_reservations_for_member(self):
        manager = FacilityManager()
        res1 = Reservation(101, "Alice Johnson", 1, 480, 600)
        res2 = Reservation(102, "Bob Smith", 1, 660, 720)
        res3 = Reservation(103, "Alice Johnson", 2, 720, 840)
        res4 = Reservation(104, "Carol White", 2, 480, 540)
        manager.make_reservation(res1)
        manager.make_reservation(res2)
        manager.make_reservation(res3)
        manager.make_reservation(res4)

        alice_res = manager.get_reservations_for_member("Alice Johnson")
        self.assertEqual(len(alice_res), 2)
        self.assertIn(res1, alice_res)
        self.assertIn(res3, alice_res)

        bob_res = manager.get_reservations_for_member("Bob Smith")
        self.assertEqual(len(bob_res), 1)
        self.assertIn(res2, bob_res)

        # Member with no reservations
        self.assertEqual(manager.get_reservations_for_member("David Brown"), [])

        # Cancelled reservations should not appear
        manager.cancel_reservation(101)
        alice_res_after = manager.get_reservations_for_member("Alice Johnson")
        self.assertEqual(len(alice_res_after), 1)
        self.assertIn(res3, alice_res_after)

    def test_get_equipment_summary(self):
        manager = FacilityManager()
        res1 = Reservation(101, "Alice Johnson", 1, 480, 540)
        res2 = Reservation(102, "Bob Smith", 1, 660, 720)
        res3 = Reservation(103, "Carol White", 1, 720, 780)
        res4 = Reservation(104, "David Brown", 2, 480, 600)
        manager.make_reservation(res1)
        manager.make_reservation(res2)
        manager.make_reservation(res3)
        manager.make_reservation(res4)

        summary_e1 = manager.get_equipment_summary(1)
        self.assertEqual(summary_e1["total_reservations"], 3)
        self.assertEqual(summary_e1["total_minutes"], 180)

        summary_e2 = manager.get_equipment_summary(2)
        self.assertEqual(summary_e2["total_reservations"], 1)
        self.assertEqual(summary_e2["total_minutes"], 120)

        # Equipment with no reservations
        summary_e3 = manager.get_equipment_summary(3)
        self.assertEqual(summary_e3["total_reservations"], 0)
        self.assertEqual(summary_e3["total_minutes"], 0)

        # Cancelled reservations should not be counted
        manager.cancel_reservation(101)
        summary_e1_after = manager.get_equipment_summary(1)
        self.assertEqual(summary_e1_after["total_reservations"], 2)
        self.assertEqual(summary_e1_after["total_minutes"], 120)

    def test_get_available_equipment(self):
        manager = FacilityManager()
        equip1 = Equipment(1, "Treadmill")
        equip2 = Equipment(2, "Rowing Machine")
        equip3 = Equipment(3, "Exercise Bike")
        equip4 = Equipment(4, "Elliptical Trainer")
        manager.add_equipment(equip1)
        manager.add_equipment(equip2)
        manager.add_equipment(equip3)
        manager.add_equipment(equip4)

        # equip1: reserved 480-600
        # equip2: reserved 300-420
        # equip3: reserved 700-780
        # equip4: no reservations
        res1 = Reservation(101, "Alice Johnson", 1, 480, 600)
        res2 = Reservation(102, "Bob Smith", 2, 300, 420)
        res3 = Reservation(103, "Carol White", 3, 700, 780)
        manager.make_reservation(res1)
        manager.make_reservation(res2)
        manager.make_reservation(res3)

        # Request: 630-720
        # equip1: res ends 600, gap = 30 min exactly → available
        # equip2: res ends 420, gap = 210 min → available
        # equip3: request overlaps 700-780 from 700-720 → not available
        # equip4: no reservations → available
        result = manager.get_available_equipment(630, 720)
        self.assertEqual(result, [1, 2, 4])

        # Request: 620-720
        # equip1: res ends 600, gap = 20 min → NOT available (under 30-min turnaround)
        # equip2: res ends 420, gap = 200 min → available
        # equip3: res starts 700, within 30 min of request end 720 → not available
        # equip4: no reservations → available
        result2 = manager.get_available_equipment(620, 720)
        self.assertEqual(result2, [2, 4])

        # Cancelled reservations should not block availability
        manager.cancel_reservation(101)
        result3 = manager.get_available_equipment(620, 720)
        self.assertIn(1, result3)

        # No equipment available
        manager2 = FacilityManager()
        equip5 = Equipment(5, "Weight Bench")
        manager2.add_equipment(equip5)
        res4 = Reservation(201, "Alice Johnson", 5, 480, 600)
        manager2.make_reservation(res4)
        self.assertEqual(manager2.get_available_equipment(610, 700), [])

        # Turnaround applies before an existing reservation too
        # Existing res: 600-720. Request 500-580: gap = 20 min → not available
        # Request 500-570: gap = exactly 30 min → available
        manager3 = FacilityManager()
        equip6 = Equipment(6, "Spin Bike")
        manager3.add_equipment(equip6)
        manager3.make_reservation(Reservation(301, "Nina Patel", 6, 600, 720))
        self.assertEqual(manager3.get_available_equipment(500, 580), [])
        self.assertEqual(manager3.get_available_equipment(500, 570), [6])


if __name__ == "__main__":
    unittest.main()
