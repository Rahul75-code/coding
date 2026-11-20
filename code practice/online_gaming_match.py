"""
We are building the back-end for an online gaming platform. The system tracks
players and their match history. Each match result records the outcome from
that player's perspective.

Definitions:
* A "player" has: player_id, username.
* A "match result" has: player_id, opponent_id, outcome, score, timestamp.
* Outcome is one of: WIN, LOSS, DRAW.
* "GameManager" manages players and match results and provides player statistics.

To begin with, we present you with two tasks:
1-1) Read through and understand the code below. Feel free to run it.
1-2) The test for GameManager is not passing due to a bug in the code.
     Make the necessary changes to GameManager to fix the bug.

Clarifications
•	total_matches counts all matches including draws.
•	win_rate = wins / total_matches.

"""
"""
We are extending the platform to support recording match results
and computing per-player score statistics.

Each MatchResult represents one player's experience of a single match:
- player_id      : the player this record belongs to
- opponent_id    : the opponent in that match
- outcome        : one of WIN, LOSS, DRAW
- score          : the player's score in that match
- timestamp      : when the match was played

To implement these changes, we need to add two functions to the GameManager class:

2.1) The add_match_result function should be used to store a match result.
     If the player_id on the match result does not refer to a known player
     in GameManager, the match result should be ignored.

2.2) The get_average_score_by_outcome function should return a dictionary
     mapping each outcome (WIN, LOSS, DRAW) to the player's average score
     for that outcome. Only outcomes the player has at least one result
     for should appear in the dictionary. If the player has no match
     results at all, return an empty dictionary.

To assist you in testing these new functions, we have provided the
test_add_match_result and test_get_average_score_by_outcome tests.
"""
"""
We want to identify which players are currently in the best form
based on their most recent match performance.

A player's form is calculated using a simple points system applied
to their last few match outcomes:
- WIN  = 3 points
- DRAW = 1 point
- LOSS = 0 points

Add one function to the GameManager class:

4) The get_recent_form function takes a number n and returns a list
   of [player_id, form_points] entries — one for each qualifying player.
   For each player:
   - Take only their last n match results, ordered by timestamp ascending.
   - Calculate their form_points from those n matches.
   - Only include players who have at least n match results.
   The returned list should be sorted by form_points in descending order,
   with player_id ascending as a tiebreaker.
   If n is less than or equal to 0, return an empty list.

To assist you in testing this new function, we have provided the
test_get_recent_form_case1 and test_get_recent_form_case2 tests.
"""


import unittest
from enum import Enum


class Outcome(Enum):
    WIN = "WIN"
    LOSS = "LOSS"
    DRAW = "DRAW"


class Player:
    def __init__(self, player_id, username):
        self.player_id = player_id
        self.username = username


class MatchResult:
    def __init__(self, player_id, opponent_id, outcome, score, timestamp):
        self.player_id = player_id
        self.opponent_id = opponent_id
        self.outcome = outcome
        self.score = score
        self.timestamp = timestamp


class PlayerStats:
    def __init__(self, total_matches, wins, win_rate):
        self.total_matches = total_matches
        self.wins = wins
        self.win_rate = win_rate

class HeadToHead:
    def __init__(self, wins_player1, wins_player2, draws,
                 total_matches, last_result, last_match_timestamp):
        self.wins_player1 = wins_player1
        self.wins_player2 = wins_player2
        self.draws = draws
        self.total_matches = total_matches
        self.last_result = last_result
        self.last_match_timestamp = last_match_timestamp

class GameManager:
    def __init__(self):
        self.players = {}        # player_id -> Player
        self.match_results = []  # list of MatchResult

    def add_player(self, player):
        self.players[player.player_id] = player

    def get_player_statistics(self, player_id):
        player_matches = [m for m in self.match_results
                         if m.player_id == player_id]

        total_matches = sum(1 for m in player_matches
                           if m.outcome in [Outcome.WIN, Outcome.LOSS, Outcome.DRAW])
        wins = sum(1 for m in player_matches
                  if m.outcome == Outcome.WIN)
        win_rate = wins / total_matches if total_matches > 0 else 0.0

        return PlayerStats(total_matches, wins, win_rate)

    def add_match_result(self, MatchResult):
        if MatchResult.player_id in self.players:
            self.match_results.append(MatchResult)

    def get_average_score_by_outcome(self, player_id):  
        player_matches = [m for m in self.match_results if m.player_id == player_id]

        if not player_matches:
            return {}
        # Step 1: Group scores by outcome category
        outcome_groups = {}
        for match in player_matches:
            if match.Outcome not in outcome_groups:
                outcome_groups[match.Outcome] = []
            
            outcome_groups[match.Outcome].append(match.score)

        # Step 2: Explicitly calculate averages step-by-step before returning
        avg_score = {}
        for outcome, scores in outcome_groups.items():
            # Perform the math explicitly
            avg_score[outcome] = sum(scores)/len(scores)

        # or # avg_score = {outcome: sum(scores) / len(scores) for outcome, scores in outcome_groups.items()}

        # Step 3: Return the final prepared dictionary
        return avg_score

    # 3) Calculate Head-to-Head Statistics between two players
    def get_head_to_head(self, p1_id, p2_id):
        # Isolate matches specifically from player1's perspective facing player2
        p1_perspective_matches = [
            m for m in self.match_results 
            if m.player_id == p1_id and m.opponent_id == p2_id
        ]

        if not p1_perspective_matches:
            return HeadToHead(0, 0, 0, 0, None, None)

        wins_player1 = sum(1 for m in p1_perspective_matches if m.outcome == Outcome.WIN)
        wins_player2 = sum(1 for m in p1_perspective_matches if m.outcome == Outcome.LOSS)
        draws = sum(1 for m in p1_perspective_matches if m.outcome == Outcome.DRAW)
        total_matches = len(p1_perspective_matches)

        # Track the most recent match based on the maximum timestamp
        most_recent_match = max(p1_perspective_matches, key=lambda m: m.timestamp)
        last_result = most_recent_match.outcome
        last_match_timestamp = most_recent_match.timestamp

        return HeadToHead(wins_player1, wins_player2, draws, total_matches, last_result, last_match_timestamp)


    def get_recent_form(self, n):
        # Guard clause for invalid n window sizes
        if n <= 0:
            return []

        # Point scoring system configuration mapping
        points_map = {
            Outcome.WIN: 3,
            Outcome.DRAW: 1,
            Outcome.LOSS: 0
        }

        qualifying_players = []

        # Evaluate every registered player in the platform
        for player_id in self.players:
            # 1. Fetch all match results matching this specific player
            player_matches = [m for m in self.match_results if m.player_id == player_id]
            
            # 2. Skip players who haven't met the minimum match count milestone
            if len(player_matches) < n:
                continue

            # 3. Sort chronologically by timestamp ascending
            player_matches.sort(key=lambda m: m.timestamp)

            # 4. Take only the most recent n matches
            recent_window = player_matches[-n:]

            # 5. Accumulate score points using the points mapping config
            form_points = sum(points_map[m.outcome] for m in recent_window)
            
            qualifying_players.append([player_id, form_points])

        # 6. Sort by points descending (-x[1]), then by player_id ascending (x[0]) as a tiebreaker
        qualifying_players.sort(key=lambda x: (-x[1], x[0]))

        return qualifying_players


class TestSuite(unittest.TestCase):
    def test_get_player_statistics(self):
        print("Running test_get_player_statistics")
        gm = GameManager()
        gm.add_player(Player(1, "player1"))
        gm.add_player(Player(2, "player2"))

        gm.match_results.append(MatchResult(1, 2, Outcome.WIN,  80, 1000))
        gm.match_results.append(MatchResult(1, 2, Outcome.LOSS, 50, 2000))
        gm.match_results.append(MatchResult(1, 2, Outcome.DRAW, 60, 3000))
        gm.match_results.append(MatchResult(1, 2, Outcome.WIN,  90, 4000))

        stats = gm.get_player_statistics(1)
        self.assertEqual(4, stats.total_matches)
        self.assertEqual(2, stats.wins)
        self.assertAlmostEqual(0.5, stats.win_rate, places=4)

        gm.match_results.append(MatchResult(2, 1, Outcome.DRAW, 60, 1000))
        gm.match_results.append(MatchResult(2, 1, Outcome.DRAW, 60, 2000))

        stats2 = gm.get_player_statistics(2)
        self.assertEqual(2, stats2.total_matches)
        self.assertEqual(0, stats2.wins)
        self.assertAlmostEqual(0.0, stats2.win_rate, places=4)

    def test_add_match_result(self):
        print("Running test_add_match_result")
        gm = GameManager()
        gm.add_player(Player(1, "player1"))
        gm.add_player(Player(2, "player2"))

        gm.add_match_result(MatchResult(1, 2, Outcome.WIN, 80, 1000))
        gm.add_match_result(MatchResult(2, 1, Outcome.LOSS, 50, 1000))

        # unknown player ignored
        gm.add_match_result(MatchResult(99, 1, Outcome.WIN, 100, 2000))

        self.assertEqual(2, len(gm.match_results))


    def test_get_average_score_by_outcome(self):
        print("Running test_get_average_score_by_outcome")
        gm = GameManager()
        gm.add_player(Player(1, "player1"))
        gm.add_player(Player(2, "player2"))

        # match 1 - player1 wins
        gm.add_match_result(MatchResult(1, 2, Outcome.WIN,  80, 1000))
        gm.add_match_result(MatchResult(2, 1, Outcome.LOSS, 50, 1000))

        # match 2 - player1 wins again
        gm.add_match_result(MatchResult(1, 2, Outcome.WIN,  90, 2000))
        gm.add_match_result(MatchResult(2, 1, Outcome.LOSS, 60, 2000))

        # match 3 - draw
        gm.add_match_result(MatchResult(1, 2, Outcome.DRAW, 70, 3000))
        gm.add_match_result(MatchResult(2, 1, Outcome.DRAW, 70, 3000))

        avg1 = gm.get_average_score_by_outcome(1)
        self.assertAlmostEqual(85.0, avg1[Outcome.WIN],  places=4)  # (80+90)/2
        self.assertAlmostEqual(70.0, avg1[Outcome.DRAW], places=4)
        self.assertNotIn(Outcome.LOSS, avg1)                         # player1 has no losses

        avg2 = gm.get_average_score_by_outcome(2)
        self.assertAlmostEqual(55.0, avg2[Outcome.LOSS], places=4)  # (50+60)/2
        self.assertAlmostEqual(70.0, avg2[Outcome.DRAW], places=4)
        self.assertNotIn(Outcome.WIN, avg2)                          # player2 has no wins

        # player with no match results
        gm.add_player(Player(3, "player3"))
        self.assertEqual({}, gm.get_average_score_by_outcome(3))

    def test_get_recent_form_case1(self):
        print("Running test_get_recent_form_case1")
        gm = GameManager()
        for pid in [1, 2, 3, 4]:
            gm.add_player(Player(pid, f"player{pid}"))

        # player 1: W W W -> 9 points
        gm.add_match_result(MatchResult(1, 2, Outcome.WIN, 80, 1000))
        gm.add_match_result(MatchResult(1, 2, Outcome.WIN, 80, 2000))
        gm.add_match_result(MatchResult(1, 2, Outcome.WIN, 80, 3000))

        # player 2: W D L -> 4 points
        gm.add_match_result(MatchResult(2, 1, Outcome.WIN,  80, 1000))
        gm.add_match_result(MatchResult(2, 1, Outcome.DRAW, 80, 2000))
        gm.add_match_result(MatchResult(2, 1, Outcome.LOSS, 80, 3000))

        # player 3: L L W -> 3 points
        gm.add_match_result(MatchResult(3, 1, Outcome.LOSS, 80, 1000))
        gm.add_match_result(MatchResult(3, 1, Outcome.LOSS, 80, 2000))
        gm.add_match_result(MatchResult(3, 1, Outcome.WIN,  80, 3000))

        # player 4: only 2 matches, n=3 -> excluded
        gm.add_match_result(MatchResult(4, 1, Outcome.WIN, 80, 1000))
        gm.add_match_result(MatchResult(4, 1, Outcome.WIN, 80, 2000))

        result = gm.get_recent_form(3)
        self.assertEqual([[1, 9], [2, 4], [3, 3]], result)

        # n=0 -> empty list
        self.assertEqual([], gm.get_recent_form(0))

    def test_get_recent_form_case2(self):
        print("Running test_get_recent_form_case2")
        gm = GameManager()
        for pid in [1, 2, 3, 4]:
            gm.add_player(Player(pid, f"player{pid}"))

        # player 1: 4 matches, last 3 = W W W -> 9 points
        # older LOSS at timestamp 500 is outside the window and ignored
        gm.add_match_result(MatchResult(1, 2, Outcome.LOSS, 80,  500))
        gm.add_match_result(MatchResult(1, 2, Outcome.WIN,  80, 1000))
        gm.add_match_result(MatchResult(1, 2, Outcome.WIN,  80, 2000))
        gm.add_match_result(MatchResult(1, 2, Outcome.WIN,  80, 3000))

        # player 2: exactly 3 matches, W W W -> 9 points
        # tied with player 1 on points, tiebreak by player_id -> player 1 ranks higher
        gm.add_match_result(MatchResult(2, 1, Outcome.WIN, 80, 1000))
        gm.add_match_result(MatchResult(2, 1, Outcome.WIN, 80, 2000))
        gm.add_match_result(MatchResult(2, 1, Outcome.WIN, 80, 3000))

        # player 3: only 2 matches, n=3 -> excluded
        gm.add_match_result(MatchResult(3, 1, Outcome.WIN, 80, 1000))
        gm.add_match_result(MatchResult(3, 1, Outcome.WIN, 80, 2000))

        # player 4: exactly 3 matches, L L L -> 0 points, included
        gm.add_match_result(MatchResult(4, 1, Outcome.LOSS, 80, 1000))
        gm.add_match_result(MatchResult(4, 1, Outcome.LOSS, 80, 2000))
        gm.add_match_result(MatchResult(4, 1, Outcome.LOSS, 80, 3000))

        result = gm.get_recent_form(3)
        # player 3 excluded - only 2 matches
        # player 1 and 2 tied on 9 points, player 1 wins tiebreak (lower id)
        # player 4 included with 0 points
        self.assertEqual([[1, 9], [2, 9], [4, 0]], result)


if __name__ == "__main__":
    unittest.main()



