# Problem
There are many races with different editions (ex. GGUT 2017, GGUT 2019) in the data which gets split up into training and testing data. This might cause data leakage because those races are practicly the same races, but held in different years. If the model gets trained and had a look at GGUT 2017, but GGUT 2019 is in the testing data, then the model has already seen this data and its performance will artifically improve.

# Hypothesis


# Analysis

# Solution
The solution is to group all the different editions of a race, but are the same race, together so the model does not get trained and tested on the same data. So instead of using a normal train and test split, you should use a group based train, test split.
Example:
Normal train, test split:
| Race_Title     |
| -              |
| GGUT 100 2022  |
| GGUT 100 2023  |
| GGUT 100 2024  |
| OCC 2023       |
| OCC 2021       |

The normal train and test split could contain the same race but different years in the training or testing data.

Group based train and test split:
| Race_Title     | Group    |
| -              | -        |
| GGUT 100 2022  | GGUT 100 |
| GGUT 100 2023  | GGUT 100 |
| GGUT 100 2024  | GGUT 100 |
| OCC 2023       | OCC      |
| OCC 2021       | OCC      |

The group based train and test split does not contain the same race in different splits, which means that for example GGUT 100 only will be used in the training, but not the testing, as this would artifically improve the models performance, because it would have been tested on data that it has been trained on.
# Code

# Learning
A model is not allowed to get trained and tested on the same data, as this will artifically improve the models performance.

# Impact
A model trained and tested on the same data will cause issues, as it seems that the model is performing good, even tho it will performe bad in production. The solution ensures that the evaluation of the model will be correct and thus displays useful information.