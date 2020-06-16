This is a script to capture input at the (Linux) command line. The output of the script can be mapped to a schema, like BioCompute, for automatic BCO creation from command line pipes. The tool is turned on when you're ready to capture a pipeline, and exited with 'Ctrl+C' when finished (see instructions below). Certain characters (like backspace) are not captured, but are used to modify the log so as to accurately capture the input. All captured input is then passed to the shell for execution.


### Basic running instructions

~~Allow bco_entry.py to be executable if it isn't: `chmod +x bco_entry.py`~~
~~Execute the program: `./bco_entry.py`~~
- Install requirements (virtual environment recomended, e.g. `mkvirtualenv bco`) using `pip`, e.g. `pip3 install -r requirements.txt`
- Execute using your favorite python3 invokation: `./bco_entry.py`, `python3 bco_entry.py`, etc.
- Type in sensible commands and see the output: `ls -lah`, `python3 -V`, probably others
- Type in nonsense commands and error handling *should* be adequate
- BCO entry runs in an infinte loop, use `Ctrl+C` to escape and shutdown

### Acknowledgements / source material
This code is heavily sourced from parts of the ActivityWatch project (https://github.com/ActivityWatch/activitywatch), specifically the 'afk-watcher' client, licensed under MPL-2.0 (https://github.com/ActivityWatch/activitywatch/blob/master/LICENSE.txt)

PyUserInput module is used under LGPL-3.0.


