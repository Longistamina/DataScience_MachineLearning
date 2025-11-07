# How to disable the PipeableCallCheckWarning

Run this command in the terminal to open the ~/.bashrc file
```
nano ~/.bashrc
```

In side the ~/.bashrc file, find an empty space and add these following lines
```
# Disable PipeableCallCheckWarning of datar
export DATAR_VERB_AST_FALLBACK="piping"
```

Then, press ```Cltr + O``` to save the settings,
and then press ```Cltr + X``` to quit the nano screen.

After that, run this command to reload the ~/.bashrc file
```
source ~/.bashrc
```