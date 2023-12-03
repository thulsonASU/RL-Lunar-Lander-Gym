### Installing Dependancies

Proven to work on Ubuntu 22.04 LTS. Create a .venv for installing python libraries without bricking current python install. This might not work with Windows machines.
```sh
# I used the built in scripts with visual studio to create my venv (You can use whatever suits your needs)
python -m virtualenv venv
# source is used for bash
source .venv/bin/activate
# will go through the requirements.txt and install (cd to src to run)
pip install -r requirements.txt
```

### Source

[Main Source](https://www.sliceofexperiments.com/p/an-actually-runnable-march-2023-tutorial)