#No poetry :()

# About
This reports the time spent per visitor per SL and page

## drop columns
["smartlink_name"] => drop, nothing functional in it

## Inconsistencies

### Durations
Some inconsistencies with durations => 

649d47768309e30012afd488	6	267351-702739	49695	5.0

649d47768309e30012afd488	6	267351-702739	49695	5.0

Like 2 days ?


## About ratings
Between 0 and 5 rating is just a clamped ratio (per page)= nb_sec/6 (so above 30s =>5) 


### Global rating per SL ?
=> Sum of time per page capped at 30 min ?
=> 

# About install, start

## Streamlit link
<https://grfrecommendations-skrkcd5tqmykmjawehmyr6.streamlit.app/>

## Locally
python3.9 venv -m venv

pip install 'scikit-surprise @ git+https://github.com/mihaiblidaru/Surprise/tree/pep517_compliant_package'
streamlit run app.py


## example data
https://nemato-data.fr/public/output.csv
https://nemato-data.fr/public/small.csv