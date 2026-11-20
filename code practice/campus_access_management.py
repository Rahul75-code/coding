"""
We are building a system to manage physical access to a corporate campus. Each user has a unique ID, 
a name, and an access level. Access levels are ranked: VISITOR is the lowest, STAFF is higher, and 
ADMIN is the highest. A user is authorized for a required access level when their own level is the 
same or higher — so an ADMIN is authorized for STAFF and VISITOR areas, and a STAFF user is authorized 
for VISITOR areas.

Definitions:
* A "user" is an object representing someone with campus access. It has a user_id, a name,
  and an access_level.
* VISITOR is the default access level a new user receives.
* An "AccessManager" is the class used to manage all users on the campus.

To begin with, two tasks:
1-1) Read through and understand the code below. Take as much time as you need, and
   feel free to run the code.
1-2) The test for AccessManager is not passing due to a bug in the code. Make the
   necessary changes to AccessManager to fix the bug.

"""
"""
We are extending the system to record building access. The new AccessEvent class
represents one badge-in/badge-out session for a user. Each event has a unique ID, an entry_time, 
and an exit_time, all measured in minutes since the start of the day. All events happen on the same day.

The campus is open from minute 480 (08:00) to minute 1200 (20:00). An event is
"after-hours" if it starts before 480 or ends after 1200. Starting exactly at 480 or ending exactly 
at 1200 still counts as within hours.

Add two methods to AccessManager:

2.1) log_access(user_id, event): add the event to that user. Return True if the user
   exists. If the user does not exist, ignore the event and return False.

2.2) get_after_hours_users(): return the IDs of all users who have at least one
   after-hours event, sorted in ascending order. Do not include a user who has no
   after-hours events, including a user with no events at all.

The test_log_access and test_get_after_hours_users tests are provided.
"""
"""
We are adding a building utilization report. For capacity planning we want to know, for each hour of the 
day, how many distinct users were present in the building during that hour.
The day is divided into 24 one-hour buckets: hour h covers the minutes 
from h*60 up to (but not including) (h+1)*60.

For example, hour 0 is minutes 0–59, hour 1 is minutes 60–119, and so on. A user is "present during 
hour h" if any of their access events overlaps that hour. A session that ends exactly on an hour 
boundary does not count as present in the next hour (an event covering minutes 120–180 is present 
in hour 2 only, not hour 3).

3.1) Implement a function get_hourly_occupancy(). It takes no arguments (other than self) and returns a 
dictionary mapping each hour to the number of distinct users present during that hour. Only include 
hours that have at least one user present; omit hours with no users.

Example:

Input:
  user 20 has one session: minute 130 to 260
  user 21 has one session: minute 200 to 230

Output (returned by get_hourly_occupancy()):
  {2: 1, 3: 2, 4: 1}

Explanation:
User 20's session covers hour 2 (minutes 120–180), hour 3 (180–240), and hour 4
(240–300). User 21's session falls entirely within hour 3. Hour 3 therefore has two users present, while hours 2 and 4 each have only user 20, giving {2: 1, 3: 2, 4: 1}.

The test_get_hourly_occupancy test is provided.
"""



import unittest
from enum import Enum


class AccessLevel(Enum):
    VISITOR = 1
    STAFF = 2
    ADMIN = 3


class User:
    """ Data about a campus user. """
    def __init__(self, user_id: int, name: str, access_level: AccessLevel):
        self.user_id = user_id
        self.name = name
        self.access_level = access_level

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (
            self.user_id == other.user_id
            and self.name == other.name
            and self.access_level == other.access_level
        )

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self.name}, Access Level: {self.access_level}"

class AccessEvent:
    """
    A single badge-in/badge-out session for a user. Has a unique ID and an entry
    and exit time, each measured in minutes since the start of the day.
    """
    def __init__(self, id: int, entry_time: int, exit_time: int):
        self.id = id
        self.entry_time = entry_time
        self.exit_time = exit_time


class AccessManager:
    """
    Data for managing campus access, and methods staff use to query or update it.
    """
    def __init__(self):
        self.users = []

    def add_user(self, user: User):
        """Registers a user on the campus."""
        self.users.append(user)

    def update_access_level(self, user_id: int, access_level: AccessLevel):
        """Updates the access level of the given user."""
        for user in self.users:
            if user.user_id == user_id:
                user.access_level = access_level
                break

    def is_authorized(self, user_id: int, required_level: AccessLevel):
        """Returns whether the given user is authorized for the required access level."""
        for user in self.users:
            if user.user_id == user_id:
                return user.access_level >= required_level.value
        return False

    def log_access(self, user_id, event):
        """Logs an access event to a user if they exist within the platform repository."""
        # Check if the user profile exists in the manager database catalogue
        if user_id not in self.users:
            return False
        
        # Append the session event history block
        self.users[user_id].events.append(event)
        return True

    def get_after_hours_users(self): 
        """Returns ascending-sorted user IDs who logged at least one after-hours session."""
        after_hours_user_ids = []

        for user_id, user in self.users.items():
            for event in user.events:
                # Rule: After-hours means starting before 480 or ending after 1200
                if event.entry_time < 480 or event.exit_time > 1200:
                    after_hours_user_ids.append(user_id)
                    break  # One event is sufficient to qualify this user

        # Return sorted IDs in ascending order
        return sorted(after_hours_user_ids)

    def get_hourly_occupancy(self):
        """Returns a map of each hour to the count of unique users present, omitting empty hours."""
        # Map hour (int) -> set of user_ids to guarantee distinct user counting
        hourly_users = {}

        # Loop through all 24 hours of the day
        for h in range(24):
            hour_start = h * 60
            hour_end = (h + 1) * 60
            
            for user_id, user in self.users.items():
                for event in user.events:
                    # Check for overlap: session starts before hour ends AND ends after hour starts
                    if event.entry_time < hour_end and event.exit_time > hour_start:
                        if h not in hourly_users:
                            hourly_users[h] = set()
                        hourly_users[h].add(user_id)

        # Convert the sets into a dictionary showing only total user counts
        # This naturally excludes hours that have no registered user entries
        return {h: len(users) for h, users in hourly_users.items()}


class TestSuite(unittest.TestCase):

    def test_user(self):
        """Test VISITOR user functionality."""
        u = User(1, "John Doe", AccessLevel.VISITOR)
        self.assertEqual(u.user_id, 1)
        self.assertEqual(u.name, "John Doe")
        self.assertEqual(u.access_level, AccessLevel.VISITOR)

    def test_is_authorized(self):
        manager = AccessManager()
        manager.add_user(User(1, "Vera Visitor", AccessLevel.VISITOR))
        manager.add_user(User(2, "Sam Staff", AccessLevel.STAFF))
        manager.add_user(User(3, "Ada Admin", AccessLevel.ADMIN))

        # A user is authorized for their own level and for any lower level.
        self.assertTrue(manager.is_authorized(1, AccessLevel.VISITOR))
        self.assertFalse(manager.is_authorized(1, AccessLevel.STAFF))
        self.assertTrue(manager.is_authorized(2, AccessLevel.STAFF))
        self.assertTrue(manager.is_authorized(2, AccessLevel.VISITOR))
        self.assertFalse(manager.is_authorized(2, AccessLevel.ADMIN))
        self.assertTrue(manager.is_authorized(3, AccessLevel.ADMIN))
        self.assertTrue(manager.is_authorized(3, AccessLevel.VISITOR))

        # An unknown user is never authorized.
        self.assertFalse(manager.is_authorized(999, AccessLevel.VISITOR))

    def test_log_access(self):
        """Test log_access."""
        manager = AccessManager()
        manager.add_user(User(12, "John Doe", AccessLevel.STAFF))
        manager.add_user(User(22, "Alex Cleeve", AccessLevel.VISITOR))

        e1 = AccessEvent(111, 10, 20)
        e2 = AccessEvent(112, 15, 35)
        e3 = AccessEvent(113, 20, 25)
        e99 = AccessEvent(999, 1, 2)

        self.assertTrue(manager.log_access(12, e1))
        self.assertTrue(manager.log_access(22, e2))
        self.assertTrue(manager.log_access(12, e3))

        # Non-existent user: event should be ignored.
        self.assertFalse(manager.log_access(404, e99))

    def test_get_after_hours_users(self):
        """Test get_after_hours_users."""
        manager = AccessManager()
        manager.add_user(User(30, "Late Leaver", AccessLevel.ADMIN))
        manager.add_user(User(10, "Early Bird", AccessLevel.STAFF))
        manager.add_user(User(50, "No Shows", AccessLevel.VISITOR))
        manager.add_user(User(40, "On The Dot", AccessLevel.STAFF))
        manager.add_user(User(20, "Nine To Five", AccessLevel.VISITOR))

        # user 30 -> single event enters in-hours but exits after closing (1250 > 1200)
        manager.log_access(30, AccessEvent(505, 1150, 1250))
        # user 10 -> one event starts before opening (400 < 480): after-hours
        manager.log_access(10, AccessEvent(501, 400, 450))
        manager.log_access(10, AccessEvent(502, 500, 600))
        # user 20 -> both events within hours
        manager.log_access(20, AccessEvent(503, 600, 700))
        manager.log_access(20, AccessEvent(504, 800, 1100))
        # user 40 -> single event exactly on the boundary (opens 480, closes 1200): within hours
        manager.log_access(40, AccessEvent(506, 480, 1200))
        # user 50 -> no events

        after_hours = manager.get_after_hours_users()
        self.assertEqual(after_hours, [10, 30])

    def test_get_hourly_occupancy(self):
        """Test get_hourly_occupancy."""
        manager = AccessManager()
        manager.add_user(User(1, "Spanner", AccessLevel.STAFF))
        manager.add_user(User(2, "Midday", AccessLevel.VISITOR))
        manager.add_user(User(3, "Edge", AccessLevel.ADMIN))
        manager.add_user(User(4, "Solo", AccessLevel.STAFF))
        manager.add_user(User(5, "Absent", AccessLevel.VISITOR))

        # user 1 -> one session that spans hours 1, 2, and 3
        manager.log_access(1, AccessEvent(701, 90, 200))
        # user 2 -> two events, both in hour 2; user 2 must still count once for hour 2
        manager.log_access(2, AccessEvent(702, 130, 150))
        manager.log_access(2, AccessEvent(705, 155, 170))
        # user 3 -> hour 3 only; exits exactly on the hour-4 boundary (240), so not hour 4
        manager.log_access(3, AccessEvent(703, 180, 240))
        # user 4 -> hour 5 only; entry (300) and exit (360) fall exactly on hour boundaries
        manager.log_access(4, AccessEvent(704, 300, 360))
        # user 5 -> no events

        occupancy = manager.get_hourly_occupancy()
        self.assertEqual(occupancy, {1: 1, 2: 2, 3: 2, 5: 1})


if __name__ == "__main__":
    unittest.main()
