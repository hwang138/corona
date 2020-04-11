iter=0
while (( $iter < 1 ))
do
  bash ./scripts/upload.sh
  echo "upload complete"
  # sleep for 12 hrs
  sleep 43200
done