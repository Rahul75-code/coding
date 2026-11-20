"""
We are building the back-end for a cloud infrastructure platform. The system tracks compute pools, customer reservations, and available compute capacity.


Definitions

A compute pool represents a pool of cloud compute capacity. A compute pool has:
- pool_id
- region
- total_capacity

A reservation represents a customer's reserved compute capacity. A reservation has:
- reservation_id
- customer_id
- pool_id
- capacity_units
- status
- start_time
- end_time

A reservation status is one of:
- ACTIVE
- CANCELLED
- EXPIRED

The ReservationManager class manages compute pools and reservations.

To begin with, we present you with two tasks:
1-1) Read through and understand the code below. Feel free to run it.
1-2) The test for ReservationManager is not passing due to a bug in the code. Make the necessary changes to ReservationManager to fix the bug.
"""
"""
We are extending the platform to support recording reservations and summarizing customer usage.

Add two functions to the ReservationManager class:

2-1) The add_reservation function should store a reservation only if:
- the reservation's pool_id refers to a known compute pool, and
- the reservation's capacity_units is less than or equal to the pool's currently available capacity.

For this question, available capacity means:
pool.total_capacity - total ACTIVE reserved capacity for that pool

If either condition is not met, the reservation should be ignored.

2-2) The get_reserved_capacity_by_customer function should return a dictionary mapping each 
customer ID to the total ACTIVE reserved capacity for that customer.

- Only ACTIVE reservations should be counted.
- Customers with no ACTIVE reservations should not appear in the dictionary.
- If there are no ACTIVE reservations, return an empty dictionary.
"""
"""
We now need to expire reservations whose reservation windows have ended.

Add one function to the ReservationManager class.


3-1) The expire_reservations function takes a current_time and updates reservation statuses according to the following rules:

- Any ACTIVE reservation with end_time less than or equal to current_time should become EXPIRED.
- CANCELLED reservations should remain CANCELLED.
- Reservations that are already EXPIRED should remain EXPIRED.
- ACTIVE reservations with end_time greater than current_time should remain ACTIVE.

The function should return the number of reservations that were changed from ACTIVE to EXPIRED.

After this change, expired reservations should no longer consume capacity. Available capacity should be calculated using only ACTIVE reservations.
"""
"""
A customer may request a large amount of compute capacity in a region. The platform should create a deterministic allocation plan using currently available capacity across pools.

Add one function to the ReservationManager class.

4-1) The get_allocation_plan function takes a region and a requested_capacity.
- It should return a list of [pool_id, allocated_capacity] entries showing how the request would be allocated across pools in that region.

This function should only return a proposed allocation plan. It should not create reservations, update reservation statuses, or modify compute pools.


Allocation Rules

- Only pools in the requested region may be used.
- Available capacity for a pool is calculated as: pool.total_capacity - total ACTIVE reserved capacity for that pool
- Pools with 0 available capacity should be skipped.
- Allocate from pools with the most available capacity first.
- If two pools have the same available capacity, use pool_id ascending as the tiebreaker.
Continue allocating until:
    - the requested capacity is fully satisfied, or
    - no available capacity remains.
- If the total available capacity in the region is less than the requested capacity, return the best partial allocation possible.
- If requested_capacity is less than or equal to 0, return an empty list.
"""



import unittest
from enum import Enum

class ReservationStatus(Enum):
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

class ComputePool:
    def __init__(self, pool_id, region, total_capacity):
        self.pool_id = pool_id
        self.region = region
        self.total_capacity = total_capacity

class Reservation:
    def __init__(self, reservation_id, customer_id, pool_id, capacity_units, status, start_time, end_time):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.pool_id = pool_id
        self.capacity_units = capacity_units
        self.status = status
        self.start_time = start_time
        self.end_time = end_time

class ReservationManager:
    def __init__(self):
        self.compute_pools = {}  # pool_id -> ComputePool
        self.reservations = []   # list of Reservation

    def add_compute_pool(self, compute_pool):
        self.compute_pools[compute_pool.pool_id] = compute_pool

    def get_available_capacity(self, pool_id):
        if pool_id not in self.compute_pools:
            return 0

        pool = self.compute_pools[pool_id]

        used_capacity = sum(
            r.capacity_units
            for r in self.reservations
            if r.pool_id == pool_id 
            and (r.status == ReservationStatus.ACTIVE or r.status == "ACTIVE")
        )

        return pool.total_capacity - used_capacity

    def add_reservation(self, reservation):
        """Validates capacity limits and registers a reservation for known pools."""
        # Condition 1: Check if the pool exists in the platform catalogue
        if reservation.pool_id not in self.compute_pools:
            return
        
        # Condition 2: Check if there is enough available space in the pool right now
        available_cap = self.get_available_capacity(reservation.pool_id)
        if reservation.capacity_units <= available_cap :
            self.reservations.append(reservation)

    def get_reserved_capacity_by_customer(self):
        result = {}

        for rev in self.reservations:
            if rev.status == ReservationStatus.ACTIVE:
                if rev.customer_id not in result:
                    result[rev.customer_id] = 0
                result[rev.customer_id] += rev.capacity_units

        return result

    def expire_reservations(self, cur_time):
        count = 0
        for r in self.reservations:
            if r.status == ReservationStatus.ACTIVE and r.end_time <= cur_time:
                r.status = ReservationStatus.EXPIRED
                count +=1
        return count

    def get_allocation_plan(self, region, requested_capacity):
        """Generates a deterministic allocation blueprint across region pools without altering state."""
        # Rule: If requested_capacity is less than or equal to 0, return an empty list immediately
        if requested_capacity <= 0:
            return []

        pool_candidates = []

        # Step 1: Collect available capacity profiles for all pools in the target region
        for pool in self.compute_pools.values():
            if pool.region == region:
                available = self.get_available_capacity(pool.pool_id)
                # Rule: Pools with 0 available capacity should be skipped
                if available > 0:
                    pool_candidates.append((pool.pool_id, available))

        # Step 2: Sort candidates according to sorting priority rules
        # Sort Key: 1. Available Capacity (Descending via -cap), 2. Pool ID (Ascending via pid)
        pool_candidates.sort(key=lambda item: (-item[1], item[0]))

        allocation_plan = []
        remaining_needed = requested_capacity

        # Step 3: Greedy allocation routing loop
        for pool_id, available_cap in pool_candidates:
            if remaining_needed <= 0:
                break

            # Allocate whichever value is smaller: what we need or what the pool has left
            allocated = min(remaining_needed, available_cap)
            allocation_plan.append([pool_id, allocated])
            remaining_needed -= allocated

        return allocation_plan


class TestSuite(unittest.TestCase):
    def test_get_available_capacity(self):
        print("Running test_get_available_capacity")

        manager = ReservationManager()
        manager.add_compute_pool(ComputePool(1, "us-east", 100))

        manager.reservations.append(
            Reservation(101, 1001, 1, 30, ReservationStatus.ACTIVE, 1000, 2000)
        )

        manager.reservations.append(
            Reservation(102, 1002, 1, 20, ReservationStatus.CANCELLED, 1000, 2000)
        )

        self.assertEqual(70, manager.get_available_capacity(1))
        self.assertEqual(0, manager.get_available_capacity(99))

    def test_add_reservation(self):
        print("Running test_add_reservation")

        manager = ReservationManager()
        manager.add_compute_pool(ComputePool(1, "us-east", 100))

        manager.add_reservation(
            Reservation(201, 1001, 1, 40, ReservationStatus.ACTIVE, 1000, 2000)
        )

        manager.add_reservation(
            Reservation(202, 1002, 1, 70, ReservationStatus.ACTIVE, 1000, 2000)
        )

        manager.add_reservation(
            Reservation(203, 1003, 99, 10, ReservationStatus.ACTIVE, 1000, 2000)
        )

        self.assertEqual(1, len(manager.reservations))
        self.assertEqual(201, manager.reservations[0].reservation_id)


    def test_get_reserved_capacity_by_customer(self):
        print("Running test_get_reserved_capacity_by_customer")

        manager = ReservationManager()
        manager.add_compute_pool(ComputePool(1, "us-east", 200))

        manager.add_reservation(
            Reservation(301, 1001, 1, 30, ReservationStatus.ACTIVE, 1000, 2000)
        )
        manager.add_reservation(
            Reservation(302, 1001, 1, 20, ReservationStatus.ACTIVE, 1000, 2000)
        )
        manager.add_reservation(
            Reservation(303, 1002, 1, 10, ReservationStatus.ACTIVE, 1000, 2000)
        )
        manager.add_reservation(
            Reservation(304, 1003, 1, 50, ReservationStatus.CANCELLED, 1000, 2000)
        )

        result = manager.get_reserved_capacity_by_customer()

        self.assertEqual({1001: 50, 1002: 10}, result)


    def test_expire_reservations(self):
        print("Running test_expire_reservations")

        manager = ReservationManager()
        manager.add_compute_pool(ComputePool(1, "us-east", 500))

        manager.add_reservation(
            Reservation(401, 1001, 1, 10, ReservationStatus.ACTIVE, 100, 1000)
        )
        manager.add_reservation(
            Reservation(402, 1002, 1, 20, ReservationStatus.ACTIVE, 100, 900)
        )
        manager.add_reservation(
            Reservation(403, 1003, 1, 30, ReservationStatus.ACTIVE, 100, 1100)
        )
        manager.add_reservation(
            Reservation(404, 1004, 1, 40, ReservationStatus.CANCELLED, 100, 800)
        )
        manager.add_reservation(
            Reservation(405, 1005, 1, 50, ReservationStatus.EXPIRED, 100, 700)
        )

        changed = manager.expire_reservations(1000)

        self.assertEqual(2, changed)
        self.assertEqual(ReservationStatus.EXPIRED, manager.reservations[0].status)
        self.assertEqual(ReservationStatus.EXPIRED, manager.reservations[1].status)
        self.assertEqual(ReservationStatus.ACTIVE, manager.reservations[2].status)
        self.assertEqual(ReservationStatus.CANCELLED, manager.reservations[3].status)
        self.assertEqual(ReservationStatus.EXPIRED, manager.reservations[4].status)
        self.assertEqual(470, manager.get_available_capacity(1))

    def test_get_allocation_plan_full_request(self):
        print("Running test_get_allocation_plan_full_request")

        manager = ReservationManager()

        manager.add_compute_pool(ComputePool(1, "us-east", 100))
        manager.add_compute_pool(ComputePool(2, "us-east", 80))
        manager.add_compute_pool(ComputePool(3, "us-east", 80))
        manager.add_compute_pool(ComputePool(4, "us-west", 200))

        manager.add_reservation(
            Reservation(501, 1001, 1, 40, ReservationStatus.ACTIVE, 100, 1000)
        )
        manager.add_reservation(
            Reservation(502, 1002, 2, 10, ReservationStatus.ACTIVE, 100, 1000)
        )
        manager.add_reservation(
            Reservation(503, 1003, 3, 10, ReservationStatus.ACTIVE, 100, 1000)
        )

        result = manager.get_allocation_plan("us-east", 120)

        self.assertEqual([[2, 70], [3, 50]], result)


    def test_get_allocation_plan_partial_request(self):
        print("Running test_get_allocation_plan_partial_request")

        manager = ReservationManager()

        manager.add_compute_pool(ComputePool(1, "us-east", 50))
        manager.add_compute_pool(ComputePool(2, "us-east", 30))

        manager.add_reservation(
            Reservation(601, 1001, 1, 20, ReservationStatus.ACTIVE, 100, 1000)
        )
        manager.add_reservation(
            Reservation(602, 1002, 2, 10, ReservationStatus.ACTIVE, 100, 1000)
        )

        result = manager.get_allocation_plan("us-east", 100)

        self.assertEqual([[1, 30], [2, 20]], result)


    def test_get_allocation_plan_ignores_unavailable_and_invalid_request(self):
        print("Running test_get_allocation_plan_ignores_unavailable_and_invalid_request")

        manager = ReservationManager()

        manager.add_compute_pool(ComputePool(1, "us-east", 50))
        manager.add_compute_pool(ComputePool(2, "us-east", 30))
        manager.add_compute_pool(ComputePool(3, "us-west", 100))

        manager.add_reservation(
            Reservation(701, 1001, 1, 50, ReservationStatus.ACTIVE, 100, 1000)
        )

        self.assertEqual([], manager.get_allocation_plan("us-east", 0))
        self.assertEqual([[2, 20]], manager.get_allocation_plan("us-east", 20))


if __name__ == "__main__":
    unittest.main()
