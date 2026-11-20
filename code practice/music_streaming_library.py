"""
We are building the analytics back-end for a music streaming platform. The system
tracks songs and play events. A play is "completed" when listened_seconds >= the
song's duration, and "skipped" otherwise.

To begin with, we present you with two tasks:
1-1) Read through and understand the code below. Feel free to run it.
1-2) The test for MusicLibrary is not passing due to bugs in the code.
     Make the necessary changes to MusicLibrary to fix the bugs.
"""
"""
We've discovered that the catalog has accumulated duplicate Song records from
multiple data feeds. We need to deduplicate.

Two songs are duplicates if they have the same title (case-insensitive), the same artist (case-insensitive), and the same duration_seconds.
You may assume all song_ids are unique.

For each group of duplicates, we keep ONE song: the one with the smallest song_id.

The DedupResult class is provided below:
    song_id:      the song_id of the song that was kept
    merged_ids:   list of song_ids to merge into it,
                  sorted ascending (does NOT include song_id itself)

Add a function to MusicLibrary:

2.1) find_duplicate_groups():
     Return the list of DedupResult objects, sorted by song_id ascending, for all groups of duplicates.
     
To assist you in testing the new function, we have provided the test_dedup test.
"""
"""
We are adding playlist support to the library. A Playlist is an ordered list
of song_ids that belong to a user, with attached validation rules.

Each rule has a "type" plus any rule-specific parameters:

  {"type": "MAX_DURATION", "max_seconds": int}
      The total duration of the playlist must not exceed max_seconds.

  {"type": "MAX_PER_ARTIST", "artist": str, "max_count": int}
      At most max_count songs by the given artist may appear in the playlist.

Each playlist has at most one rule of each type.

We have added the Playlist class:

    Playlist(playlist_id, owner_user_id, song_ids, rules)
        song_ids: list of song_ids in playback order
        rules:    list of rule entries as described above

Add two functions to MusicLibrary:

3.1) add_playlist(playlist):
     Store the playlist.

3.2) validate_playlist(playlist_id) -> List[str]:
     Return the rule_type strings of violated rules, in the order they appear
     in playlist.rules. Return [] for an unknown playlist_id or empty rules.

To assist you in testing these new functions, we have provided the
test_playlist_validation test.
"""
"""
We want to recommend songs based on what users listen to together in the same session.

A Session represents one listening session by a user:
    Session(user_id, song_ids)
        user_id:  the user who listened
        song_ids: the songs played in this session (order does not matter)

If a session contains duplicate song_ids, treat each song as appearing once.

A pair counts once per user, even if it appears in multiple sessions. The
total co-occurrence between A and B is the number of distinct users for whom
they co-occur.

Example:
  User 1, session 1: [10, 20, 30]  -> pairs (10,20),(10,30),(20,30) for user 1
  User 1, session 2: [10, 20]      -> pair (10,20) again for user 1, but this
                                      is the SAME user — still counts as 1.
  User 2, session 1: [10, 20]      -> pair (10,20) for user 2 — different user,
                                      so (10,20) co-occurrence count is now 2.

Add two functions to MusicLibrary:

4.1) add_session(session):
     Store the session.

4.2) get_recommendations(song_id, top_n) -> List[Tuple[int, int]]:
     Return the top_n songs that most frequently co-occur with the given
     song across users' sessions.

     Output: list of (other_song_id, co_occurrence_count) tuples,
       - co_occurrence_count is the number of distinct users in whose
         sessions song_id and other_song_id appear together
       - sorted by co_occurrence_count DESCENDING, then other_song_id ASCENDING
       - exclude the input song_id itself
       - exclude any songs with co_occurrence_count of 0
       - if fewer than top_n songs qualify, return all qualifying songs
       - if the input song_id is not in the catalog, return []
       - if top_n is 0 or negative, return []

To assist you in testing these new functions, we have provided the test_get_recommendations_case1 and test_get_recommendations_case2 tests.
"""


import unittest


class Song:
    def __init__(self, song_id, title, artist, duration_seconds,
                 description=None, album=None, release_year=None, genre=None):
        self.song_id = song_id
        self.title = title
        self.artist = artist
        self.duration_seconds = duration_seconds
        self.description = description
        self.album = album
        self.release_year = release_year
        self.genre = genre


class PlayEvent:
    def __init__(self, play_id, user_id, song_id, listened_seconds):
        self.play_id = play_id
        self.user_id = user_id
        self.song_id = song_id
        self.listened_seconds = listened_seconds


class ListenerStats:
    def __init__(self, total_plays, unique_songs, completion_rate):
        self.total_plays = total_plays
        self.unique_songs = unique_songs
        self.completion_rate = completion_rate


class DedupResult:
    def __init__(self, song_id, merged_ids):
        self.song_id = song_id  # int
        self.merged_ids = merged_ids  # list[int], sorted ascending

class Playlist:
    def __init__(self, playlist_id, owner_user_id, song_ids, rules):
        self.playlist_id = playlist_id
        self.owner_user_id = owner_user_id
        self.song_ids = song_ids
        self.rules = rules

class Session:
    def __init__(self, user_id, song_ids):
        self.user_id = user_id
        self.song_ids = song_ids


class MusicLibrary:
    def __init__(self):
        self.songs = {}        # song_id -> Song
        self.play_events = []  # list of PlayEvent
        self.playlists = {}

    def add_song(self, song):
        self.songs[song.song_id] = song

    def add_play_event(self, event):
        self.play_events.append(event)

    def _is_completed(self, event):
        # A play is completed when listened_seconds reaches the song's duration.
        song = self.songs[event.song_id]
        return event.listened_seconds >= song.duration_seconds

    def get_listener_stats(self, user_id):
        """
        Return statistics for a single user:
        * total_plays:     total number of play events by this user
        * unique_songs:    number of distinct songs this user has played (including skipped plays)
        * completion_rate: fraction of this user's plays that were completed,
                           expressed as a value between 0.0 and 1.0
        """
        user_events = [e for e in self.play_events if e.user_id == user_id]

        completed_events = [e for e in user_events if self._is_completed(e)]
        total_plays = len(user_events)

        unique_songs = len({e.song_id for e in user_events})

        if total_plays == 0:
            completion_rate = 0.0
        else:
            completion_rate = len(completed_events) / len(user_events)

        return ListenerStats(total_plays, unique_songs, completion_rate)

    def find_duplicate_groups(self):
        groups={}
        for song in self.songs.values():
            key = (song.itle.lower(), song.artist.lower(), song.duration_seconds)
            if key not in groups:
                groups[key] = []
            groups[key].append(song.song_id)

        dedup_results = []

        for song_ids in groups.values():
            if len(song_ids) > 1 :
                master_id = min(song_ids)
                merged_ids = [sid for sid in song_ids if sid is not master_id]
                merged_ids.sort()

                dedup_results.append(DedupResult(master_id, merged_ids))

    def add_playlist(self, playlist):
        self.playlists[playlist.playlist_id] = playlist

    def validate_playlist(self, playlist_id):
        # Return empty list if the playlist does not exist in our system
        if playlist_id not in self.playlists:
            return []
        
        playlist = self.playlists[playlist_id]
        violated_rules = []

        # Process each validation rule in the exact order they are defined
        for rule in self.playlist.rules:
            if rule["type"] == "MAX_DURATION":
                # Compute total play duration of all tracks currently in the playlist
                total_duration = sum(
                    self.song[sid].duration_seconds 
                    for sid in playlist.song_ids if sid in self.songs
                )
                if total_duration > rule["max_seconds"]:
                    violated_rules.append(rule["type"])
            elif rule["type"] == "MAX_PER_ARTIST":
            # Count the number of track instances matching the target artist                
                target_artist = rule["artist"]
                artist_count = sum(
                    1 for sid in playlist.song_ids
                    if sid in self.songs and self.songs[sid].artist == target_artist
                )
                if artist_count > rule["max_count"]:
                    violated_rules.append(rule["type"])

        return violated_rules    


    def add_session(self, session):
        self.sessions.append(session)
        
        # Initialize user tracking if they are new to the platform
        if session.user_id not in self.user_song_history:
            self.user_song_history[session.user_id] = set()
            
        # Accumulate unique songs this user has interacted with across all their sessions
        for song_id in session.song_ids:
            if song_id in self.songs:
                self.user_song_history[session.user_id].add(song_id)

    def get_recommendations(self, song_id, top_n):
        # Guard clauses for unmapped items or invalid top_n counts
        if song_id not in self.songs or top_n <= 0:
            return []

        co_occurrence_counts = {}

        # Loop through each distinct user's historic aggregated profile
        for user_id, unique_songs in self.user_song_history.items():
            if song_id in unique_songs:
                # Add co-occurrences for other tracks this user listened to in any session
                for other_song_id in unique_songs:
                    if other_song_id != song_id:
                        co_occurrence_counts[other_song_id] = co_occurrence_counts.get(other_song_id, 0) + 1

        # Flatten counts into a list of tuples
        qualifying_recommendations = list(co_occurrence_counts.items())

        # Sort: Count DESC (-x), then Song ID ASC (x)
        qualifying_recommendations.sort(key=lambda x: (-x[1], x[0]))

        # Slice the list up to top_n items
        return qualifying_recommendations[:top_n]



class TestSuite(unittest.TestCase):
    def test_get_listener_stats(self):
        print("Running test_get_listener_stats")
        lib = MusicLibrary()

        # Catalog: 3 songs.
        lib.add_song(Song(101, "Song A", "Artist 1", 180))
        lib.add_song(Song(102, "Song B", "Artist 2", 200))
        lib.add_song(Song(103, "Song C", "Artist 1", 240))

        # User 1: 4 plays total
        #   - song 101 completed (180 of 180)
        #   - song 102 completed (220 of 200)
        #   - song 101 skipped  (50 of 180)
        #   - song 103 skipped  (100 of 240)
        # Expected: total_plays = 4, unique_songs = 3, completion_rate = 0.5
        lib.add_play_event(PlayEvent(1, 1, 101, 180))
        lib.add_play_event(PlayEvent(2, 1, 102, 220))
        lib.add_play_event(PlayEvent(3, 1, 101, 50))
        lib.add_play_event(PlayEvent(4, 1, 103, 100))

        # User 2: 2 plays total
        #   - song 102 completed (200 of 200)
        #   - song 103 completed (250 of 240)
        # Expected: total_plays = 2, unique_songs = 2, completion_rate = 1.0
        lib.add_play_event(PlayEvent(5, 2, 102, 200))
        lib.add_play_event(PlayEvent(6, 2, 103, 250))

        stats_user_1 = lib.get_listener_stats(1)
        self.assertEqual(4, stats_user_1.total_plays)
        self.assertEqual(3, stats_user_1.unique_songs)
        self.assertAlmostEqual(0.5, stats_user_1.completion_rate, places=4)

        stats_user_2 = lib.get_listener_stats(2)
        self.assertEqual(2, stats_user_2.total_plays)
        self.assertEqual(2, stats_user_2.unique_songs)
        self.assertAlmostEqual(1.0, stats_user_2.completion_rate, places=4)

        stats_user_3 = lib.get_listener_stats(3)
        self.assertEqual(0, stats_user_3.total_plays)
        self.assertEqual(0, stats_user_3.unique_songs)
        self.assertAlmostEqual(0, stats_user_3.completion_rate, places=4)

    def test_dedup(self):
        print("Running test_dedup")
        lib = MusicLibrary()

        # Group A: songs 1, 2, 3 share ("song a", "artist 1", 180).
        lib.add_song(Song(1, "Song A",  "Artist 1", 180, genre="rock"))
        lib.add_song(Song(2, "song a",  "ARTIST 1", 180,
                        description="Studio version",
                        album="First Album",
                        genre="rock"))
        lib.add_song(Song(3, "SONG A",  "artist 1", 180,
                        description="Live",
                        album="Live Album"))
        lib.add_song(Song(30, "Song A", "Artist 1", 999))
        lib.add_song(Song(60, "Unrelated", "Nobody", 180))
        lib.add_song(Song(61, "Also Unrelated", "Else", 180))

        # Group B: songs 10, 11 share ("song b", "artist 2", 200).
        lib.add_song(Song(10, "Song B", "Artist 2", 200, album="B Album"))
        lib.add_song(Song(11, "SONG B", "Artist 2", 200, description="some description", genre="pop"))
        lib.add_song(Song(40, "Song B", "Other Artist", 200))
        lib.add_song(Song(50, "Different Title", "Artist 2", 200))

        # Group C: songs 20, 21 share ("song c", "artist 3", 240). Duplicate — smallest song_id wins.
        lib.add_song(Song(20, "Song C", "Artist 3", 240))
        lib.add_song(Song(21, "song c", "Artist 3", 240))

        # Group D: songs 8, 5, 7 share ("late group", "late artist", 50). Duplicate — smallest song_id wins.
        lib.add_song(Song(8, "Late Group", "Late Artist", 50))
        lib.add_song(Song(5, "late group", "LATE ARTIST", 50))
        lib.add_song(Song(7, "LATE GROUP", "late artist", 50))

        # Unique song — not a duplicate.
        lib.add_song(Song(99, "Only Song", "Solo Artist", 300))

        # Identify songs to merge.
        results = lib.find_duplicate_groups()

        self.assertEqual(4, len(results))

        self.assertEqual(1, results[0].song_id)
        self.assertEqual([2, 3], results[0].merged_ids)

        self.assertEqual(5, results[1].song_id)
        self.assertEqual([7, 8], results[1].merged_ids)

        self.assertEqual(10, results[2].song_id)
        self.assertEqual([11], results[2].merged_ids)

        self.assertEqual(20, results[3].song_id)
        self.assertEqual([21], results[3].merged_ids)

    def test_playlist_validation(self):
        print("Running test_playlist_validation")
        lib = MusicLibrary()

        # Catalog: 6 songs across 3 artists and 3 genres.
        lib.add_song(Song(1, "T1", "Artist A", 100, genre="rock"))
        lib.add_song(Song(2, "T2", "Artist A", 200, genre="rock"))
        lib.add_song(Song(3, "T3", "Artist B", 150, genre="rock"))
        lib.add_song(Song(4, "T4", "Artist B", 250, genre="jazz"))
        lib.add_song(Song(5, "T5", "Artist C", 300, genre="jazz"))
        lib.add_song(Song(6, "T6", "Artist C", 100, genre="pop"))

        # Playlist 100: passes both rules.
        lib.add_playlist(Playlist(
            playlist_id=100,
            owner_user_id=1,
            song_ids=[1, 3, 5, 4],
            rules=[
                {"type": "MAX_DURATION", "max_seconds": 1000},
                {"type": "MAX_PER_ARTIST", "artist": "Artist B", "max_count": 2},
            ],
        ))

        # Playlist 200 (initial version): violates MAX_PER_ARTIST.
        lib.add_playlist(Playlist(
            playlist_id=200,
            owner_user_id=2,
            song_ids=[1, 2, 5, 6],
            rules=[
                {"type": "MAX_DURATION", "max_seconds": 1000},
                {"type": "MAX_PER_ARTIST", "artist": "Artist A", "max_count": 1},
            ],
        ))

        # Verify the initial version of playlist 200.
        v200_initial = lib.validate_playlist(200)
        self.assertEqual(1, len(v200_initial))
        self.assertEqual("MAX_PER_ARTIST", v200_initial[0])

        # Playlist 300: violates only the duration rule.
        lib.add_playlist(Playlist(
            playlist_id=300,
            owner_user_id=3,
            song_ids=[2, 4, 5],
            rules=[
                {"type": "MAX_DURATION", "max_seconds": 500},
            ],
        ))

        # Playlist 400: empty rules list -> always compliant.
        lib.add_playlist(Playlist(
            playlist_id=400,
            owner_user_id=4,
            song_ids=[1, 2, 3],
            rules=[],
        ))

        # Playlist 100 has no violations.
        self.assertEqual([], lib.validate_playlist(100))

        v300 = lib.validate_playlist(300)
        self.assertEqual(1, len(v300))
        self.assertEqual("MAX_DURATION", v300[0])

        # Playlist 400 has no rules, no violations.
        self.assertEqual([], lib.validate_playlist(400))

        # Unknown playlist returns empty list.
        self.assertEqual([], lib.validate_playlist(999))

        # Add a fresh violating playlist to test both rule types (MAX_DURATION + MAX_PER_ARTIST).
        lib.add_playlist(Playlist(
            playlist_id=600,
            owner_user_id=6,
            song_ids=[1, 2, 5, 6],
            rules=[
                {"type": "MAX_DURATION", "max_seconds": 500},
                {"type": "MAX_PER_ARTIST", "artist": "Artist A", "max_count": 1},
            ],
        ))

        v600 = lib.validate_playlist(600)
        self.assertEqual(2, len(v600))
        self.assertEqual("MAX_DURATION", v600[0])
        self.assertEqual("MAX_PER_ARTIST", v600[1])

    def test_get_recommendations_case1(self):
        print("Running test_get_recommendations_case1")
        lib = MusicLibrary()

        # 4 songs in the catalog.
        lib.add_song(Song(10, "S10", "Artist X", 200))
        lib.add_song(Song(20, "S20", "Artist X", 200))
        lib.add_song(Song(30, "S30", "Artist Y", 200))
        lib.add_song(Song(40, "S40", "Artist Z", 200))

        # User 1, session 1: songs 10, 20, 30
        lib.add_session(Session(1, [10, 20, 30]))
        # User 1, session 2: songs 10, 20 (same user, duplicate pair)
        lib.add_session(Session(1, [10, 20]))
        # User 2: songs 10, 20
        lib.add_session(Session(2, [10, 20]))
        # User 3: songs 30, 40
        lib.add_session(Session(3, [30, 40]))

        self.assertEqual(
            [(20, 2), (30, 1)],
            lib.get_recommendations(song_id=10, top_n=5)
        )

        self.assertEqual(
            [(10, 1), (20, 1), (40, 1)],
            lib.get_recommendations(song_id=30, top_n=5)
        )

        # top_n smaller than the number of qualifying recommendations.
        self.assertEqual(
            [(10, 1), (20, 1)],
            lib.get_recommendations(song_id=30, top_n=2)
        )

        self.assertEqual([(30, 1)], lib.get_recommendations(song_id=40, top_n=5))

        # Unknown song_id -> empty list.
        self.assertEqual([], lib.get_recommendations(song_id=999, top_n=5))

        # top_n = 0 -> empty list.
        self.assertEqual([], lib.get_recommendations(song_id=10, top_n=0))

        # top_n negative -> empty list.
        self.assertEqual([], lib.get_recommendations(song_id=10, top_n=-1))

    # Add inside the existing TestSuite class:
    def test_get_recommendations_case2(self):
        print("Running test_get_recommendations_case2")
        lib = MusicLibrary()

        # 5 songs in the catalog.
        for sid in [1, 2, 3, 4, 5]:
            lib.add_song(Song(sid, f"S{sid}", "Artist", 100))

        lib.add_session(Session(1, [1, 2, 3]))    # user 1
        lib.add_session(Session(2, [1, 2]))        # user 2, session A
        lib.add_session(Session(2, [1, 2, 4]))     # user 2, session B (duplicate pair with session A)
        lib.add_session(Session(3, [1, 3, 4]))     # user 3
        lib.add_session(Session(4, [2, 5]))        # user 4
        lib.add_session(Session(5, [1]))           # user 5, session A: singleton, no pairs
        lib.add_session(Session(5, [4, 5]))        # user 5, session B

        self.assertEqual(
            [(2, 2), (3, 2), (4, 2)],
            lib.get_recommendations(song_id=1, top_n=10)
        )

        self.assertEqual(
            [(1, 2), (3, 1), (4, 1), (5, 1)],
            lib.get_recommendations(song_id=2, top_n=10)
        )

        # top_n cap.
        self.assertEqual(
            [(1, 2), (3, 1)],
            lib.get_recommendations(song_id=2, top_n=2)
        )

        self.assertEqual(
            [(2, 1), (4, 1)],
            lib.get_recommendations(song_id=5, top_n=10)
        )


if __name__ == "__main__":
    unittest.main()
