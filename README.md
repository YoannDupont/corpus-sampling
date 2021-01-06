# corpus-sampling

Utility script to sample corpora of some sources.

# Installation

## Creating a virtual environment

To install this tool, I would recommend using a virtual environment.

If you do not have one, you can create an environment using :

`python3.7 -m venv /path/to/venv`

You can then switch to this environment :

`source /path/to/venv/bin/activate`

## Installing the sampler

You can then install the sampler by running :

`python ./setup.py install`

## Using the sampler

You now have access to the sampling tool by using the command :

`sample-corpus`

You can access the help with :

`sample-corpus -h`

You can sample 1000 tokens from some text file and put it in `/path/to/sampledir/` with :

`sample-corpus /path/to/file.txt -s 1000 -o /path/to/sampledir/`
