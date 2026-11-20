"""
We are building the backend for an incident alerting service. Each Alert represents a problem raised against a 
monitored service. Times are measured in minutes since the start of the current on-call window.

Definitions:
- An "Alert" is one reported problem for a service. It has an alert_id, a service name, a severity, a created_at 
time, and a resolved_at time.
- If an alert is "open" its resolved_at time is None.
- Once an alert gets resolved, its resolved_at gets set to the time it was resolved.
- Severity is ranked: LOW is the lowest, then MEDIUM, then HIGH, then CRITICAL.
- An "AlertRouter" is the class used to manage all alerts for the on-call window.

To begin with, two tasks:
1.1) Read through and understand the code below. Take as much time as you need, and
   feel free to run the code.
1.2) The test for AlertRouter is not passing due to a bug in the code. Make the
   necessary changes to AlertRouter to fix the bug.
"""
"""
We now want to track our attempts to deliver each alert to an on-call responder. Every time the 
system tries to notify someone about an alert, it records a delivery attempt: which responder 
was contacted, and at what time (in minutes since the start of the window).

Add two methods to AlertRouter:

2.1) record_attempt(alert_id, responder, timestamp): record one delivery attempt for the given
 alert if the alert with given alert_id exists and return True. If there is no alert with that ID, 
 ignore the attempt and return False.

2.2) get_attempt_counts(): return a dictionary of each alert ID to the number of delivery
attempts recorded for it. Only include alerts that have at least one attempt; omit alerts that have none.

Example:

Input (alerts 42 and 77 already exist):
  record_attempt(42, "alice", 5)    -> True
  record_attempt(42, "bob", 30)     -> True
  record_attempt(77, "alice", 10)   -> True
  record_attempt(500, "carol", 0)   -> False   (no alert with ID 500)

Output (returned by get_attempt_counts()):
  {42: 2, 77: 1}

Explanation:
Alert 42 received two delivery attempts and alert 77 received one, so the map reports 2 and 1. The attempt for alert 500 was ignored because no such alert exists, and an alert with no attempts does not appear at all.

The test_record_attempt and test_get_attempt_counts methods are provided.
"""
"""
We are adding a check to catch on-call responders being paged too frequently for the same alert. Our retry policy says that
 any two delivery attempts for the same alert must be at least `cooldown` minutes apart. We want to find the alerts that 
 break this policy.

3.1) Implement get_backoff_violations(cooldown). It returns the IDs of every alert for which at least one pair of consecutive 
attempts, taken in time order, is spaced fewer than `cooldown` minutes apart. The returned IDs must be sorted in ascending order.

Two attempts spaced exactly `cooldown` minutes apart are allowed; only a gap strictly less than `cooldown` is a violation. 
An alert with fewer than two attempts can never break the policy.

Example:

Input:
  alert 1 has attempts recorded at minutes 0, 20, 10
  alert 2 has attempts recorded at minutes 0, 3
  cooldown = 5

Output (returned by get_backoff_violations(5)):
  [2]

Explanation:
Taken in time order, alert 1's attempts are 0, 10, 20, with gaps of 10 and 10 — both at
least 5, so alert 1 is compliant. Alert 2's two attempts are 3 minutes apart, which is
less than 5, so alert 2 breaks the policy.

The test_get_backoff_violations method is provided.
"""
"""
When an alert stays open despite repeated delivery attempts, we escalate it: we hand it to an on-call responder to deal with directly. We want to distribute the escalated alerts across the available responders as evenly as possible, while making sure the most urgent alerts are placed first.

4.1) Implement escalate_alerts(responders, max_attempts). `responders` is a list of responder IDs, given in preference order. An alert is escalated when it is still open and has had at least `max_attempts` delivery attempts recorded. Assign every escalated alert to exactly one responder, and return a dictionary of alert ID to the responder it was assigned to.

Assign the alerts using these rules:
1) Consider the escalated alerts in priority order: highest severity first, then earlier created_at, then smaller alert_id.
2) Each responder carries a load equal to the sum of the severity values of the alerts assigned to them (LOW = 1, MEDIUM = 2, HIGH = 3, CRITICAL = 4). Assign each alert, in the order above, to the responder who currently has the least total load. If two responders are tied, choose the one that appears earlier in the responders list.

Resolved alerts are never escalated, even if they have many attempts. An alert with fewer than `max_attempts` attempts is not escalated. If the responders list is empty, nothing can be assigned, so return an empty dictionary.

Example:

Input (all four alerts are open and each has at least 2 attempts):
  alert 5: CRITICAL, created 10
  alert 6: LOW, created 20
  alert 7: LOW, created 30
  alert 8: LOW, created 40
  responders = ["r1", "r2"], max_attempts = 2

Output (returned by escalate_alerts(["r1", "r2"], 2)):
  {5: "r1", 6: "r2", 7: "r2", 8: "r2"}

Explanation:
In priority order the alerts are 5 (CRITICAL), 6, 7, 8 (all LOW, ordered by created_at). Alert 5 goes to r1, giving r1 a load of 4. Each LOW alert then goes to whichever responder has the least load: r2 has 0, so alerts 6, 7, and 8 all go to r2, bringing its load to 3. The single high-severity alert on r1 is balanced by the three low-severity alerts on r2.

The test_escalate_alerts method is provided.
"""



import unittest
from enum import Enum

class Severity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class Alert:
    """ Data about a single reported problem for a service. """
    def __init__(self, alert_id, service, severity, created_at, resolved_at=None):
        self.alert_id = alert_id
        self.service = service
        self.severity = severity
        self.created_at = created_at        # minutes since the start of the window
        self.resolved_at = resolved_at      # minutes, or None while the alert is open

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (
            self.alert_id == other.alert_id
            and self.service == other.service
            and self.severity == other.severity
            and self.created_at == other.created_at
            and self.resolved_at == other.resolved_at
        )

    def __str__(self):
        return f"Alert {self.alert_id} [{self.service}] {self.severity} created={self.created_at} resolved={self.resolved_at}"

class AlertRouter:
    """
    Data for managing incident alerts, and methods on-call staff use to query them.
    """
    def __init__(self):
        self.alerts = []
        self.attempt_details = {}

    def add_alert(self, alert):
        """Registers an alert for the current on-call window."""
        self.alerts.append(alert)

    def get_alert(self, alert_id):
        """Returns the alert with the given ID, or None if there is no such alert."""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                return alert
        return None

    def has_open_alert(self, service):
        """Returns whether the given service currently has at least one open alert."""
        for alert in self.alerts:
            if alert.service == service and alert.resolved_at is None:
                return True
        return False

    def record_attempt(self, alert_id, responder, timestamp):
        alert_exist = any(alert.alert_id == alert_id for alert in self.alerts)

        # or
        # Initialize our tracker variable as False by default
        alert_exists = False
        # Scan through every alert object in our list one by one
        for alert in self.alerts:
            # If we find an alert whose ID matches the one we are looking for...
            if alert.alert_id == alert_id:
                alert_exists = True  # Switch our tracker to True
                break                # Stop the loop immediately (no need to check the rest!)

        if not alert_exist:
            return False

        if alert_id not in self.attempt_details:
            self.attempt_details[alert_id] = []
        self.attempt_details[alert_id].append(timestamp)
        
        return True
        
    def get_attempt_counts(self):
        return {aid : len(times) for aid, times in self.attempt_details.items() }

    def get_backoff_violations(self,cooldown):
        violations = []
        for id, times in self.attempt_details.items():

            if len(times)< 2:
                continue

            sorted_times = sorted(times)

            for i in range(len(sorted_times) -1):
                gap = sorted_times[i+1]- sorted_times[i]
                if gap < cooldown:
                    violations.append(id)
                    break

        return sorted(violations)

    def escalate_alerts(self, responders, max_attempts):
        """Escalates open alerts with high attempt histories to responders using a load-balancing algorithm."""
        if not responders:
            return {}

        escalation_candidates = []

        # Step 1: Identify eligible escalation candidates
        for alert in self.alerts:
            # Rule: Must be open (resolved_at is None)
            if alert.resolved_at is not None:
                continue
            
            # Fetch total attempts recorded for this alert ID
            attempts = self.attempt_history.get(alert.alert_id, [])
            
            # Rule: Must meet or exceed the maximum attempt boundary threshold limit
            if len(attempts) >= max_attempts:
                escalation_candidates.append(alert)

        # Step 2: Sort candidates in strict priority order
        # Sort Key: 1. Severity Value (Descending), 2. created_at (Ascending), 3. alert_id (Ascending)
        escalation_candidates.sort(key=lambda a: (-a.severity.value, a.created_at, a.alert_id))

        # Step 3: Initialize loads tracking dictionary repository for responders
        responder_loads = {r: 0 for r in responders}
        assignments = {}

        # Step 4: Iteratively distribute alerts targeting the least-loaded individual
        for alert in escalation_candidates:
            # Find the responder with the absolute minimum total load weight value.
            # Python's min() preserves the original list order for tie-breaking.
            chosen_responder = min(responders, key=lambda r: responder_loads[r])
            
            # Log the assignment record mapping
            assignments[alert.alert_id] = chosen_responder
            
            # Add this alert's explicit numeric intensity tier value to the responder's total load weight balance
            responder_loads[chosen_responder] += alert.severity.value

        return assignments


class TestSuite(unittest.TestCase):

    def test_alert(self):
        """Test basic Alert construction."""
        a = Alert(1, "auth", Severity.HIGH, 100)
        self.assertEqual(a.alert_id, 1)
        self.assertEqual(a.service, "auth")
        self.assertEqual(a.severity, Severity.HIGH)
        self.assertEqual(a.created_at, 100)
        self.assertIsNone(a.resolved_at)

    def test_has_open_alert(self):
        router = AlertRouter()
        router.add_alert(Alert(1, "auth", Severity.HIGH, 100, 150))       # resolved
        router.add_alert(Alert(2, "auth", Severity.LOW, 200, None))       # open
        router.add_alert(Alert(3, "billing", Severity.CRITICAL, 50, 90))  # resolved
        router.add_alert(Alert(4, "search", Severity.MEDIUM, 10, None))   # open
        # Harder case: "payments" has two resolved alerts before its only open one,
        # with another service's alert mixed in — the open alert is last in the list.
        router.add_alert(Alert(5, "payments", Severity.CRITICAL, 300, 320))  # resolved
        router.add_alert(Alert(6, "cdn", Severity.LOW, 10, None))            # different service
        router.add_alert(Alert(7, "payments", Severity.HIGH, 330, 360))      # resolved
        router.add_alert(Alert(8, "payments", Severity.MEDIUM, 400, None))   # open

        # "auth" has one resolved and one open alert -> it has an open alert.
        self.assertTrue(router.has_open_alert("auth"))
        # "billing" has only a resolved alert.
        self.assertFalse(router.has_open_alert("billing"))
        self.assertTrue(router.has_open_alert("search"))
        # A service with no alerts at all never has an open alert.
        self.assertFalse(router.has_open_alert("unknown"))
        # "payments" is open only because of its last alert.
        self.assertTrue(router.has_open_alert("payments"))

    def test_record_attempt(self):
        """Test record_attempt."""
        router = AlertRouter()
        router.add_alert(Alert(10, "auth", Severity.HIGH, 0, None))
        router.add_alert(Alert(20, "billing", Severity.LOW, 0, None))

        self.assertTrue(router.record_attempt(10, "alice", 5))
        self.assertTrue(router.record_attempt(10, "bob", 12))
        self.assertTrue(router.record_attempt(20, "alice", 8))

        # No alert with this ID: the attempt should be ignored.
        self.assertFalse(router.record_attempt(999, "alice", 9))

        # Edge case: a resolved alert still exists, so recording an attempt against it
        # must still succeed — record_attempt gates on existence, not on open/resolved.
        router.add_alert(Alert(30, "search", Severity.CRITICAL, 100, 150))  # resolved
        self.assertTrue(router.record_attempt(30, "dave", 200))
        # Recording the same responder again is a separate attempt and still succeeds.
        self.assertTrue(router.record_attempt(10, "alice", 40))

    def test_get_attempt_counts(self):
        """Test get_attempt_counts."""
        router = AlertRouter()
        router.add_alert(Alert(10, "auth", Severity.HIGH, 0, None))
        router.add_alert(Alert(20, "billing", Severity.LOW, 0, None))
        router.add_alert(Alert(30, "search", Severity.MEDIUM, 0, None))  # never attempted

        router.record_attempt(10, "alice", 5)
        router.record_attempt(10, "bob", 12)
        router.record_attempt(10, "alice", 20)
        router.record_attempt(20, "carol", 8)
        router.record_attempt(999, "alice", 9)   # ignored: no such alert

        self.assertEqual(router.get_attempt_counts(), {10: 3, 20: 1})

    def test_get_backoff_violations(self):
        """Test get_backoff_violations."""
        router = AlertRouter()
        for aid in [1, 2, 3, 4, 5]:
            router.add_alert(Alert(aid, "svc" + str(aid), Severity.HIGH, 0, None))

        # cooldown = 5

        # alert 1 -> recorded out of order; in time order 0, 10, 20 (gaps 10, 10) -> compliant
        router.record_attempt(1, "a", 0)
        router.record_attempt(1, "a", 20)
        router.record_attempt(1, "a", 10)
        # alert 2 -> 0, 3 (gap 3 < 5) -> violation
        router.record_attempt(2, "a", 0)
        router.record_attempt(2, "a", 3)
        # alert 3 -> in time order 100, 105, 110 (gaps exactly 5) -> compliant (boundary)
        router.record_attempt(3, "a", 100)
        router.record_attempt(3, "a", 110)
        router.record_attempt(3, "a", 105)
        # alert 4 -> a single attempt -> can never violate
        router.record_attempt(4, "a", 50)
        # alert 5 -> recorded out of order; in time order 0, 4, 9 (gap 4 < 5) -> violation
        router.record_attempt(5, "a", 0)
        router.record_attempt(5, "a", 9)
        router.record_attempt(5, "a", 4)

        self.assertEqual(router.get_backoff_violations(5), [2, 5])

    def test_escalate_alerts(self):
        """Test escalate_alerts."""
        router = AlertRouter()
        # Escalation candidates: open, and at least max_attempts (3) attempts recorded.
        router.add_alert(Alert(100, "auth", Severity.CRITICAL, 10, None))   # load 4
        router.add_alert(Alert(101, "billing", Severity.HIGH, 20, None))    # load 3
        router.add_alert(Alert(102, "search", Severity.HIGH, 20, None))     # load 3 (id tie-break after 101)
        router.add_alert(Alert(103, "cdn", Severity.MEDIUM, 30, None))      # load 2
        router.add_alert(Alert(104, "dns", Severity.LOW, 50, None))         # load 1
        router.add_alert(Alert(105, "queue", Severity.LOW, 40, None))       # load 1 (created tie-break before 104)
        # Excluded from escalation:
        router.add_alert(Alert(200, "auth", Severity.CRITICAL, 5, 60))      # resolved -> never escalated
        router.add_alert(Alert(201, "auth", Severity.HIGH, 15, None))       # below the attempt threshold
        router.add_alert(Alert(202, "auth", Severity.LOW, 0, None))         # no attempts

        for aid in [100, 101, 102, 103, 104, 105]:
            for i in range(3):
                router.record_attempt(aid, "a", i)
        for i in range(5):
            router.record_attempt(200, "a", i)   # exhausted, but the alert is resolved
        for i in range(2):
            router.record_attempt(201, "a", i)   # only two attempts (below threshold)

        # Priority order: 100 (C), 101 (H, id 101), 102 (H, id 102), 103 (M), 105 (L, 40), 104 (L, 50).
        # Least-loaded assignment across ["r1", "r2"]:
        #   100 -> r1 (r1=4), 101 -> r2 (r2=3), 102 -> r2 (r2=6),
        #   103 -> r1 (r1=6), 105 -> r1 (r1=7), 104 -> r2 (r2=7)
        result = router.escalate_alerts(["r1", "r2"], 3)
        self.assertEqual(result, {100: "r1", 101: "r2", 102: "r2", 103: "r1", 105: "r1", 104: "r2"})

        # No responders -> nothing can be routed.
        self.assertEqual(router.escalate_alerts([], 3), {})

        # Single escalation candidate -> goes to the first responder.
        solo = AlertRouter()
        solo.add_alert(Alert(1, "auth", Severity.MEDIUM, 0, None))
        for i in range(3):
            solo.record_attempt(1, "a", i)
        self.assertEqual(solo.escalate_alerts(["r1", "r2"], 3), {1: "r1"})

        # Nothing qualifies (one below threshold, one resolved-but-exhausted) -> empty map.
        none_qualify = AlertRouter()
        none_qualify.add_alert(Alert(1, "auth", Severity.CRITICAL, 0, None))  # open, 1 attempt
        none_qualify.add_alert(Alert(2, "auth", Severity.HIGH, 0, 10))        # resolved, 4 attempts
        none_qualify.record_attempt(1, "a", 0)
        for i in range(4):
            none_qualify.record_attempt(2, "a", i)
        self.assertEqual(none_qualify.escalate_alerts(["r1", "r2"], 3), {})


if __name__ == "__main__":
    unittest.main()
