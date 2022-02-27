# Static resources build guide

The application is build using the QT framework. A lot of stuff is defined outside the code, as they need to be accessed
by external tools.

## Files

Currently, the project depends on those files:

- UI Files
  - `phypidaq/phypi.ui`
- Resources files
  - `phypidaq/resources.qrc`

## Apply modifications

If there were modifications those files listed above, we need to compile those changes back to Python code. To do this,
you simply need to execute the following commands in the shell

This is the command for the ui files:

```shell
pyuic5 phypi.ui -o phypiUi.py
```

This is the command for the resources files:

```shell
pyrcc5 resources.qrc -o resources.py
```
