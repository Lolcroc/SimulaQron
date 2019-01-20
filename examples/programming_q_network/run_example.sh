#!/usr/bin/env sh
TEST_PIDS=$(ps aux | grep python | grep -E "Test" | awk {'print $2'})
if [ "$TEST_PIDS" != "" ]
then
        kill -9 $TEST_PIDS
fi

while getopts ":n:E" opt; do
  case $opt in
    n)
      N=$OPTARG
      if (("$N" > "256")); then
        echo "WARNING: $N bits too large; set to 256"
        N="256"
      fi
      ;;
    E)
      EVE="y"
      ;;
    \?)
      echo "Unknown argument: -$OPTARG"
      exit 1
      ;;
    :)
      echo "Specify #bits after -$OPTARG"
      exit 1
      ;;
  esac
done

N=${N:-"16"} # If not set, use 16 bits
EVE=${EVE:-"n"} # If not set, don't eavesdrop

echo "Running w/ $N input bits, Eve active: [$EVE]"

python aliceTest.py "$N" &
python bobTest.py "$N" &
python eveTest.py "$N" "$EVE" &
