# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

A rule-based content-based music recommender that scores songs by how closely they match a user's stated genre, mood, and energy preferences.

---

## 2. Intended Use

VibeMatch 1.0 is designed for classroom exploration of how recommender systems work. It is meant for students and curious people who want to understand the basic mechanics behind "you might also like" features — not for use in a real music app.

It assumes the user can describe their own taste in simple terms: a preferred genre, a current mood, and a rough energy level. It works best when the catalog contains at least a few songs in the user's genre.

**This system should NOT be used for:**
- Making real music recommendations to real listeners — the catalog is 18 songs, which is far too small to cover any real taste
- Deciding what gets promoted or surfaced on a platform — the scoring has known biases that would unfairly under-serve low-energy listeners and niche genre fans
- Any context where a user's experience or opportunities depend on the output

---

## 3. How the Model Works

Imagine a judge at a talent show who has been given a scorecard with three criteria. For every song in the catalog, the judge checks three things and assigns points.

First, does the song belong to the genre the user said they like? If yes, it gets 2 points — the biggest reward, because genre is the most reliable signal of someone's taste. If no, it gets nothing for that category.

Second, does the song match the mood the user is looking for right now? A match earns 1 point. Mood matters, but it is worth less than genre because the same person might want happy music one day and chill music the next — it depends on the moment.

Third, how close is the song's energy level to what the user wants? Energy is measured on a scale from 0 (completely calm) to 1 (maximum intensity). The system calculates the gap between the song's energy and the user's target, then subtracts that gap from 1.0. A perfect match gives a full extra point; a song that is very far away gives almost nothing. This means no song ever scores zero on energy — every song contributes something to the total.

Once all three numbers are added up, every song has a score out of 4. The system then sorts all 18 songs from highest to lowest score and returns the top 5. Alongside each recommendation, it prints a plain-English explanation of exactly which rules fired and by how much — so the user always knows *why* a song was chosen, not just *that* it was chosen.

---

## 4. Data

The catalog contains 18 songs stored in a CSV file. Each song has 10 attributes: a unique ID, title, artist name, genre, mood, energy (0–1), tempo in BPM, valence (how positive the song feels, 0–1), danceability (0–1), and acousticness (how acoustic vs. electronic the sound is, 0–1).

The original starter file had 10 songs. Eight more were added manually to cover genres not in the original set: hip-hop, R&B, classical, metal, country, EDM, folk, and reggae.

Genres represented: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, R&B, classical, metal, country, EDM, folk, reggae (15 genres across 18 songs).

Moods represented: happy, chill, intense, relaxed, moody, focused, confident, romantic, peaceful, angry, nostalgic, euphoric, melancholic, uplifting (14 moods).

What is missing: lyrics, language, instrumentation details, release era, and listening context (e.g., commute, workout, sleep). The dataset also has no information about which songs real users have actually enjoyed together, so it cannot learn from listening patterns the way Spotify or Apple Music does. Valence, danceability, and acousticness are stored but not currently used in scoring.

---

## 5. Strengths

The system works best when the user's genre and mood are well-represented in the catalog. A lofi listener asking for chill music reliably gets Midnight Coding and Library Rain at the top — both are genuinely appropriate picks. The Deep Intense Rock profile found Storm Runner as a near-perfect match (3.99 out of 4.00) on the first try.

The explainability is a genuine strength. Every recommendation comes with a reason string that shows exactly which rules fired and what each contributed. A user can read "genre match (+2.0); mood match (+1.0); energy proximity +0.99" and immediately understand why a song was chosen. Most real recommenders give no explanation at all.

The system also handles unknown inputs gracefully. When given a genre that does not exist in the catalog (like k-pop), it does not crash — it falls back to mood and energy matching and still returns five results. The rankings are weaker but the output is always valid.

---

## 6. Limitations and Bias

**Weakness discovered during experiments: energy distribution creates an invisible filter bubble for low-energy listeners.**

The catalog contains 8 songs with energy ≥ 0.70 (44%) but only 5 songs with energy below 0.40 (28%), and just 2 songs below 0.30. The scoring formula treats all energy targets equally — it always computes `1 − |difference|` — but the catalog does not. A user who wants calm, quiet music (target energy ≈ 0.15) will find their top-5 filled with songs at energy 0.28–0.42 that are still noticeably more intense than what they asked for, while a user targeting energy 0.90 has six songs clustered right at their preference. The formula is fair; the data is not. This is a classic example of how bias enters a recommender not through the algorithm itself but through the training data it was built on — in a production system this would silently under-serve a whole category of users (ambient listeners, classical fans, people studying or winding down) without ever throwing an error.

A second, related bias is catalog depth inequality: lofi is the only genre with 3 entries, pop has 2, and all other 13 genres have exactly 1 song. A lofi listener will almost always see 3 genre-matched songs in their top-5; a metal or jazz listener gets at most 1, and the remaining 4 picks are genre-miss songs padded in by energy. This makes confidence in the recommendations structurally unequal across users — not because of anything they did, but because of which genres the catalog happened to cover more deeply.

---

## 7. Evaluation

Six user profiles were run against the 18-song catalog: three designed to test normal use cases, and three designed to break or confuse the system.

---

### Profile 1 vs. Profile 2 — High-Energy Pop vs. Chill Lofi

These two profiles are near-opposites. The pop listener wants upbeat, fast, dance-ready songs; the lofi listener wants something quiet and low-key to study or relax to. The results reflected this cleanly. Pop recommendations clustered around energy levels of 0.80–0.93, while lofi recommendations clustered around 0.35–0.42. What made sense: the system correctly split these two groups apart because their energy targets are so far from each other that almost no song could satisfy both. What was surprising: the lofi profile produced three genre-matched results (Midnight Coding, Library Rain, Focus Flow) while the pop profile only got two (Sunrise City, Gym Hero). That is not because pop is less popular — it is because lofi happened to have more entries in the catalog. A real user would not know their genre just has less catalog depth.

---

### Profile 2 vs. Profile 3 — Chill Lofi vs. Deep Intense Rock

Both profiles have a clear, well-represented genre in the catalog, so both got strong top picks. The lofi profile's #1 scored 3.98 out of 4.00; the rock profile's #1 scored 3.99. Both are almost perfect matches. The interesting difference is in spots #2 through #5. The lofi list stays coherent — all five songs are genuinely calm and quiet. The rock list falls off a cliff after the first pick: Storm Runner is exactly right, but Gym Hero (pop), Pulse at Dawn (EDM), and Shatter the Grid (metal) appear next because they all happen to have high energy near 0.92. The system does not know that high-energy EDM and high-energy rock feel nothing alike to a listener. It only sees the number.

---

### Profile 1 vs. Profile 3 — High-Energy Pop vs. Deep Intense Rock

These profiles share almost the same energy target (0.90 vs. 0.92) but differ on genre and mood. The overlap in results is revealing: Gym Hero appeared in both top-5 lists because it is a pop song with intense mood and energy 0.93, which satisfies the energy requirement for both users even though one wants happy pop and the other wants intense rock. This is a good example of how "Gym Hero keeps showing up for people who just want Happy Pop." The system sees that Gym Hero is pop (genre match, +2.0 points) and that its energy of 0.93 is close to the target of 0.90. It does not care that the song is labeled "intense" rather than "happy" — it still ranks second because the genre match is worth more than the mood mismatch. To a non-programmer: imagine a music store clerk who checks whether the CD is in the right genre section and roughly the right tempo, but never actually listens to whether the vibe feels happy or aggressive. That is what the scorer is doing.

---

### Adversarial Profile 1 — Conflicting preferences (folk/melancholic + energy 0.95)

This profile was designed to ask an impossible question: recommend a folk song that is also high energy. Folk music in the catalog sits at energy 0.30, and no other folk songs exist. The result was that Hollow River landed at #1 with a score of 3.35 — ahead of Pulse at Dawn (edm, energy 0.95 exactly) which only scored 2.00 in the weighted experiment. This was the most surprising outcome. A human listener handed these instructions would probably say "just give me something high-energy, the folk part is flexible." The system did the opposite — it locked onto genre and mood match and accepted a song that is almost as far from the energy target as possible. This revealed that categorical labels can override what the numbers are clearly saying.

---

### Adversarial Profile 2 — Ghost genre (k-pop not in catalog)

When no songs in the catalog match the requested genre, the entire genre weight goes to waste. The best score any song could reach dropped from 4.00 to about 2.00. The system still returned five results, so it did not crash or refuse — it just became noticeably less confident. The top two picks (Rooftop Lights, Sunrise City) both matched on mood and energy, which is a reasonable fallback. What this test showed is that the system degrades gracefully when given an unknown genre, but it has no way to signal to the user that it is working with less information than usual. A real recommender would ideally say "I do not have any k-pop in the catalog — here are the closest alternatives."

---

### Adversarial Profile 3 — Contradictory vibe (ambient genre + intense mood + energy 0.15)

No song in the catalog is simultaneously ambient, intense, and low energy. The system had to split its bets. Spacewalk Thoughts won on genre alone, even though its mood is chill and its energy penalty was minor. Storm Runner and Gym Hero appeared next because their mood is intense, even though their energy of 0.91–0.93 is almost the maximum distance from the target of 0.15. In plain terms: the system saw "intense" and said yes, without noticing that the user is asking for something that feels calm and slow. The mood label matched but the actual feeling of the song could not be more different. This exposed that the system treats each feature as an independent checklist item. It has no concept of features contradicting each other.

---

## 8. Ideas for Improvement

**Add valence to the scoring formula.** Valence measures how emotionally positive a song feels, on a scale from 0 (dark, sad) to 1 (bright, happy). It is already stored for every song but currently ignored. Adding it would let the system tell the difference between a high-energy metal song (angry, valence ≈ 0.31) and a high-energy EDM song (euphoric, valence ≈ 0.88) — two songs that look identical under the current scorer.

**Balance the catalog before scoring.** Right now lofi has 3 songs and most genres have 1. A simple fix would be to either add more songs in underrepresented genres, or cap genre-match bonuses at a "per genre" rate so users are not punished for liking a less-covered style. The goal is to make confidence in the recommendations equal across all user types.

**Add a low-confidence warning.** When the best score returned is below a threshold (say 2.0 out of 4.0), the system should tell the user it could not find a strong match — either because their genre is missing from the catalog or because their preferences conflict. Right now it silently returns five weak picks as if they were genuine recommendations, which is misleading.

---

## 9. Personal Reflection

**Biggest learning moment**

The biggest learning moment came not from writing code, but from running the adversarial profiles. I designed the "conflicting preferences" profile — folk genre, melancholic mood, but energy 0.95 — specifically expecting it to expose the energy scoring. What I did not expect was how completely the genre and mood labels overruled the numbers. Hollow River scored 3.35 and landed at #1 even though its energy of 0.30 was almost as far from the target as physically possible. A song with a perfect energy match — Pulse at Dawn at exactly 0.95 — only scored 2.00 and sat at #2. The formula was doing exactly what I told it to do, and the result was still wrong. That moment made it real: writing correct code is not the same as writing code that does what you actually want.

**How AI tools helped, and when I had to double-check them**

The AI assistant was most useful for two things: translating design decisions into working Python quickly, and asking questions that forced me to be more precise about what I actually wanted. When I described the scoring recipe in plain English — "reward songs closer to the user's energy target, not just higher or lower" — it immediately suggested `1 - abs(difference)` and explained why that formula behaves the way it does. That saved a lot of trial and error.

Where I had to be careful was with the weights. The AI suggested a reasonable starting point, but it had no way of knowing which direction mattered more for this specific catalog. When it initially proposed equal weights for genre and mood, I had to push back based on my own reasoning: genre is a stable identity preference, mood is a moment-to-moment state. The AI accepted that reasoning and adjusted, but the judgment call was mine. The lesson was that AI tools are fast at implementation but cannot supply the design intuition — that still requires a human who understands the problem.

I also had to verify the math independently after the weight-shift experiment. The AI confirmed the max score stayed at 4.0 when I halved genre and doubled energy, but I calculated it by hand anyway (1.0 + 1.0 + 2.0 = 4.0) before trusting the output. When you change weights, the whole scale shifts in ways that are easy to miss.

**What surprised me about simple algorithms feeling like recommendations**

The thing that surprised me most is how much the explainability contributed to the feeling of a real recommendation. When the terminal printed "genre match (indie pop, +2.0); mood match (happy, +1.0); energy proximity +0.99," it felt like the system understood something — even though it was just three arithmetic operations. The explanation created a sense of reasoning where there was really just addition and sorting.

The second surprise was how quickly the results became intuitive. After running a few profiles, I could predict roughly where songs would rank before seeing the output. That meant the scoring logic had become a mental model — which is a sign the algorithm was at least internally consistent, even if imperfect.

**What I would try next**

If I extended this project, the first thing I would add is valence to the scoring formula. Right now the system cannot tell the difference between a dark, angry high-energy song and a joyful high-energy one. Valence is already stored in the CSV — it would take one line of code to include it, and it would meaningfully change the recommendations for users who care about emotional tone.

I would also want to try replacing the hand-crafted weights with something learned from data. If I collected ratings from real listeners — even just asking people to rate five recommendations on a 1–5 scale — I could use that feedback to adjust the weights automatically toward what actually satisfies people, rather than what seems logical in theory. That would be the first step from a rule-based system toward a real machine learning one.
