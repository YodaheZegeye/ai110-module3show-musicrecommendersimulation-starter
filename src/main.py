"""
Command line runner for the Music Recommender Simulation.

Runs six user profiles — three standard and three adversarial —
and prints ranked recommendations for each.
"""

import os
from recommender import load_songs, recommend_songs

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")

PROFILES = [
    # --- Standard profiles ---
    {
        "label":         "High-Energy Pop",
        "genre":         "pop",
        "mood":          "happy",
        "target_energy": 0.90,
    },
    {
        "label":         "Chill Lofi",
        "genre":         "lofi",
        "mood":          "chill",
        "target_energy": 0.40,
    },
    {
        "label":         "Deep Intense Rock",
        "genre":         "rock",
        "mood":          "intense",
        "target_energy": 0.92,
    },
    # --- Adversarial / edge-case profiles ---
    {
        "label":         "ADVERSARIAL: Conflict (high energy + melancholic mood)",
        "genre":         "folk",
        "mood":          "melancholic",
        "target_energy": 0.95,
        # Expects: genre miss on most songs; mood only matches Hollow River (low energy).
        # Will the scorer surface a high-energy song over the only mood match?
    },
    {
        "label":         "ADVERSARIAL: Ghost genre (k-pop - not in catalog)",
        "genre":         "k-pop",
        "mood":          "happy",
        "target_energy": 0.78,
        # Expects: zero genre bonuses for every song; ranking falls entirely to
        # mood and energy. Tests whether the system degrades gracefully.
    },
    {
        "label":         "ADVERSARIAL: Contradictory vibe (ambient + intense mood)",
        "genre":         "ambient",
        "mood":          "intense",
        "target_energy": 0.15,
        # Expects: Spacewalk Thoughts earns genre match but mood=chill, not intense.
        # No song has ambient+intense. Tests genre-only partial match edge case.
    },
]


def print_recommendations(label: str, user_prefs: dict, songs: list) -> str:
    """Run recommender, print results, and return the block as a string for README."""
    recommendations = recommend_songs(user_prefs, songs, k=5)
    lines = []
    lines.append("=" * 62)
    lines.append(f"  PROFILE: {label}")
    lines.append(f"  genre={user_prefs.get('genre')} | mood={user_prefs.get('mood')} | energy={user_prefs.get('target_energy')}")
    lines.append("=" * 62)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        lines.append(f"\n  #{rank}  {song['title']}  -  {song['artist']}")
        lines.append(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']:.2f}")
        lines.append(f"       Score: {score:.2f} / 4.00")
        lines.append(f"       Why:   {explanation}")
    lines.append("")
    lines.append("=" * 62)
    block = "\n".join(lines)
    print(block)
    return block


def main() -> None:
    songs = load_songs(CSV_PATH)
    print(f"Loaded songs: {len(songs)}\n")

    for profile in PROFILES:
        label = profile.pop("label")
        print_recommendations(label, profile, songs)
        profile["label"] = label   # restore for re-use
        print()


if __name__ == "__main__":
    main()
