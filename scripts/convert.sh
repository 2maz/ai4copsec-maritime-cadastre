#!/bin/bash

# This script will convert the BaseDateTime column in all downloaded *.zip files
# see convert.sh to a proper timestamp column 'timestamp' to allow searching and processing

SCRIPT_DIR=$(realpath -L $(dirname $0))
DATA_DIR=$(realpath -L $SCRIPT_DIR/..)

for d in 2016 2017 2018 2019 2020 2021 2022 2023 2024; do
    cd $DATA_DIR/$d/

    echo "CURRENT DIR: $PWD"
    for i in $(ls *.zip); do
        FILENAME=$(basename -s .zip $i)
        echo "    damast process"
        echo "        --pipeline $SCRIPT_DIR/pipelines/str-to-timestamp.damast.ppl"
        echo "        --input-data $i"
        echo "        --output-file $DATA_DIR/$d/$i"

        damast process --pipeline $SCRIPT_DIR/pipelines/str-to-timestamp.damast.ppl --input-data $i --output-file $DATA_DIR/$d/$i 2>&1 > $DATA_DIR/logs/$d-convert.log
    done
done
