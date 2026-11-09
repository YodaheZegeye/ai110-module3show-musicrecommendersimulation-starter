# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Imagine a judge at a talent show who has been given a scorecard with three criteria. For every song in the catalog, the judge checks three things and assigns points.

First, does the song belong to the genre the user said they like? If yes, it gets 2 points — the biggest reward, because genre is the most reliable signal of someone's taste. If no, it gets nothing for that category.

Second, does the song match the mood the user is looking for right now? A match earns 1 point. Mood matters, but it is worth less than genre because the same person might want happy music one day and chill music the next — it depends on the moment.

Third, how close is the song's energy level to what the user wants? Energy is measured on a scale from 0 (completely calm) to 1 (maximum intensity). The system calculates the gap between the song's energy and the user's target, then subtracts that gap from 1.0. A perfect match gives a full extra point; a song that is very far away gives almost nothing. This means no song ever scores zero on energy — every song contributes something to the total.

Once all three numbers are added up, every song has a score out of 4. The system then sorts all 18 songs from highest to lowest score and returns the top 5. Alongside each recommendation, it prints a plain-English explanation of exactly which rules fired and by how much — so the user always knows *why* a song was chosen, not just *that* it was chosen.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
