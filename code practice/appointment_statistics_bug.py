"""
We are building the back-end for a clinic appointment management system.
The system tracks doctors and appointments.

Definitions:
* A "doctor" has: doctor_id, name.
* An "appointment" has: appointment_id, doctor_id, patient_id,
  duration_minutes, status, appointment_type.
* AppointmentStatus is one of: SCHEDULED, COMPLETED, CANCELLED, NO_SHOW.
* AppointmentType is one of: CONSULTATION, FOLLOWUP, EMERGENCY.
* "ClinicManager" manages doctors, appointments, and provides statistics.

To begin with, we present you with two tasks:
1-1) Read through and understand the code below. Feel free to run it.
1-2) The test for ClinicManager is not passing due to a bug in the code.
     Make the necessary changes to ClinicManager to fix the bug.
"""
"""
We are extending the platform to report on appointment durations by type.

Recall that each Appointment carries an appointment_type, one of
CONSULTATION, FOLLOWUP, EMERGENCY.

Add a new function to the ClinicManager class:

2) The get_average_appointment_duration_by_type function should return a
   dictionary mapping each appointment type (CONSULTATION, FOLLOWUP,
   EMERGENCY) to the doctor's average appointment duration in minutes for
   that type. Only appointments with a COMPLETED status should be counted;
   ignore appointments with any other status. Only appointment types the
   doctor has at least one completed appointment for should appear in the
   dictionary. If the doctor has no completed appointments at all, return
   an empty dictionary.

To assist you in testing this new function, we have provided the
test_get_average_appointment_duration_by_type test.
"""
"""
We want to generate an appointment activity summary for each doctor in the system.

For each doctor, the summary captures how busy they are overall and
what kind of appointments they handle most often.

We have added a DoctorAppointmentSummary class to represent this summary:
- total_appointments       : total number of appointments for that doctor
- total_minutes            : sum of all appointment duration_minutes for that doctor
- busiest_appointment_type : the appointment type with the most appointments
                             for that doctor. If two appointment types are
                             tied, pick the one that comes first
                             alphabetically. If the doctor has no
                             appointments, set this to None.

Add one function to the ClinicManager class:

3) The get_doctor_appointment_summary function returns a dictionary mapping
   each doctor_id to that doctor's DoctorAppointmentSummary.
   All of a doctor's appointments count toward the summary regardless of
   status. The result should include every doctor in the system, including
   doctors who have no appointments. For doctors with no appointments, return
   a summary with total_appointments = 0, total_minutes = 0, and
   busiest_appointment_type = None.

To assist you in testing this new function, we have provided the
test_get_doctor_appointment_summary test.
"""
"""
We want to rank doctors by their overall workload and identify the
patient who has the most appointments with each of them.

Add one function to the ClinicManager class:

4) The get_doctor_workload_ranking function takes a number k and
   returns a list of [doctor_id, total_minutes, most_frequent_patient_id]
   entries — one for each qualifying doctor.
   For each doctor with at least one appointment:
   - total_minutes is the sum of all appointment duration_minutes for
     that doctor.
   - most_frequent_patient_id is the patient_id with the most
     appointments with that doctor. If two patients have equal
     appointment counts, pick the smaller patient_id.
   Only include doctors who have at least one appointment.
   The returned list should be sorted by total_minutes in descending
   order, with doctor_id ascending as a tiebreaker.
   Return only the top k entries.
   If k is less than or equal to 0, return an empty list.

To assist you in testing this new function, we have provided the
test_get_doctor_workload_ranking_case1 and
test_get_doctor_workload_ranking_case2 tests.
"""


import unittest
from enum import Enum


class AppointmentStatus(Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"


class AppointmentType(Enum):
    CONSULTATION = "CONSULTATION"
    FOLLOWUP = "FOLLOWUP"
    EMERGENCY = "EMERGENCY"


class Doctor:
    def __init__(self, doctor_id, name):
        self.doctor_id = doctor_id
        self.name = name


class Appointment:
    def __init__(self, appointment_id, doctor_id, patient_id,
                 duration_minutes, status, appointment_type):
        self.appointment_id = appointment_id
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.duration_minutes = duration_minutes
        self.status = status
        self.appointment_type = appointment_type


class AppointmentStats:
    def __init__(self, total_appointments, completed_appointments, no_show_rate):
        self.total_appointments = total_appointments
        self.completed_appointments = completed_appointments
        self.no_show_rate = no_show_rate

class DoctorAppointmentSummary:
    def __init__(self, total_appointments, total_minutes, busiest_appointment_type):
        self.total_appointments = total_appointments
        self.total_minutes = total_minutes
        self.busiest_appointment_type = busiest_appointment_type


class ClinicManager:
    def __init__(self):
        self.doctors = {}        # doctor_id -> Doctor
        self.appointments = []   # list of Appointment

    def add_doctor(self, doctor):
        self.doctors[doctor.doctor_id] = doctor

    def add_appointment(self, appointment):
        if appointment.doctor_id not in self.doctors:
            return
        self.appointments.append(appointment)

    def get_appointment_statistics(self):
        total = len(self.appointments)

        completed = sum(
            1 for a in self.appointments
            if a.status == AppointmentStatus.COMPLETED
        )

        no_shows = sum(
            1 for a in self.appointments
            if a.status == AppointmentStatus.NO_SHOW
        )

        no_show_rate = no_shows / total if total > 0 else 0.0

        return AppointmentStats(total, completed, no_show_rate)

    def get_average_appointment_duration_by_type(self, doctor_id):
        ap_duration = {}

        for ap in self.appointments:
            # Step 1: Only look at appointments that match our criteria
            if ap.doctor_id == doctor_id and ap.status == AppointmentStatus.COMPLETED:
                appt_type = ap.appointment_type
                
                # FIX 2: Check if key does not exist using 'not in'
                if appt_type not in ap_duration:
                    ap_duration[appt_type] = []
                    
                ap_duration[appt_type].append(ap.duration_minutes)
            
            # FIX 1: Removed the 'else: return {}' block entirely. 
            # We just let the loop continue scanning all appointments.

        # FIX: Handle doctors who have zero completed appointments safely
        if not ap_duration:
            return {}

        avg_ap_d = {}
        for appt_type, durations in ap_duration.items():
            avg = sum(durations) / len(durations)
            avg_ap_d[appt_type] = avg

        return avg_ap_d

# or

    def get_average_appointment_duration_by_type(self, doctor_id):
        # Gather completed appointments for the given doctor
        completed_appointments = [
            a for a in self.appointments 
            if a.doctor_id == doctor_id and a.status == AppointmentStatus.COMPLETED
        ]

        if not completed_appointments:
            return {}

        # Step 1: Group durations by appointment type
        type_groups = {}
        for appt in completed_appointments:
            if appt.appointment_type not in type_groups:
                type_groups[appt.appointment_type] = []
            type_groups[appt.appointment_type].append(appt.duration_minutes)

        # Step 2: Calculate averages via dict comprehension before returning
        return {
            appt_type: sum(durations) / len(durations)
            for appt_type, durations in type_groups.items()
        }

    def get_doctor_appointment_summary(self):
        summary_map = {}

        # Step 1: Pre-populate summaries for all registered doctors
        for doctor_id in self.doctors:
            summary_map[doctor_id] = {
                "total_appointments": 0,
                "total_minutes": 0,
                "type_counts": {}
            }

        # Step 2: Accumulate appointment metrics globally across all statuses
        for appt in self.appointments:
            if appt.doctor_id in summary_map:
                doc_stats = summary_map[appt.doctor_id]
                doc_stats["total_appointments"] += 1
                doc_stats["total_minutes"] += appt.duration_minutes
                
                # Track frequencies per appointment category type
                appt_type = appt.appointment_type
                if appt_type not in doc_stats["type_counts"]:
                    doc_stats["type_counts"][appt_type] = 0
                doc_stats["type_counts"][appt_type] += 1

        # Step 3: Compute final busiest type handling tiebreaks alphabetically
        final_summary = {}
        for doctor_id, stats in summary_map.items():
            busiest_type = None
            
            if stats["type_counts"]:
                # Sort criteria: Count descending (-count), then Enum string value ascending
                # Using .value extraction handles string alphabetical comparisons smoothly
                busiest_type = min(
                    stats["type_counts"].keys(),
                    key=lambda t: (-stats["type_counts"][t], t.value)
                )

            # Map the aggregated values back into the DoctorAppointmentSummary object
            final_summary[doctor_id] = DoctorAppointmentSummary(
                total_appointments=stats["total_appointments"],
                total_minutes=stats["total_minutes"],
                busiest_appointment_type=busiest_type
            )

        return final_summary

    def get_doctor_workload_ranking(self, k):
        # Guard clause for invalid rank cap parameters
        if k <= 0:
            return []

        doctor_data = {}

        # Step 1: Accumulate total workloads and patient metrics for each appointment
        for appt in self.appointments:
            did = appt.doctor_id
            pid = appt.patient_id
            
            if did not in doctor_data:
                doctor_data[did] = {
                    "total_minutes": 0,
                    "patient_counts": {}
                }
                
            doctor_data[did]["total_minutes"] += appt.duration_minutes
            
            # Map patient interaction frequencies
            counts = doctor_data[did]["patient_counts"]
            counts[pid] = counts.get(pid, 0) + 1

        ranking_list = []

        # Step 2: Establish the most frequent patient for each qualifying doctor
        for did, data in doctor_data.items():
            patient_counts = data["patient_counts"]
            
            # Find the most frequent patient; handle ties by selecting the smaller patient_id
            # Sort order criteria: Count descending (-count), then patient_id ascending (pid)
            most_frequent_patient_id = min(
                patient_counts.keys(),
                key=lambda p: (-patient_counts[p], p)
            )
            
            ranking_list.append([did, data["total_minutes"], most_frequent_patient_id])

        # Step 3: Rank doctors by total_minutes DESC (-x[1]), then doctor_id ASC (x[0])
        ranking_list.sort(key=lambda x: (-x[1], x[0]))

        # Return capped at the top k elements
        return ranking_list[:k]


class TestSuite(unittest.TestCase):
    def test_get_appointment_statistics(self):
        print("Running test_get_appointment_statistics")
        cm = ClinicManager()
        cm.add_doctor(Doctor(10, "dr_smith"))

        cm.add_appointment(Appointment(1, 10, 100, 30, AppointmentStatus.COMPLETED, AppointmentType.CONSULTATION))
        cm.add_appointment(Appointment(2, 10, 101, 45, AppointmentStatus.COMPLETED, AppointmentType.FOLLOWUP))
        cm.add_appointment(Appointment(3, 10, 102, 30, AppointmentStatus.NO_SHOW, AppointmentType.EMERGENCY))
        cm.add_appointment(Appointment(4, 10, 103, 60, AppointmentStatus.CANCELLED, AppointmentType.CONSULTATION))
        cm.add_appointment(Appointment(5, 10, 104, 30, AppointmentStatus.SCHEDULED, AppointmentType.FOLLOWUP))

        stats = cm.get_appointment_statistics()
        self.assertEqual(5, stats.total_appointments)
        self.assertEqual(2, stats.completed_appointments)
        self.assertAlmostEqual(0.2, stats.no_show_rate, places=4)

    def test_get_average_appointment_duration_by_type(self):
        print("Running test_get_average_appointment_duration_by_type")
        cm = ClinicManager()
        cm.add_doctor(Doctor(1, "dr_smith"))
        cm.add_doctor(Doctor(2, "dr_jones"))

        cm.add_appointment(Appointment(1, 1, 100, 30, AppointmentStatus.COMPLETED, AppointmentType.CONSULTATION))
        cm.add_appointment(Appointment(2, 1, 101, 41, AppointmentStatus.COMPLETED, AppointmentType.CONSULTATION))
        cm.add_appointment(Appointment(3, 1, 102, 20, AppointmentStatus.COMPLETED, AppointmentType.FOLLOWUP))
        # not COMPLETED -> excluded from averages
        cm.add_appointment(Appointment(5, 1, 105, 100, AppointmentStatus.CANCELLED, AppointmentType.CONSULTATION))
        cm.add_appointment(Appointment(4, 2, 103, 40, AppointmentStatus.COMPLETED, AppointmentType.EMERGENCY))

        avg1 = cm.get_average_appointment_duration_by_type(1)
        self.assertAlmostEqual(35.5, avg1[AppointmentType.CONSULTATION], places=4)  # (30+41)/2
        self.assertAlmostEqual(20.0, avg1[AppointmentType.FOLLOWUP],     places=4)
        self.assertNotIn(AppointmentType.EMERGENCY, avg1)

        avg2 = cm.get_average_appointment_duration_by_type(2)
        self.assertAlmostEqual(40.0, avg2[AppointmentType.EMERGENCY], places=4)
        self.assertNotIn(AppointmentType.CONSULTATION, avg2)
        self.assertNotIn(AppointmentType.FOLLOWUP,     avg2)

        # doctor with no appointments
        cm.add_doctor(Doctor(3, "dr_brown"))
        self.assertEqual({}, cm.get_average_appointment_duration_by_type(3))

        # unknown doctor_id -> empty dictionary
        self.assertEqual({}, cm.get_average_appointment_duration_by_type(999))

    def test_get_doctor_appointment_summary(self):
        print("Running test_get_doctor_appointment_summary")
        cm = ClinicManager()
        for did in [1, 2, 3, 4]:
            cm.add_doctor(Doctor(did, f"doctor{did}"))

        # doctor 1: 4 appointments, 125 total minutes
        # CONSULTATION x2, FOLLOWUP x1, EMERGENCY x1
        # busiest = CONSULTATION (2 appointments, clear winner)
        cm.add_appointment(Appointment(1, 1, 100, 30, AppointmentStatus.COMPLETED, AppointmentType.CONSULTATION))
        cm.add_appointment(Appointment(2, 1, 101, 45, AppointmentStatus.COMPLETED, AppointmentType.CONSULTATION))
        cm.add_appointment(Appointment(3, 1, 102, 20, AppointmentStatus.COMPLETED, AppointmentType.FOLLOWUP))
        cm.add_appointment(Appointment(4, 1, 103, 30, AppointmentStatus.COMPLETED, AppointmentType.EMERGENCY))

        # doctor 2: 2 appointments, 90 total minutes
        # FOLLOWUP x1, EMERGENCY x1 — tied
        # tiebreak alphabetically -> EMERGENCY wins (E < F)
        cm.add_appointment(Appointment(5, 2, 104, 40, AppointmentStatus.COMPLETED, AppointmentType.FOLLOWUP))
        cm.add_appointment(Appointment(6, 2, 105, 50, AppointmentStatus.COMPLETED, AppointmentType.EMERGENCY))

        # doctor 3: no appointments -> zeroed summary

        # doctor 4: 2 appointments, CONSULTATION x1, FOLLOWUP x1 — tied
        # tiebreak alphabetically -> CONSULTATION wins (C < F)
        cm.add_appointment(Appointment(7, 4, 106, 30, AppointmentStatus.COMPLETED, AppointmentType.CONSULTATION))
        cm.add_appointment(Appointment(8, 4, 107, 30, AppointmentStatus.COMPLETED, AppointmentType.FOLLOWUP))

        summary = cm.get_doctor_appointment_summary()


        # doctor 1
        self.assertEqual(4,                            summary[1].total_appointments)
        self.assertEqual(125,                          summary[1].total_minutes)
        self.assertEqual(AppointmentType.CONSULTATION, summary[1].busiest_appointment_type)

        # doctor 2 — tiebreak by name -> EMERGENCY wins
        self.assertEqual(2,                         summary[2].total_appointments)
        self.assertEqual(90,                        summary[2].total_minutes)
        self.assertEqual(AppointmentType.EMERGENCY, summary[2].busiest_appointment_type)

        # doctor 3 — zero appointments
        self.assertEqual(0,    summary[3].total_appointments)
        self.assertEqual(0,    summary[3].total_minutes)
        self.assertIsNone(summary[3].busiest_appointment_type)

        # doctor 4 — tiebreak by name -> CONSULTATION wins
        self.assertEqual(2,                            summary[4].total_appointments)
        self.assertEqual(60,                           summary[4].total_minutes)
        self.assertEqual(AppointmentType.CONSULTATION, summary[4].busiest_appointment_type)

    def test_get_doctor_workload_ranking_case1(self):
        print("Running test_get_doctor_workload_ranking_case1")
        cm = ClinicManager()
        for did in [1, 2, 3]:
            cm.add_doctor(Doctor(did, f"doctor{did}"))

        # doctor 1: 3 appointments, 110 total minutes
        # patient 100 has 2 appointments -> most frequent = 100
        cm.add_appointment(Appointment(1, 1, 100, 30, AppointmentStatus.COMPLETED, AppointmentType.CONSULTATION))
        cm.add_appointment(Appointment(2, 1, 100, 50, AppointmentStatus.COMPLETED, AppointmentType.FOLLOWUP))
        cm.add_appointment(Appointment(3, 1, 101, 30, AppointmentStatus.COMPLETED, AppointmentType.EMERGENCY))

        # doctor 2: 2 appointments, 70 total minutes
        # patient 102 and 103 each have 1 appointment -> tiebreak by patient_id -> 102
        cm.add_appointment(Appointment(4, 2, 102, 40, AppointmentStatus.COMPLETED, AppointmentType.CONSULTATION))
        cm.add_appointment(Appointment(5, 2, 103, 30, AppointmentStatus.COMPLETED, AppointmentType.FOLLOWUP))

        # doctor 3: no appointments -> excluded
        result = cm.get_doctor_workload_ranking(3)
        self.assertEqual([[1, 110, 100], [2, 70, 102]], result)

        # k=0 -> empty
        self.assertEqual([], cm.get_doctor_workload_ranking(0))


    def test_get_doctor_workload_ranking_case2(self):
        print("Running test_get_doctor_workload_ranking_case2")
        cm = ClinicManager()
        for did in [1, 2, 3, 4]:
            cm.add_doctor(Doctor(did, f"doctor{did}"))

        # doctor 1: 3 appointments, 90 total minutes
        # patient 100 has 2 appointments -> most frequent = 100
        cm.add_appointment(Appointment(1, 1, 100, 30, AppointmentStatus.COMPLETED, AppointmentType.CONSULTATION))
        cm.add_appointment(Appointment(2, 1, 100, 30, AppointmentStatus.COMPLETED, AppointmentType.FOLLOWUP))
        cm.add_appointment(Appointment(3, 1, 101, 30, AppointmentStatus.COMPLETED, AppointmentType.EMERGENCY))

        # doctor 2: 3 appointments, 90 total minutes
        # tied on total_minutes with doctor 1
        # patient 102 has 2 appointments -> most frequent = 102
        # doctor_id tiebreak -> doctor 1 ranks higher
        cm.add_appointment(Appointment(4, 2, 102, 30, AppointmentStatus.COMPLETED, AppointmentType.CONSULTATION))
        cm.add_appointment(Appointment(5, 2, 102, 30, AppointmentStatus.COMPLETED, AppointmentType.FOLLOWUP))
        cm.add_appointment(Appointment(6, 2, 103, 30, AppointmentStatus.COMPLETED, AppointmentType.EMERGENCY))

        # doctor 3: 2 appointments, 90 total minutes
        # tied on total_minutes with doctor 1 and 2
        # patient 104 and 105 each have 1 appointment -> tiebreak by patient_id -> 104
        # doctor_id tiebreak -> doctor 3 ranks after doctor 2
        cm.add_appointment(Appointment(7, 3, 104, 45, AppointmentStatus.COMPLETED, AppointmentType.CONSULTATION))
        cm.add_appointment(Appointment(8, 3, 105, 45, AppointmentStatus.COMPLETED, AppointmentType.FOLLOWUP))

        # doctor 4: 1 appointment, 30 total minutes -> ranks last
        cm.add_appointment(Appointment(9, 4, 106, 30, AppointmentStatus.COMPLETED, AppointmentType.CONSULTATION))

        # k=3 -> top 3 only, doctor 4 excluded
        result = cm.get_doctor_workload_ranking(3)
        self.assertEqual(
            [[1, 90, 100], [2, 90, 102], [3, 90, 104]],
            result
        )


if __name__ == "__main__":
    unittest.main()
