"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os
from recommender import load_songs, recommend_songs

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")


def main() -> None:
    songs = load_songs(CSV_PATH)
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: upbeat indie pop listener, mid-high energy, positive tone, not heavily acoustic
    user_prefs = {
        "genre":        "indie pop",
        "mood":         "happy",
        "target_energy":       0.75,
        "target_valence":      0.80,
        "target_acousticness": 0.30,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 56)
    print("  TOP 5 RECOMMENDATIONS")
    print(f"  Profile: genre={user_prefs['genre']} | mood={user_prefs['mood']} | energy={user_prefs['target_energy']}")
    print("=" * 56)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  -  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']:.2f}")
        print(f"       Score: {score:.2f} / 4.00")
        print(f"       Why:   {explanation}")
    print()
    print("=" * 56)


if __name__ == "__main__":
    main()
