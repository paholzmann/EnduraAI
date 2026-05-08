Ja. Für **Performance Metrics** würde ich nicht nur einzelne Ergebnisse anzeigen, sondern eine kleine **Analyse-Seite**, die aus wenigen Inputs mehrere sinnvolle Metriken ableitet.

## 1. Inputs oben als Calculator Card

```text
Distance (km)
Elevation Gain (m+)
Total Time (hours)
```

Optional später:

```text
Runner Weight
Technicality
Weather
Target Pace
```

---

## 2. Metric Cards

Direkt nach dem Absenden zeigst du einzelne KPI-Cards:

```text
Race Effort
116.0 km-effort
```

```text
Vertical Rate
833 m/km
```

```text
Flat Equivalent Pace
6:12 / km-effort
```

```text
Difficulty Score
87 / 100
```

```text
Race Category
100K
```

```text
Vertical Speed
742 m+/h
```

---

## 3. Gute Struktur für deine Seite

```html
<section class="metrics-input-section">
  <form class="metrics-form">
    <!-- distance, elevation, time -->
  </form>
</section>

<section class="metrics-overview-grid">
  <article class="metric-card"></article>
  <article class="metric-card"></article>
  <article class="metric-card"></article>
  <article class="metric-card"></article>
</section>

<section class="metrics-analysis-section">
  <article class="card">
    <h2>Race Profile</h2>
  </article>

  <article class="card">
    <h2>Performance Breakdown</h2>
  </article>
</section>
```

---

## 4. Welche Metrik wohin?

| Metrik                                          | UI-Darstellung            |
| ----------------------------------------------- | ------------------------- |
| `calculate_race_effort()`                       | große KPI Card            |
| `calculate_vertical_rate()`                     | KPI Card + Race Profile   |
| `calculate_estimated_pace_on_flat_equivalent()` | Performance Card          |
| `calculate_race_difficulty_score()`             | Score Ring / Progress Bar |
| `calculate_race_category()`                     | Badge                     |
| `generate_category_label()`                     | Badge mit Text            |
| `calculate_vertical_per_hour()`                 | KPI Card                  |

---

## 5. Beispiel Dashboard-Text

```text
This race has an equivalent effort of 116 km.
With 833 m+ per kilometer, the course is classified as Extreme Mountain.
Your flat-equivalent pace is 6:12/km-effort.
```

---

## 6. Beste visuelle Idee

Für `difficulty_score`:

```html
<div class="score-ring">
  <span>87</span>
  <small>Difficulty Score</small>
</div>
```

Oder einfacher:

```html
<div class="progress-bar">
  <div class="progress-fill" style="width: 87%"></div>
</div>
```

---

## 7. Mein Vorschlag für deine Performance Metrics Page

Die Seite sollte 4 Bereiche haben:

```text
1. Input Calculator
2. Key Metrics Overview
3. Race Profile Classification
4. Performance Interpretation
```

Das wirkt direkt wie ein echtes SaaS-Feature und nicht nur wie ein API-Test.
