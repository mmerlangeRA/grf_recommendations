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

# PDF analysis
This is a test to check what an article is and how we could detect it and maybe enhance the recommendations
In the local pdf (real one), here are some issues :
* 

# Installation

## Streamlit link
<https://grfrecommendations-skrkcd5tqmykmjawehmyr6.streamlit.app/>

## Locally
python3.9 -m venv venv
source venv/bin/activate
pip install requir
streamlit run app.py

openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
uvicorn server:app --reload

## example data
https://nemato-data.fr/public/output.csv
https://nemato-data.fr/public/small.csv