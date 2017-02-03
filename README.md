# Traverse cli

A very simple command line tool for tree exploration. Designed to interact well with shell pipelines.
Works with both python2 and python3.

# Installing

```
pip install git+https://github.com/talwrii/traverse_cli#egg=traverse_cli
```

# Usage

```
# Equivalent of "find ." -- more wordy than desired because we need absolute(ish) paths
traverse_cli   'if [ -d "{node}" ]; then ls {node} | sed "s!^!{node}/!" ; fi ' .

# Reverse depends tree for apt
traverse_cli  "apt-cache rdepends {node} | tail -n +3 | tr -d '|' | tr -d ' ' " vlc --depth 2
```
