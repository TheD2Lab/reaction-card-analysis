# Abstract

These scripts were created in order to analyze the qualitative feedback provided by participants of the Ontology Mapping Visualization study (as can be found in the OntoMapVis repository).
This feedback was primarily provided in the form of "reaction cards" - words chosen by participants to best describe their experience with a particular data visualization - 
which were internally recorded using .csv files, one per participant.

The various scripts fall into one of two different categories:
* The reaction card readers, which are used to aggregate participant feedback information into unified datasets (i.e., summative .csv files).
* The word cloud generator, which produces word cloud representations in order to better visualize and inform on the aggregated feedback.

A brief explanation of each script is as follows.

## Reaction Card Readers

### Reaction Card Compiler

This script runs through all participants' reaction card files and simply copy-pastes the information into a single .csv file;
this is meant mainly to provide a means of manually double-checking that the correct information is used for the scripts to follow.

### Reaction Card Counter

This script runs through all participants' reaction card files and essentially counts up every instance of every word selected,
producing a list of all such words and their frequencies across the entire participant reaction dataset. This particular file is also
meant to provide a means of manually double-checking the aggregated feedback information, as it provides information about 
which participants were counted and which were skipped over during the creation of the word-frequency list.

### Raw Card Counter

This script is nearly identical to the counter script above, but excludes the redundant double-checking information;
it generates *only* an overencompassing word-frequency list to be used for the word cloud generator script described below.

## Word Cloud Generator

This script produces two summative visualizations of the participant feedback data:
* An "all-heuristics" word cloud, which consists of the entire set of selected reaction card words, color-coded by which heuristic category each belongs to.
* A "per-heuristic" word cloud matrix, which consists of a set of word clouds separated by heuristic, whose words are color-coded by whether or not each has "negative" or "positive" connotation.