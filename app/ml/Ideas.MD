Ja. Wenn du nur `distance/elevation/time → expected rank` machst, ist das **fast dasselbe wie deine Projection**.

Was du mit ML machen solltest, das du **noch nicht hast**:

# 1. Athlete Type Detection

Nicht fragen:

> Wo würdest du landen?

Sondern erkennen:

> Was für ein Läufertyp bist du?

Beispiel Output:

```txt
Athlete Type: Vertical Endurance Specialist

Strengths:
- very strong on steep races
- strong on long efforts
- weaker on flat/runnable speed races

Best race profile:
40–80 km, 2500–5000 hm, technical mountain terrain
```

ML-Idee:

```txt
Clustering
```

Zum Beispiel:

```txt
KMeans / HDBSCAN
```

Du clusterst Rennen oder Leistungen in Profile:

```txt
Flat Speed
Rolling Trail
Vertical Beast
Mountain Ultra
Long Slow Grind
Elite Short Trail
```

Das ist neu.

---

# 2. Race DNA Clustering

Du gruppierst nicht nach UTMB-Kategorie, sondern nach echtem Profil.

Beispiel:

```txt
Race DNA:
Technical Mountain Ultra
```

Statt:

```txt
100K
```

Features:

```txt
distance_km
elevation_m
vertical_density
winner_time
median_time
time_spread
top10_avg_time
difficulty_score
```

Dann ML:

```python
KMeans(n_clusters=6)
```

Das erzeugt echte „Race Archetypes“.

Das ist viel cooler als normale Filter.

---

# 3. Anomaly Detection

Das wäre richtig stark.

ML erkennt:

```txt
This race is unusually hard for its distance.
```

Beispiel:

```txt
A 42 km race with 3500 hm and very slow median time
```

Output:

```txt
Hidden Beast Score: 94/100
Reason: Median finish time is much slower than comparable races.
```

ML:

```txt
IsolationForest
LocalOutlierFactor
```

Damit findest du:

```txt
Underrated brutal races
Overrated easy races
Fast races
Slow technical races
```

Das hast du garantiert noch nicht.

---

# 4. Race Difficulty Model

Nicht Formel:

```txt
distance + elevation / 100
```

Sondern ML lernt Difficulty aus echten Resultaten.

Target:

```txt
median_time oder winner_time
```

Features:

```txt
distance
elevation
category
n_results
country
```

Dann:

```txt
expected_median_time
actual_median_time
difficulty_above_expected
```

Das ist extrem gut.

Beispiel:

```txt
Expected median time: 8:20h
Actual median time: 10:45h
Race is 29% harder than expected.
```

Das ist ein echter ML-Mehrwert.

---

# 5. Similar Athlete Performance Simulation

Das wäre später sehr stark.

Du suchst im Dataset ähnliche Leistungen/Rennen und leitest daraus ab:

```txt
Athletes with a similar profile usually perform best at...
```

ML/Analytics:

```txt
Nearest Neighbors
Similarity Search
```

Das ist eher Recommendation System als Prediction.

---

# Mein Favorit für dich

Mach jetzt:

# ML Race Difficulty Engine

Warum?

Weil du dadurch etwas bekommst, was du noch nicht hast:

```txt
Welche Rennen sind schwerer/leichter als sie auf dem Papier wirken?
```

Das ist stark für:

* Portfolio
* UI
* Content
* echte Nutzer
* SaaS
* ML-Lerneffekt

---

# Konkretes Feature

## Neue Section:

```txt
Race Difficulty Intelligence
```

Für jedes Rennen zeigst du:

```txt
Expected Median Time
Actual Median Time
Difficulty Delta
Hidden Beast Score
Race Archetype
```

Beispiel:

```txt
Race: Mozart 100
Expected Median Time: 13:20h
Actual Median Time: 15:05h
Difficulty Delta: +13.1%
Hidden Beast Score: 82/100
Archetype: Runnable Mountain Ultra
```

Das ist nicht nur Projection.
Das ist **ML-basierte Race Analyse**.

---

# MVP-Reihenfolge

## 1. Trainiere Modell

Input:

```txt
distance_km
elevation_m
vertical_density
race_effort
race_category
n_results
```

Target:

```txt
median_time_minutes
```

---

## 2. Berechne Difficulty Delta

```python
difficulty_delta = actual_median_time / predicted_median_time - 1
```

---

## 3. Skaliere zu Score

```python
hidden_beast_score = min(100, max(0, 50 + difficulty_delta * 200))
```

---

## 4. UI

Zeige pro Rennen:

```txt
On-paper difficulty
Real-world difficulty
Hidden Beast Score
```

---

# Das ist der nächste richtige Schritt

Nicht:

```txt
Predict my placement
```

Sondern:

```txt
Learn race difficulty from real-world results.
```

Das ist wirklich ML.
