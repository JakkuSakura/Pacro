#!/bin/sh
for package in pacro ship
do
  pip_site=$(env python3 -m pip --version | awk '{print $4}')
  site_packages="$(dirname "$pip_site")"
  BASEDIR=$(realpath $(dirname "$0"))
  unlink "$site_packages/$package" 2> /dev/null
  echo Linking from "$BASEDIR/$package" to "$site_packages/$package"
  ln -s "$BASEDIR/$package" "$site_packages/$package"
done
