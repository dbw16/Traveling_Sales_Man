#!/bin/bash

QUICK=NO
OUTPUTDIR=NONE

# $# is number command line args
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -o|--output)
        OUTPUTDIR="$2"
        shift # past argument
        ;;
        # This uses the quicker method but does not produce a graph of route distance
        # vs iterations
        -q|--quick)
        QUICK=YES
        ;;
        -h|--help)
        echo 'Tool demonstrating the traveling salesman problem'
        echo
        echo 'Arguments are:'
        echo '        -q|--quick: This uses the quicker method but does not produce a graph of route distance vs iterations'
        echo '        -o|--output: Select a directory to output the .pngs too'
        exit 0
        ;;
        *)
        echo 'Unkown arg "'$key'". Use --help. Exiting'
        exit 1
        ;;
        esac
    shift
done

# Check if driectory exists and exit if it does not
if [[ $OUTPUTDIR != "NONE" ]]; then
    if [ ! -d $OUTPUTDIR ]; then
        echo $OUTPUTDIR is not a valid directory
        exit 1
    fi
fi

#Use quick version if -q command line arg is used
if [[ $QUICK == "YES" ]]; then
    python tsp_2.py
else
    python traveling_sales_man.py
fi

if [[ $OUTPUTDIR != "NONE" ]]; then
    mv *.png $OUTPUTDIR
fi