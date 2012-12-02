#!/bin/bash
gens=250;
datasets=("reddit" "sx" "synthetic");
root="/u/elie/condor_experiments/"

python generate_data.py synthetic_info

for dataset in "${datasets[@]}"
do
	python app.py $dataset"_info" $dataset"_complete.pkl" $dataset"_netinf.txt"
	./netinf -i:$dataset"_netinf.txt" -o:$dataset"_network.txt" 
	python pretty_graph.py netinf $dataset"_network.txt"
done