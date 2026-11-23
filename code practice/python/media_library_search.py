"""
Our media streaming product shows a catalog dashboard that breaks down how many titles of each type the library holds - movies vs. shows vs. podcasts vs. songs. This powers the 'Browse by type' tiles and internal catalog reports.

The MediaIndex class stores catalog items and exposes count_by_type(), which should return a dict from each media type to the number of items of that type. The provided test is currently failing.

1) Read through and understand the code below. Take as much time as you need, and feel free to run it.

2) count_by_type() has a bug that makes the counts wrong. Find and fix it so the test passes. For a catalog with two movies and one show, the correct result is {"MOVIE": 2, "SHOW": 1}.
"""
"""
The catalog dashboard gives editors two at-a-glance signals about the library. First, a per-title 
popularity badge, so an editor scanning a title immediately sees how watched it is. Second, an average 
rating per media type, so they can tell where the library is strong and where it needs investment.

1) Add popularity_tier(item_id) to MediaIndex. Given an item's id, return its popularity tier as a 
string, based on that item's lifetime view_count: HOT for 1000 or more, POPULAR for 100 or more 
(but under 1000), and NICHE for under 100. For example, a title with 5000 views is HOT, one with 500
 is POPULAR, and one with 10 is NICHE.

2) Add average_rating_by_type() to MediaIndex. Return a dict from each media type to the average 
rating (a floating-point number) of the items of that type. A library with two movies rated 4.0 and 2.0 
and one show rated 5.0 returns {"MOVIE": 3.0, "SHOW": 5.0}. A media type with no items simply does not 
appear in the result.
"""
"""
The browse page shows a Trending tags rail - the tags that appear on the most titles across the whole catalog - 
so users can jump straight into the genres and themes the library leans into. Tags are free-text, and editors 
are inconsistent about capitalisation, so the same theme shows up as Action, action, or ACTION on different titles.

1) Add top_tags(n) to MediaIndex. It returns the n most common tags across the catalog, as a list of tag strings 
ordered by how many titles carry the tag, descending. Counting is case-insensitive - Action, action, and ACTION 
are the same tag and count together - and the returned tags are lower-cased. Ties are broken alphabetically (ascending).

Worked example - over a catalog whose titles carry the tags ["Action", "Thriller"], ["action", "drama"], 
and ["ACTION"]: the tag action appears on all three titles (count 3), while drama and thriller each appear once. 
So for n = 2 the result is ["action", "drama"] - action first by count, then drama ahead of thriller on the alphabetical tie-break.

Counterexample: if you count tags without normalising case first, Action, action, and ACTION become three different 
tags of count 1 each, and a genuinely less popular tag can outrank the real leader. Fold case before counting, not after.
"""
"""
This is the core of catalog search. When a user types several keywords into the search box - say action 2020 - they expect results that match every keyword, ordered so the most-watched titles appear first.

1) Add search(terms) to MediaIndex. Given a list of query terms, it returns a list of item ids for the items whose tags contain all of the terms. Matching is case-insensitive (a tag "Action" matches the term "action"). Results are ranked by view_count descending; ties are broken by item id ascending.

Worked example - searching ["action", "2020"] over:
- Item 1 - tags ["action", "2020"], 100 views - matches (has both terms).
- Item 2 - tags ["action"], 999 views - excluded: it has only one of the two terms, even though it is the most-watched.
- Item 3 - tags ["action", "2020"], 100 views - matches.

The result is [1, 3]: items 1 and 3 both match all terms and tie on views (100), so they are ordered by id ascending.
"""


import unittest
from enum import Enum

class MediaType(Enum):
    """The kind of catalog entry.

    MOVIE   - a single feature-length film.
    SHOW    - an episodic series (counted as one catalog entry).
    PODCAST - an audio series entry.
    SONG    - a single music track.
    """
    MOVIE = 1
    SHOW = 2
    PODCAST = 3
    SONG = 4

class MediaItem:
    """One entry in the media catalog."""
    def __init__(self, item_id, title, media_type, tags, view_count, rating):
        self.item_id = item_id            # unique integer id
        self.title = title                # display title
        self.media_type = media_type      # a MediaType
        self.tags = tags                  # list of free-text keyword tags, e.g. "action"
        self.view_count = view_count      # lifetime number of plays/views
        self.rating = rating              # average rating, 0.0-5.0

class MediaIndex:
    """In-memory catalog index. Stores MediaItems and answers catalog queries
    for the product's browse and search screens."""
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
 
    def count_by_type(self):
        counts = {}
        for it in self.items:
            if it.media_type.name not in counts:
                counts[it.media_type.name] = 0
            counts[it.media_type.name] += 1
        return counts
    
    def popularity_tier(self, item_id):
        for item in self.items:
            if item.item_id == item_id:
                if item.view_count >= 1000:
                    return "HOT"
                elif item.view_count >= 100 and item.view_count < 100:
                    return "POPULAR"
                else:
                    return "NICHE"
        return None

    def average_rating_by_type(self):
        media_rating = {}
        for it in self.items:
            type_name = it.media_type.name
            if type_name not in media_rating:
                media_rating[type_name] = []
            media_rating[type_name].append(it.rating)
        media_avg_rating = {}
        for m, r in media_rating.items():
            avg = sum(r)/len(r)
            media_avg_rating[m] = avg

        return media_avg_rating

    def top_tags(self, n):
        top_tags = {}
        for it in self.items:
            for tag in it.tags:
                lower_tag = tag.lower()
                top_tags[lower_tag] = top_tags.get(lower_tag, 0) + 1

        unique_tags = list(top_tags.keys())

        unique_tags.sort(key = lambda tag : (-top_tags[tag],tag))

        return unique_tags [:n]

    def search(self, terms):
        """Filters catalog items containing ALL search terms (case-insensitive),

        ranking results by view_count descending, then item_id ascending.
        """
        # Step 1: Lowercase and normalize all input search query terms
        query_terms = [t.lower() for t in terms]
        matching_items = []

        # Step 2: Scan the library and filter items that match every single keyword
        for item in self.items:
            # Lowercase all current item tags for case-insensitive set check validation
            item_tags = {tag.lower() for tag in item.tags}
            
            # Check if every individual term exists inside the item's tag pool boundary
            if all(term in item_tags for term in query_terms):
                matching_items.append(item)

        # Step 3: Sort using a tuple key: (-view_count, item_id)
        # -x handles count descending, x handles ID ascending
        matching_items.sort(key=lambda item: (-item.view_count, item.item_id))

        # Step 4: Extract and return only the item IDs
        return [item.item_id for item in matching_items]
               

class TestSuite(unittest.TestCase):
    def test_count_by_type(self):
        index = MediaIndex()
        index.add_item(MediaItem(1, "Heat", MediaType.MOVIE, [], 0, 0.0))
        index.add_item(MediaItem(2, "Drive", MediaType.MOVIE, [], 0, 0.0))
        index.add_item(MediaItem(3, "The Wire", MediaType.SHOW, [], 0, 0.0))
        self.assertEqual(index.count_by_type(), {"MOVIE": 2, "SHOW": 1})

    # Add these two methods inside the TestSuite class.
    def test_popularity_tier(self):
        index = MediaIndex()
        index.add_item(MediaItem(1, "Blockbuster", MediaType.MOVIE, [], 5000, 0.0))
        index.add_item(MediaItem(2, "Midlist", MediaType.MOVIE, [], 500, 0.0))
        index.add_item(MediaItem(3, "Deep Cut", MediaType.SHOW, [], 10, 0.0))
        index.add_item(MediaItem(4, "Edge Hot", MediaType.MOVIE, [], 1000, 0.0))
        index.add_item(MediaItem(5, "Edge Pop", MediaType.SHOW, [], 100, 0.0))
        self.assertEqual(index.popularity_tier(1), "HOT")
        self.assertEqual(index.popularity_tier(2), "POPULAR")
        self.assertEqual(index.popularity_tier(3), "NICHE")
        self.assertEqual(index.popularity_tier(4), "HOT")
        self.assertEqual(index.popularity_tier(5), "POPULAR")

    def test_average_rating_by_type(self):
        index = MediaIndex()
        index.add_item(MediaItem(1, "Heat", MediaType.MOVIE, [], 0, 4.0))
        index.add_item(MediaItem(2, "Drive", MediaType.MOVIE, [], 0, 2.0))
        index.add_item(MediaItem(3, "The Wire", MediaType.SHOW, [], 0, 5.0))
        self.assertEqual(index.average_rating_by_type(), {"MOVIE": 3.0, "SHOW": 5.0})
        self.assertEqual(MediaIndex().average_rating_by_type(), {})

    def test_top_tags(self):
            index = MediaIndex()
            index.add_item(MediaItem(1, "Heat", MediaType.MOVIE, ["Action", "Thriller"], 0, 0.0))
            index.add_item(MediaItem(2, "Drive", MediaType.MOVIE, ["action", "drama"], 0, 0.0))
            index.add_item(MediaItem(3, "Collateral", MediaType.SHOW, ["ACTION"], 0, 0.0))
            self.assertEqual(index.top_tags(2), ["action", "drama"])
            self.assertEqual(index.top_tags(10), ["action", "drama", "thriller"])

    def test_search(self):
        index = MediaIndex()
        index.add_item(MediaItem(1, "Heat", MediaType.MOVIE, ["Action", "2020"], 100, 0.0))
        index.add_item(MediaItem(2, "Drive", MediaType.MOVIE, ["action"], 999, 0.0))
        index.add_item(MediaItem(3, "Collateral", MediaType.MOVIE, ["action", "2020"], 100, 0.0))
        self.assertEqual(index.search(["action", "2020"]), [1, 3])
        self.assertEqual(index.search(["action"]), [2, 1, 3])
        self.assertEqual(index.search(["drama"]), [])


if __name__ == "__main__":
    unittest.main()
