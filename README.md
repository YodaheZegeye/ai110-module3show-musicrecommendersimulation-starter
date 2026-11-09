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

Three standard profiles and three adversarial edge-case profiles were run against the 18-song catalog.

### Standard Profile 1 — High-Energy Pop

```
==============================================================
  PROFILE: High-Energy Pop
  genre=pop | mood=happy | energy=0.9
==============================================================

  #1  Sunrise City  -  Neon Echo
       Genre: pop  |  Mood: happy  |  Energy: 0.82
       Score: 3.92 / 4.00
       Why:   genre match (pop, +2.0); mood match (happy, +1.0); energy proximity +0.92 (target 0.90, song 0.82)

  #2  Gym Hero  -  Max Pulse
       Genre: pop  |  Mood: intense  |  Energy: 0.93
       Score: 2.97 / 4.00
       Why:   genre match (pop, +2.0); energy proximity +0.97 (target 0.90, song 0.93)

  #3  Rooftop Lights  -  Indigo Parade
       Genre: indie pop  |  Mood: happy  |  Energy: 0.76
       Score: 1.86 / 4.00
       Why:   mood match (happy, +1.0); energy proximity +0.86 (target 0.90, song 0.76)

  #4  Storm Runner  -  Voltline
       Genre: rock  |  Mood: intense  |  Energy: 0.91
       Score: 0.99 / 4.00
       Why:   energy proximity +0.99 (target 0.90, song 0.91)

  #5  Pulse at Dawn  -  Echosphere
       Genre: edm  |  Mood: euphoric  |  Energy: 0.95
       Score: 0.95 / 4.00
       Why:   energy proximity +0.95 (target 0.90, song 0.95)

==============================================================
```

### Standard Profile 2 — Chill Lofi

```
==============================================================
  PROFILE: Chill Lofi
  genre=lofi | mood=chill | energy=0.4
==============================================================

  #1  Midnight Coding  -  LoRoom
       Genre: lofi  |  Mood: chill  |  Energy: 0.42
       Score: 3.98 / 4.00
       Why:   genre match (lofi, +2.0); mood match (chill, +1.0); energy proximity +0.98 (target 0.40, song 0.42)

  #2  Library Rain  -  Paper Lanterns
       Genre: lofi  |  Mood: chill  |  Energy: 0.35
       Score: 3.95 / 4.00
       Why:   genre match (lofi, +2.0); mood match (chill, +1.0); energy proximity +0.95 (target 0.40, song 0.35)

  #3  Focus Flow  -  LoRoom
       Genre: lofi  |  Mood: focused  |  Energy: 0.40
       Score: 3.00 / 4.00
       Why:   genre match (lofi, +2.0); energy proximity +1.00 (target 0.40, song 0.40)

  #4  Spacewalk Thoughts  -  Orbit Bloom
       Genre: ambient  |  Mood: chill  |  Energy: 0.28
       Score: 1.88 / 4.00
       Why:   mood match (chill, +1.0); energy proximity +0.88 (target 0.40, song 0.28)

  #5  Coffee Shop Stories  -  Slow Stereo
       Genre: jazz  |  Mood: relaxed  |  Energy: 0.37
       Score: 0.97 / 4.00
       Why:   energy proximity +0.97 (target 0.40, song 0.37)

==============================================================
```

### Standard Profile 3 — Deep Intense Rock

```
==============================================================
  PROFILE: Deep Intense Rock
  genre=rock | mood=intense | energy=0.92
==============================================================

  #1  Storm Runner  -  Voltline
       Genre: rock  |  Mood: intense  |  Energy: 0.91
       Score: 3.99 / 4.00
       Why:   genre match (rock, +2.0); mood match (intense, +1.0); energy proximity +0.99 (target 0.92, song 0.91)

  #2  Gym Hero  -  Max Pulse
       Genre: pop  |  Mood: intense  |  Energy: 0.93
       Score: 1.99 / 4.00
       Why:   mood match (intense, +1.0); energy proximity +0.99 (target 0.92, song 0.93)

  #3  Pulse at Dawn  -  Echosphere
       Genre: edm  |  Mood: euphoric  |  Energy: 0.95
       Score: 0.97 / 4.00
       Why:   energy proximity +0.97 (target 0.92, song 0.95)

  #4  Shatter the Grid  -  Iron Veil
       Genre: metal  |  Mood: angry  |  Energy: 0.97
       Score: 0.95 / 4.00
       Why:   energy proximity +0.95 (target 0.92, song 0.97)

  #5  Sunrise City  -  Neon Echo
       Genre: pop  |  Mood: happy  |  Energy: 0.82
       Score: 0.90 / 4.00
       Why:   energy proximity +0.90 (target 0.92, song 0.82)

==============================================================
```

### Adversarial Profile 1 — Conflicting preferences (high energy + melancholic mood)

```
==============================================================
  PROFILE: ADVERSARIAL: Conflict (high energy + melancholic mood)
  genre=folk | mood=melancholic | energy=0.95
==============================================================

  #1  Hollow River  -  June Ashford
       Genre: folk  |  Mood: melancholic  |  Energy: 0.30
       Score: 3.35 / 4.00
       Why:   genre match (folk, +2.0); mood match (melancholic, +1.0); energy proximity +0.35 (target 0.95, song 0.30)

  #2  Pulse at Dawn  -  Echosphere
       Genre: edm  |  Mood: euphoric  |  Energy: 0.95
       Score: 1.00 / 4.00
       Why:   energy proximity +1.00 (target 0.95, song 0.95)

  #3  Gym Hero  -  Max Pulse
       Genre: pop  |  Mood: intense  |  Energy: 0.93
       Score: 0.98 / 4.00
       Why:   energy proximity +0.98 (target 0.95, song 0.93)

  #4  Shatter the Grid  -  Iron Veil
       Genre: metal  |  Mood: angry  |  Energy: 0.97
       Score: 0.98 / 4.00
       Why:   energy proximity +0.98 (target 0.95, song 0.97)

  #5  Storm Runner  -  Voltline
       Genre: rock  |  Mood: intense  |  Energy: 0.91
       Score: 0.96 / 4.00
       Why:   energy proximity +0.96 (target 0.95, song 0.91)

==============================================================
```

### Adversarial Profile 2 — Ghost genre (k-pop not in catalog)

```
==============================================================
  PROFILE: ADVERSARIAL: Ghost genre (k-pop - not in catalog)
  genre=k-pop | mood=happy | energy=0.78
==============================================================

  #1  Rooftop Lights  -  Indigo Parade
       Genre: indie pop  |  Mood: happy  |  Energy: 0.76
       Score: 1.98 / 4.00
       Why:   mood match (happy, +1.0); energy proximity +0.98 (target 0.78, song 0.76)

  #2  Sunrise City  -  Neon Echo
       Genre: pop  |  Mood: happy  |  Energy: 0.82
       Score: 1.96 / 4.00
       Why:   mood match (happy, +1.0); energy proximity +0.96 (target 0.78, song 0.82)

  #3  Night Drive Loop  -  Neon Echo
       Genre: synthwave  |  Mood: moody  |  Energy: 0.75
       Score: 0.97 / 4.00
       Why:   energy proximity +0.97 (target 0.78, song 0.75)

  #4  Street Lights Fade  -  Marcus Cole
       Genre: hip-hop  |  Mood: confident  |  Energy: 0.72
       Score: 0.94 / 4.00
       Why:   energy proximity +0.94 (target 0.78, song 0.72)

  #5  Storm Runner  -  Voltline
       Genre: rock  |  Mood: intense  |  Energy: 0.91
       Score: 0.87 / 4.00
       Why:   energy proximity +0.87 (target 0.78, song 0.91)

==============================================================
```

### Adversarial Profile 3 — Contradictory vibe (ambient genre + intense mood + very low energy)

```
==============================================================
  PROFILE: ADVERSARIAL: Contradictory vibe (ambient + intense mood)
  genre=ambient | mood=intense | energy=0.15
==============================================================

  #1  Spacewalk Thoughts  -  Orbit Bloom
       Genre: ambient  |  Mood: chill  |  Energy: 0.28
       Score: 2.87 / 4.00
       Why:   genre match (ambient, +2.0); energy proximity +0.87 (target 0.15, song 0.28)

  #2  Storm Runner  -  Voltline
       Genre: rock  |  Mood: intense  |  Energy: 0.91
       Score: 1.24 / 4.00
       Why:   mood match (intense, +1.0); energy proximity +0.24 (target 0.15, song 0.91)

  #3  Gym Hero  -  Max Pulse
       Genre: pop  |  Mood: intense  |  Energy: 0.93
       Score: 1.22 / 4.00
       Why:   mood match (intense, +1.0); energy proximity +0.22 (target 0.15, song 0.93)

  #4  Morning Sonata  -  Clara Voss
       Genre: classical  |  Mood: peaceful  |  Energy: 0.22
       Score: 0.93 / 4.00
       Why:   energy proximity +0.93 (target 0.15, song 0.22)

  #5  Hollow River  -  June Ashford
       Genre: folk  |  Mood: melancholic  |  Energy: 0.30
       Score: 0.85 / 4.00
       Why:   energy proximity +0.85 (target 0.15, song 0.30)

==============================================================
```

---

## Experiments You Tried

### What the adversarial profiles revealed

**Conflict profile (folk/melancholic/energy=0.95):** The genre+mood combo locked in Hollow River at #1 (score 3.35) even though its energy (0.30) is the furthest possible from the target (0.95). The categorical match earned 3.0 points; the energy mismatch only subtracted 0.65. This confirms the bias noted in the algorithm recipe: genre dominates so heavily that it can surface a nearly wrong-energy song over a perfect-energy one from a different genre. Spots #2–5 are all high-energy songs with zero categorical match — purely sorted by energy proximity.

**Ghost genre (k-pop):** With zero genre bonuses available, the entire top-5 was decided by mood and energy alone. The system degraded gracefully — it still returned five reasonable results rather than erroring. Max score dropped from ~4.0 to ~2.0, exposing that most of the recommender's confidence comes from genre match.

**Contradictory vibe (ambient/intense/energy=0.15):** The system was split between two incompatible signals. Spacewalk Thoughts won on genre alone (2.87) even though its mood is chill, not intense. Storm Runner and Gym Hero came second and third purely on mood match, scoring 1.24 and 1.22 — but with energy penalties near 0.75 each because their energy (0.91–0.93) is the opposite of the 0.15 target. No song in the catalog satisfies all three constraints simultaneously, which is what this profile was designed to expose.

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



