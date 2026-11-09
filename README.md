# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This simulation builds a lightweight content-based music recommender that scores songs by how closely their attributes match a user's stated preferences. Rather than learning from listening history, it uses hand-crafted feature weights to rank a small catalog and return the top-k matches with a plain-language explanation for each pick.

---

## How The System Works

Real-world recommenders like Spotify or YouTube learn from massive amounts of behavioral data — plays, skips, likes — to infer what a listener wants next. Under the hood they often combine **collaborative filtering** (people like you also liked…) with **content-based filtering** (this song has similar sonic features to ones you've played). This simulation focuses purely on the content-based side: each song is described with measurable attributes, the user is described with a taste profile, and the system computes a match score for every song in the catalog. The top-k highest-scoring songs become the recommendations, each accompanied by a plain-language explanation of why it was chosen.

### Data flow

```
user_prefs (dict)          data/songs.csv
      │                          │
      └──────────┬───────────────┘
                 ▼
     for each song → score_song()
         genre match?   +2.0 or 0
         mood match?    +1.0 or 0
         energy prox    0.0–1.0
                 │
                 ▼
     sort all scores descending
                 │
                 ▼
     return top k (song, score, explanation)
```

### Algorithm Recipe

Each song is scored out of a maximum of **4.0 points** using three rules:

| Rule | Formula | Max pts | Rationale |
|---|---|---|---|
| Genre match | `+2.0` if `song.genre == user.genre` | 2.0 | Genre is a stable identity preference — a wrong genre is a hard vibe miss regardless of other features |
| Mood match | `+1.0` if `song.mood == user.mood` | 1.0 | Mood is contextual; it refines the vibe within a genre but matters less than the genre itself |
| Energy proximity | `1.0 − \|song.energy − target_energy\|` | 1.0 | Rewards closeness to a target, not just high or low values; always contributes something |

```
score = genre_match        # +2.0 or 0
      + mood_match         # +1.0 or 0
      + energy_proximity   # 1.0 − |song.energy − target_energy|

max score = 4.0
```

Songs are scored independently, sorted descending, and the top `k` are returned (default `k = 5`).

### `Song` features

| Feature | Type | Used in scoring |
|---|---|---|
| `genre` | str | Yes — categorical match (+2.0) |
| `mood` | str | Yes — categorical match (+1.0) |
| `energy` | float 0–1 | Yes — proximity to `target_energy` |
| `valence` | float 0–1 | Stored; available for future experiments |
| `acousticness` | float 0–1 | Stored; available for future experiments |
| `tempo_bpm` | float | Stored; available for future experiments |
| `danceability` | float 0–1 | Stored; available for future experiments |

### `UserProfile` fields

| Field | Type | Used for |
|---|---|---|
| `favorite_genre` | str | Genre match rule |
| `favorite_mood` | str | Mood match rule |
| `target_energy` | float 0–1 | Energy proximity rule |
| `target_valence` | float 0–1 | Available for future scoring experiments |
| `target_acousticness` | float 0–1 | Available for future scoring experiments |

### Expected biases and limitations

- **Genre over-prioritization.** At 50% of the max score, genre dominates. A perfect-energy, perfect-mood song from a different genre scores at most 2.0 out of 4.0, while a genre-matching song with poor energy still scores at least 2.47. This can bury genuinely fitting songs just because they carry the wrong genre label.

- **Mood is nearly a tiebreaker.** Worth only 25% of max score, mood rarely changes which songs appear in the top-5 — it mainly re-orders songs that already matched on genre. A chill jazz song and a focused jazz song look almost identical to this scorer.

- **Energy is the only continuous signal.** Valence and acousticness are ignored, so the system cannot distinguish a dark high-energy metal song from a euphoric high-energy EDM track. Both score identically for a user targeting energy 0.95.

- **Small catalog amplifies all of the above.** With 18 songs and 10 genres, most users will have zero or one genre match, making mood and energy do most of the real ranking work despite their lower weights.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Profile used: `genre=indie pop | mood=happy | target_energy=0.75`

```
========================================================
  TOP 5 RECOMMENDATIONS
  Profile: genre=indie pop | mood=happy | energy=0.75
========================================================

  #1  Rooftop Lights  -  Indigo Parade
       Genre: indie pop  |  Mood: happy  |  Energy: 0.76
       Score: 3.99 / 4.00
       Why:   genre match (indie pop, +2.0); mood match (happy, +1.0); energy proximity +0.99 (target 0.75, song 0.76)

  #2  Sunrise City  -  Neon Echo
       Genre: pop  |  Mood: happy  |  Energy: 0.82
       Score: 1.93 / 4.00
       Why:   mood match (happy, +1.0); energy proximity +0.93 (target 0.75, song 0.82)

  #3  Night Drive Loop  -  Neon Echo
       Genre: synthwave  |  Mood: moody  |  Energy: 0.75
       Score: 1.00 / 4.00
       Why:   energy proximity +1.00 (target 0.75, song 0.75)

  #4  Street Lights Fade  -  Marcus Cole
       Genre: hip-hop  |  Mood: confident  |  Energy: 0.72
       Score: 0.97 / 4.00
       Why:   energy proximity +0.97 (target 0.75, song 0.72)

  #5  Sunshine Riddim  -  Coastal Roots
       Genre: reggae  |  Mood: uplifting  |  Energy: 0.64
       Score: 0.89 / 4.00
       Why:   energy proximity +0.89 (target 0.75, song 0.64)

========================================================
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



