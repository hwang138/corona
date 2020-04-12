# Covid-19 global case and death number tracking
Author: Chris Hwang<br>
GitHub: [link](https://github.com/hwang138/corona)

**Python version and dependencies**<br>
- version=3.6
- [dependencies](./environment.sh)

This report uses data from the European Centre for Disease Prevention and Control [(ecdc)](
https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases
)

To donwload the csv file yourself: [link](
https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide
)

**[Corona Class](./corona)**

**Notebook(s)**
- [corona_19_visualization](./corona_19_visualization.ipynb)
    - Pull the latest data from ECDC and plot some charts

**Script(s)**
- [run_and_upload.sh](./scripts/run_and_upload.sh)
    - bash script to run corona_19_visualization.ipynb
- [scheduled_run.sh](./scripts/scheduled_run.sh)
    - bash script to run on a 6 hr schedule

**Update log**    
- 2020-04-11
    - initial commit
- 2020-04-12
    - add global case and death numbers

**TODO(s)**
- pull data from CDC or some other source with finer spatil resolution that countries (especially the US)
- `current branch` build out basic projection model: use past 3 day case & death numbers to project 3 days out
- build out SIR model for proections by country
    - pull country/state population & population density
    - ...
