# <p align = 'center'> Predicting the Outcomes of NBA Games </p>
## <p align = 'center'> Team Members: Zichang Ye, Kuan-Lin Liu, Duo Jiang, Guojin Tang </p>

## Introduction
The sports of basketball fascinates us for its unpredictability, but whenever we look retrospectively, the result almost always makes sense. We can explain a victory by many factors: better star players, better team chemistry, better coaching, better momentum, and the list goes on and on. With the belief that the result of a basketball game is not entirely random, we landed this project to predict the result of the game based on the previous records of the participating opponents.

This prediction task can be thought as a classification problem. The target variable is whether the home team wins this game, and the features are previous information about the competing two teams, such as their up-to-date ability, their previous records of competing, as well as their level of fatigue and momentum. The detailed descriptions of the features can be found in the section of data preparation.

## Business Understanding
Two businesses will be benefited: the betting business and the merchandising and licensing business. 
- Betting: the company sets the odds based on their belief and calculation about the odds of the occurrence of certain events. Conversely, a bettor can tailor his/her betting strategy to beat the betting company using such a model's prediction, as illustrated by a similar study in tennis (Sikpo, 2016). 
- Merchandising and Licensing: Since the sales of the licensed products are likely to be correlated with the performance of the team, merchandising and licensing businesses need an estimation of the team's success to decide the resources and budget required for production. A reliable prediction can help them control their budgets. 

## Data Understanding
### Data Source
There was no comprehensive dataset that includes all the information we need for this project, so we made the best efforts to scrape data from the internet and then merged these datasets to create our dataset. The three data sources are basketball-reference, stats.nba.com and ESPN's NBA website. 

From basketball-reference, we got the schedule for all games from 2008 to 2019, and we call it Total-schedule. Total-schedule, including includes games from regular seasons and playoff seasons,  contains 15625 games in total. The features in Total-schedule are the two opponents(home team and away team), game date, and final points for the two teams.  Also, from basketball-reference, a player-level dataset, player-details, was obtained. Player-details  tab has 34 statistics for each player in each game, such as minutes played, points, and rebounds.

We believe team chemistry is a key factor in determining the result of a game, and lineup-level statistics may capture it. Therefore, we scraped stats.nba.com to get lineup-level statistics. For each game and each lineup, 15 different statistics were collected. These statistics include basic features like minutes played as well as more advanced features like PIE(which is a weighted sum of some other basic features).  

The last data source is ESPN's NBA website. From ESPN, we obtained a statistics called Real Plus and Minus(RPM) which can also be divided into Offensive Real Plus and Minus(ORPM) and Defensive Real Plus and Minus(DRPM). As a player-level statistics, ORPM and DPRM can quantify a player's contribution on the offensive end and defensive end, respectively. 

Note that the home team wins about  59.1\% of all games in this dataset, which serves a proper baseline for model evaluation.

## Data Preparation
## Modeling and Evaluation
## Results
