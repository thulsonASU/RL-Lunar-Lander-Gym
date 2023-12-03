### Installing Dependencies

Proven to work on Ubuntu 22.04 LTS. Create a .venv for installing Python libraries without bricking the current Python install. This might not work with Windows machines.
```sh
# We used the built-in scripts with Visual Studio to create Venv (You can use whatever suits your needs)
python -m virtualenv venv
# source is used for bash
source .venv/bin/activate
# will go through the requirements.txt and install (cd to src to run)
pip install -r requirements.txt
```

### Source

[Main Source](https://www.sliceofexperiments.com/p/an-actually-runnable-march-2023-tutorial)
