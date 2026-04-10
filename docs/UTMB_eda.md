
Columns:
'City / Country', 'Date', 'Distance', 'Elevation Gain', 'N Results', 'Race Category', 'Race Title', 'Results', 'Age_20-34', 'Age_35-39', 'Age_40-44', 'Age_45-49', 'Age_50-54', 'Age_55-59', 'Age_60-64', 'Age_65-69', 'Age_70-74', 'Age_U18', 'Age_U20', 'Age_80+', 'Age_75-79', 'Country X', 'Sex_Men', 'Sex_Women'


# UTMB EDA MASTER CHECKLIST

| Phase | Goal | What to calculate / plot | Why (Insight) | Code / Method | DoD (Definition of Done) | Done |
|------|-----|--------------------------|-----------------|----------------|--------------------------| ----- |

| 1. Data Overview | Understand dataset | shape, dtypes, head(), describe() | Basic understanding | df.info(), df.describe() | I know size, data types, and rough distributions | |

| 2. Missing Values | Check data quality | Missing ratio per column (bar plot) | Identify critical features | df.isnull().mean() | I know which columns are problematic | |

| 3. Basic Distributions | Understand features | Histogram: distance, elevation, finish_time | Understand distributions | sns.histplot() | I know typical value ranges | |

| 4. Outlier Check | Detect extremes | Boxplot: finish_time, elevation | Identify outliers | sns.boxplot() | I know extreme races/times | |

| 5. Race Difficulty | Model difficulty | Effort Score = distance + elevation/100 | Standardized comparison | Feature Engineering | Effort score exists and makes sense | DONE |

| 6. Difficulty Distribution | Understand races | Histogram of effort score | Identify typical ultra zones | sns.histplot() | I see clusters of races | |

| 7. Distance vs Elevation | Understand race types | Scatter: distance vs elevation | Flat vs technical races | sns.scatterplot() | I see race structure | |

| 8. Performance Distribution | Understand times | Histogram: finish_time | Understand finishers | sns.histplot() | Median & spread are clear | |

| 9. Percentiles | Benchmarking | 10%, 25%, 50%, 75%, 90% | Elite vs average | np.percentile() | Benchmarks defined | |

| 10. Effort vs Time | Core insight | Scatter: effort vs finish_time | Physical performance model | sns.scatterplot() | Relationship is visible | |

| 11. Efficiency | Measure performance | efficiency = effort / time | Key KPI | Feature Engineering | Efficiency calculated | |

| 12. Efficiency Distribution | Compare performance | Histogram: efficiency | Good vs bad performers | sns.histplot() | Distribution understood | |

| 13. Correlation | Feature importance | Heatmap of numerical features | Identify key drivers | df.corr() + heatmap | I know important variables | |

| 14. Feature Relationships | Understand causes | Scatter: distance vs time, elevation vs time | Analyze influence | sns.scatterplot() | Influence is visible | |

| 15. Category Analysis | Compare groups | Boxplot: category vs finish_time | Identify differences | sns.boxplot() | Group differences are clear | |

| 16. Top Categories | Understand distribution | Countplot: category | Understand data structure | sns.countplot() | Most frequent categories known | |

| 17. Personal Benchmark | Position yourself | Your time vs distribution | Personal ranking | plt.axvline() | I know my percentile | |

| 18. Personal Efficiency | Evaluate performance | Your efficiency vs dataset | Track progress | Histogram + line | I know my efficiency | |

| 19. Position Plot | Overall picture | Scatter + your point | Over/underperformance | scatter + plt.scatter() | I see my position | |

| 20. Data Quality Final | ML readiness | Check duplicates, ranges | Clean dataset | df.duplicated() | Dataset is ML-ready | |