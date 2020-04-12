# Description: Scheduled script to run run_and_upload.sh
# Author: Chris Hwang

iter=0
while (( $iter < 1 ))
do
  bash ./scripts/run_and_upload.sh
  # sleep for 6 hrs
  sleep 21600
done