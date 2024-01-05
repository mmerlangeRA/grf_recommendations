# Objectives
From reports the time spent per visitor per SL, article and page, let's recommend other articles to users

## Vocabulary
* SL and page => clear
* Article : ?


# Quick analysis & Processing 

## Inconsistencies

### Durations

Some inconsistencies with durations => like 2 days

## drop columns
["smartlink_name"] => drop, nothing functional in it

## About ratings
Between 0 and 5 rating is just a clamped ratio (per page)= nb_sec/6 (so above 30s =>5) 

### Global rating per SL ?
=> Sum of time per page capped at 30 min ?
=> 

# About install, start

## Streamlit link
<https://grfrecommendations-skrkcd5tqmykmjawehmyr6.streamlit.app/>

## Locally
python3.9 -m venv venv
pip install
streamlit run app.py

## example data
https://nemato-data.fr/public/output.csv
https://nemato-data.fr/public/small.csv