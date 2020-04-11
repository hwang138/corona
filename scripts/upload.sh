jupyter nbconvert --to notebook --execute  ./corona_19_visualization.ipynb
mv ./corona_19_visualization.nbconvert.ipynb ./corona_19_visualization.ipynb

git add ./corona_19_visualization.ipynb
git commit -am 're-run of notebook'
git push