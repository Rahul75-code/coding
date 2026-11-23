"""
We are building a program to manage a gym's membership. The gym has multiple members, each with a unique ID, name, and membership status.
The program allows gym staff to add new members, update members status, and get membership statistics.

Definitions:
* A "member" is an object that represents a gym member. It has properties for the ID, name, and membership status.
* A "membership" is a class which is used for managing members in the gym.

To begin with, we present you with two tasks:
1-1) Read through and understand the code below. Please take as much time as necessary, and feel free to run the code.
1-2) The test for Membership is not passing due to a bug in the code. Make the necessary changes to Membership to fix the bug.
"""
"""
We are currently updating our system to include information about workouts for our members. As part of this update, 
we have introduced the Workout class, which represents a single workout session for a member. 
Each object of the Workout class has a unique ID, as well as a start time and end time that are represented in the 
number of minutes spent from the start of the day. You can assume that all the Workouts are from the same day.

To implement these changes, we need to add two functions to the Membership class:

2.1) The `add_workout` function takes a member ID and a `Workout` as inputs and associates the workout with that member. 
If the workout is associated successfully, the function should return `True`. 
If the given member does not exist while calling this function, the workout should be ignored and the function should return `False`.

2.2) The `get_average_workout_durations` function should generate a dictionary of member IDs onto 
their average workout durations in minutes. The returned dictionary should include all members. 
If a member has no workouts, their value should be `None`.

To assist you in testing these new functions, we have provided the test_add_workout and test_get_average_workout_durations functions.
"""
"""
We are developing a payment calculation system for our members. The payment amount is determined as follows:

- For members with BRONZE Membership:
  - The first workout is free.
  - From the second workout onwards, each hour costs $10.

- For members with SILVER Membership:
  - The first three workouts are free.
  - From the fourth workout onwards, each hour costs $8.

- For members with GOLD Membership:
  - The first five workouts are free.
  - From the sixth workout onwards, each hour costs $6.

The workouts are ordered by their ID.  
The duration of each workout is always rounded up to the nearest hour. For example, if a person 
spent 80 minutes in a workout, they would be charged for 2 hours.

3) Implement a `get_due_payments` function, which returns a dictionary associating 
each member ID with their due payment.

To help you understand the requirements and test this new function, we have provided the 
`test_get_due_payments` function.
"""
"""
We are developing a gym buddy program to help our members find suitable workout partners. Our analysis has shown that members who spend 
the maximum amount of time working out at the same time are more compatible as gym buddies. To facilitate this, we want to generate a 
sorted list for each member, displaying their potential gym buddies in descending order based on the time they have spent working out 
at the same time.

4) Implement `get_gym_buddies` function in `Membership` class. This function returns a dictionary mapping each member ID to a list of 
(buddy member ID, total overlap duration) pairs, sorted by overlap duration in descending order.

To assist you in understanding the requirements and testing this new function, we have provided the `test_get_gym_buddies` function.
"""



from enum import Enum
import unittest
import math

class MembershipStatus(Enum):
    """
    Membership Status is of three types: BRONZE, SILVER and GOLD.
    BRONZE is the default membership a new member gets.
    SILVER and GOLD are paid memberships for the gym.
    """
    BRONZE = 1
    SILVER = 2
    GOLD = 3

class Member:
    """ Data about a gym member. """
    def __init__(self, member_id: int, name: str, membership_status: MembershipStatus):
        self.member_id = member_id
        self.name = name
        self.membership_status = membership_status

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (
            self.member_id == other.member_id
            and self.name == other.name
            and self.membership_status == other.membership_status
        )
    
    def __str__(self):
        return f"Member ID: {self.member_id}, Name: {self.name}, Membership Status: {self.membership_status}"

class Workout:
    """
    This class represents a single workout session for a member.
    Each object of the Workout class has a unique ID, as well as 
    a start time and end time that are represented in the number 
    of minutes spent from the start of the day.
    """
    def __init__(self, id: int, start_time: int, end_time: int):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time

    def get_duration(self):
        return self.end_time - self.start_time


class Membership:
    """
    Data for managing a gym membership, and methods which staff can
    use to perform any queries or updates.
    """
    def __init__(self):
        self.members = []
        self.workouts = []

    def add_member(self, member: Member):
        """Adds a member to the gym"""
        self.members.append(member)

    def update_membership(self, member_id: int, membership_status: MembershipStatus):
        """Update membership of the given member"""
        for member in self.members:
            if member.member_id == member_id:
                member.membership_status = membership_status
                break

    def get_membership_statistics(self):
        """Calculates and returns membership statistics for all members"""
        total_members = len(self.members)
        total_paid_members = sum(1 for member in self.members if member.membership_status in (MembershipStatus.GOLD, MembershipStatus.SILVER))
        conversion_rate = (total_paid_members / total_members) * 100
        return {
            "total_members": total_members,
            "total_paid_members": total_paid_members,
            "conversion_rate": conversion_rate
        }

    def add_workout(self, member_id: int, workout: Workout) -> bool:
        """Associates a workout session with a specific valid member profile."""
        for member in self.members:
            if member.member_id == member_id:
                member.workouts.append(workout)
                return True
        return False

    def get_average_workout_durations(self) -> dict:
        """Calculates and reports the average workout length for all system members."""
        averages = {}
        for member in self.members:
            if not member.workouts:
                averages[member.member_id] = None
            else:
                total_duration = sum(w.get_duration() for w in member.workouts)
                averages[member.member_id] = total_duration / len(member.workouts)
        return averages

    def get_due_payments(self) -> dict:
        tier_rules = {
            MembershipStatus.BRONZE:(1,10),
            MembershipStatus.SILVER:(3,8),
            MembershipStatus.GOLD:(5,6)
        }
        due_payment={}

        for member in self.members:
            # If a member has no recorded workouts, their balance is always $0
            if not member.workout:
                due_payment[member.member_id] = 0
                continue

            # CRITICAL: Workouts must be evaluated in order of their unique Workout ID
            sorted_workout = sorted(member.workouts, key = lambda w:w.id)

            free_tier, rate = tier_rules[member.membership_status]

            total_due = 0
            for idx, workout in enumerate(sorted_workout):
                if idx < free_tier:
                    continue

                # Calculate billing duration: Convert minutes to hours and round up to the nearest integer hour
                duration_hrs = math.ceil(workout.get_duration/60)
                total_due = duration_hrs*rate
            due_payment[member.member_id] = total_due

        return due_payment

    def get_gym_buddies(self) -> dict:
        """Generates a ranked dictionary mapping each member to their compatible gym buddies."""
        buddies_map = {}
        
        # Initialize an empty tracking array for all registered gym members
        for member in self.members:
            buddies_map[member.member_id] = {}

        # Compute total window overlap duration values between every unique pair of members
        for i in range(len(self.members)):
            for j in range(i + 1, len(self.members)):
                m1 = self.members[i]
                m2 = self.members[j]
                
                total_overlap = 0
                # Compare each individual workout block between the two members
                for w1 in m1.workouts:
                    for w2 in m2.workouts:
                        # Mathematical formula to check overlap between two time intervals
                        overlap = max(0, min(w1.end_time, w2.end_time) - max(w1.start_time, w2.start_time))
                        total_overlap += overlap
                
                # Only map relationships where an actual time overlap occurs (> 0)
                if total_overlap > 0:
                    buddies_map[m1.member_id][m2.member_id] = total_overlap
                    buddies_map[m2.member_id][m1.member_id] = total_overlap

        # Format and sort results for each member
        final_buddies = {}
        for member in self.members:
            mid = member.member_id
            # Convert internal counts map to a list of (buddy_id, overlap_duration) tuples
            buddy_pairs = list(buddies_map[mid].items())
            
            # FIXED/SORTED: Arrange by overlap duration in descending order
            buddy_pairs.sort(key=lambda x: x[1], reverse=True)
            
            final_buddies[mid] = buddy_pairs

        return final_buddies


class TestSuite(unittest.TestCase):
    """ This is not a complete test suite, but tests some basic functionality of
        the code and shows how to use it.
    """
    def test_member(self):
        """Test Bronze Member functionality"""
        test_member = Member(1, "John Doe", MembershipStatus.BRONZE)
        self.assertEqual(test_member.member_id, 1)
        self.assertEqual(test_member.name, "John Doe")
        self.assertEqual(test_member.membership_status, MembershipStatus.BRONZE)

    def test_membership(self):
        test_membership = Membership()
        test_member = Member(1, "John Doe", MembershipStatus.BRONZE)
        test_membership.add_member(test_member)
        self.assertEqual(len(test_membership.members), 1)
        self.assertEqual(test_membership.members[0], test_member)

        test_membership.update_membership(1, MembershipStatus.SILVER)
        self.assertEqual(test_membership.members[0].membership_status, MembershipStatus.SILVER)

        test_member_2 = Member(2, "Alex C", MembershipStatus.BRONZE)
        test_membership.add_member(test_member_2)

        test_member_3 = Member(3, "Marie C", MembershipStatus.GOLD)
        test_membership.add_member(test_member_3)

        test_member_4 = Member(4, "Joe D", MembershipStatus.SILVER)
        test_membership.add_member(test_member_4)

        test_member_5 = Member(5, "June R.", MembershipStatus.BRONZE)
        test_membership.add_member(test_member_5)

        test_member_6 = Member(6, "Westley D.", MembershipStatus.SILVER)
        test_membership.add_member(test_member_6)

        attendance_stats = test_membership.get_membership_statistics()
        self.assertEqual(attendance_stats["total_members"], 6)
        self.assertEqual(attendance_stats["total_paid_members"], 4)
        self.assertAlmostEqual(attendance_stats["conversion_rate"], 66.67, 1)

    def test_add_workout(self):
        """Test add_workout function"""
        test_membership = Membership()
        test_member = Member(12, "John Doe", MembershipStatus.SILVER)
        test_membership.add_member(test_member)
        
        test_member_2 = Member(22, "Alex Cleeve", MembershipStatus.BRONZE)
        test_membership.add_member(test_member_2)

        test_workout_1 = Workout(111, 10, 20)
        test_workout_2 = Workout(112, 15, 35)
        test_workout_3 = Workout(113, 20, 25)
        test_workout_99 = Workout(999, 1, 2)

        self.assertTrue(test_membership.add_workout(12, test_workout_1))
        self.assertTrue(test_membership.add_workout(22, test_workout_2))
        self.assertTrue(test_membership.add_workout(12, test_workout_3))

        # Non-existent member: workout should be ignored.
        self.assertFalse(test_membership.add_workout(404, test_workout_99))

    def test_get_average_workout_durations(self):
        """Test get_average_workout_durations function"""
        test_membership = Membership()
        test_member = Member(12, "John Doe", MembershipStatus.SILVER)
        test_membership.add_member(test_member)
        
        test_member_2 = Member(22, "Alex Cleeve", MembershipStatus.BRONZE)
        test_membership.add_member(test_member_2)

        test_member_3 = Member(31, "Marie Cardiff", MembershipStatus.GOLD)
        test_membership.add_member(test_member_3)

        test_member_4 = Member(37, "George Costanza", MembershipStatus.SILVER)
        test_membership.add_member(test_member_4)
    
        test_workout_1 = Workout(101, 10, 20)
        test_workout_2 = Workout(102, 15, 35)
        test_workout_3 = Workout(103, 45, 90)
        test_workout_4 = Workout(104, 100, 155)
        test_workout_5 = Workout(105, 120, 200)
        test_workout_6 = Workout(106, 300, 400)
        test_workout_7 = Workout(107, 1000, 1010)
        test_workout_8 = Workout(108, 1010, 1045)

        test_membership.add_workout(12, test_workout_1)
        test_membership.add_workout(22, test_workout_2)
        test_membership.add_workout(31, test_workout_3)
        test_membership.add_workout(12, test_workout_4)
        test_membership.add_workout(22, test_workout_5)
        test_membership.add_workout(31, test_workout_6)
        test_membership.add_workout(12, test_workout_7)
        test_membership.add_workout(404, test_workout_8)

        average_durations = test_membership.get_average_workout_durations()
        self.assertAlmostEqual(average_durations[12], 25.0, 1)
        self.assertAlmostEqual(average_durations[22], 50.0, 1)
        self.assertAlmostEqual(average_durations[31], 72.5, 1)
        self.assertIsNone(average_durations[37])
        self.assertNotIn(404, average_durations.keys())

    def test_get_due_payments(self):
        """Test get_due_payments function"""
        test_membership = Membership()
        test_membership.add_member(Member(1, "John Doe", MembershipStatus.BRONZE))
        test_membership.add_member(Member(2, "Alex C", MembershipStatus.SILVER))
        test_membership.add_member(Member(3, "Marie C", MembershipStatus.GOLD))

        # Add workouts for members
        member_workouts = {
            1: [Workout(1, 500, 700), Workout(10, 300, 350), Workout(12, 10, 20), Workout(3, 50, 90), Workout(6, 130, 150), Workout(15, 900, 960)],
            2: [Workout(13, 510, 540), Workout(14, 600, 700), Workout(2, 15, 35), Workout(4, 100, 155), Workout(18, 200, 225), Workout(8, 1050, 1155)],
            3: [Workout(5, 120, 135), Workout(17, 140, 190), Workout(9, 210, 255), Workout(11, 400, 450), Workout(16, 910, 940), Workout(7, 1000, 1100)]
        }
        for member_id, member_workout_list in member_workouts.items():
            for workout in member_workout_list:
                test_membership.add_workout(member_id, workout)

        due_payments = test_membership.get_due_payments()
        self.assertEqual(due_payments[1], 50)
        self.assertEqual(due_payments[2], 32)
        self.assertEqual(due_payments[3], 6)
        
        # Test member with no workouts
        test_membership.add_member(Member(4, "Ron Burgundy", MembershipStatus.SILVER))
        due_payments = test_membership.get_due_payments()
        self.assertEqual(due_payments[4], 0)

    def test_get_gym_buddies(self):
        """Test the get_gym_buddies function"""
        test_membership = Membership()
        
        members = [
            Member(1, "John Doe", MembershipStatus.SILVER),
            Member(2, "Alex C", MembershipStatus.BRONZE),
            Member(3, "Marie C", MembershipStatus.GOLD),
            Member(4, "Jane Smith", MembershipStatus.BRONZE),
        ]
        for member in members:
            test_membership.add_member(member)
        
        test_membership.add_workout(1, Workout(1, 10, 20))
        test_membership.add_workout(2, Workout(2, 15, 60))
        test_membership.add_workout(3, Workout(3, 50, 90))
        test_membership.add_workout(1, Workout(4, 100, 155))
        test_membership.add_workout(2, Workout(5, 120, 200))
        test_membership.add_workout(3, Workout(6, 300, 400))
        test_membership.add_workout(4, Workout(7, 380, 410))
        
        suggested_buddies = test_membership.get_gym_buddies()
        expected_values = {
            1: [(2, 40)],
            2: [(1, 40), (3, 10)],
            3: [(4, 20), (2, 10)],
            4: [(3, 20)]
        }
        for key, value in expected_values.items():
            self.assertEqual(suggested_buddies.get(key), value)

        # Second test case
        test_membership = Membership()
        members = [
            Member(1, "John Doe", MembershipStatus.SILVER),
            Member(2, "Alex C", MembershipStatus.BRONZE),
            Member(3, "Marie C", MembershipStatus.GOLD),
            Member(4, "Jane Smith", MembershipStatus.BRONZE),
            Member(5, "Sarah Johnson", MembershipStatus.SILVER),
            Member(6, "David Brown", MembershipStatus.BRONZE),
            Member(7, "Emily Davis", MembershipStatus.GOLD),
            Member(8, "Michael Wilson", MembershipStatus.BRONZE),
            Member(9, "Olivia Taylor", MembershipStatus.SILVER),
            Member(10, "Daniel Lee", MembershipStatus.BRONZE)
        ]
        for member in members:
            test_membership.add_member(member)
        
        workouts = [
            Workout(i, j, k)
            for i, (j, k) in enumerate(
                [
                    (10, 20), (15, 35), (50, 90), (100, 155), (110, 120),
                    (300, 400), (2000, 2010), (30, 70), (60, 80), (150, 180),
                    (250, 260), (310, 330), (370, 390), (5, 25), (190, 210),
                    (220, 230), (240, 270), (320, 350), (380, 395), (400, 410)
                ]
            )
        ]

        member_workouts = {
            1: [workouts[0], workouts[17]],
            2: [workouts[4], workouts[9], workouts[14]],
            3: [workouts[5]],
            4: [workouts[6], workouts[11]],
            5: [workouts[13], workouts[18]],
            6: [workouts[19]],
            7: [workouts[1], workouts[10], workouts[15]],
            8: [workouts[2], workouts[16]],
            9: [workouts[3], workouts[7], workouts[12]],
            10: [workouts[8]]
        }

        for member_id, member_workout_list in member_workouts.items():
            for workout in member_workout_list:
                test_membership.add_workout(member_id, workout)
        
        # Test gym buddies
        suggested_buddies = test_membership.get_gym_buddies()        
        expected_values = {
            1: [(3, 30), (4, 10), (5, 10), (7, 5)],
            2: [(9, 15)],
            3: [(1, 30), (4, 20), (9, 20), (5, 15)],
            4: [(3, 20), (1, 10)],
            5: [(3, 15), (1, 10), (7, 10), (9, 10)],
            6: [],
            7: [(5, 10), (8, 10), (1, 5), (9, 5)],
            8: [(9, 20), (10, 20), (7, 10)],
            9: [(3, 20), (8, 20), (2, 15), (5, 10), (10, 10), (7, 5)],
            10: [(8, 20), (9, 10)]
        }
        for key, value in expected_values.items():
            self.assertEqual(suggested_buddies.get(key), value)

if __name__ == "__main__":
    unittest.main()
