# Description: Script to run corona_19_visualization.ipynb and upload back to git
# Author: Chris Hwang

# use nbconvert to execute the notebook
jupyter nbconvert --to notebook --execute  ./corona_19_visualization.ipynb

# override the original notebook file
mv ./corona_19_visualization.nbconvert.ipynb ./corona_19_visualization.ipynb

# push up to git
git add ./corona_19_visualization.ipynb
git commit -am 're-run of notebook'
git push