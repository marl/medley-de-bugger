#!/bin/sh

# See setup.py for instructions

# delete the temporary directories (from earlier builds that may have failed)
rm -rf build
rm -rf dist

# create the app bundle
python setup.py py2app

# create the .dmg disk file
rm -rf dist_mac
mkdir dist_mac
hdiutil create -fs HFS+ -volname "NewMultitrack" -srcfolder dist dist_mac/NewMultitrack.dmg

# delete the temporary directories
rm -rf build
rm -rf dist