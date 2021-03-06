# Release guide

This is a rather simple guide, describing how to do releases.

## Versioning

The project is following the schema `va.b.c`, which can be evaluated to

- `a` is the major version of the package. This will only get changed, if there is either a large code rewrite or a
 really important new feature is introduced.
- `b` describes minor changes of software package.
- `c` is for revisions, which describes small important changes, like a small bug fix or fixes of typos.

All are natural numbers starting from 0.

## Preparing a release

Follow this steps to create a release

- Write down all changes to the code into the [Release Notes](../ReleaseNotes.md), following the displayed format. Keep
  only the sections, where you have entries. More information about the file structure can be found
  [here](https://keepachangelog.com/en/1.0.0/).

  ```markdown
  ## [1.0.0] - 2022-01-30
  
  ### Added
  
  - A simple list of changes
  - Another one
  
  ### Changed
  
  - ..
  
  ### Deprecated
  
  - ...
  
  ### Removed
  
  - ...
  
  ### Fixed
  
  - ...
  
  ### Security
  
  - ...
  
  ```

- Ensure, that you have a date for the release and also the correct version number.
- Ensure, that the code, you want to release is working properly and mets the check of the Python Code linter.
- Update the `phypidaq/_version_info.py` with the matching version.
- Inform all project maintainers of the release.
- Do the release, by merging all the code from your development branch onto the `main` branch.
- Do a release on the GitHub page, by manually starting the *Create Release* GitHub Action.
