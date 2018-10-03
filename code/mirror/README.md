Prototype code for experimentation goes here

## Adding a widget

You can add any Widget that is supported by Qt. The best approach is to just copy one of the existing files in the widgets-folder (don't forget to rename the class-name),
and add a section in the config.ini file for interval and screen-position.

## Run in virtualenv

```bash
sudo pip install --user --upgrade virtualenv
virtualenv env
source env/bin/activate
pip install -r ../../system/requirements.txt
```

## TODO

* User profiles

## Current state

Try to update this picture regularly :)

![GUI](../doc/gui.png)
