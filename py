#!/bin/bash
# Copyright (c) 2021-present Tommy Nguyen
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)

set -eu

project_root=$(cd -P "$(dirname $0)" && pwd)
virtual_env="$project_root/.venv"

if [[ $(uname) == MINGW64_NT-* ]]; then
  venv_activate="$virtual_env/Scripts/activate"
else
  venv_activate="$virtual_env/bin/activate"
fi

if [[ ! -f "$venv_activate" ]]; then
  python3 -m venv "$virtual_env"
  source "$venv_activate"
  pip install --quiet --requirement "$project_root/requirements.txt"
else
  source "$venv_activate"
fi

case ${1-} in
  "check")
    pylint dodo
    mypy --strict dodo
    ;;
  "ci")
    ./py format
    ./py check
    ./py test
    ;;
  "format")
    black dodo
    ;;
  "help")
    echo "usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  check      Run linters and type checking"
    echo "  ci         Simulate a full CI loop"
    echo "  format     Format all Python files"
    echo "  help       Show this help message and exit"
    echo "  install    Install Dodo Boy on this device"
    echo "  run        Run Dodo Boy"
    echo "  test       Run tests"
    ;;
  "install")
    sudo apt update
    sudo apt install --assume-yes libatlas-base-dev libopenjp2-7 libtiff5 python3-pip
    sudo pip3 install Pillow arrow font-roboto inky[rpi,fonts]
    sudo echo "* * * * * python3 $project_root/dodo -c $project_root/config.json" >> /etc/crontab
    sudo systemctl enable cron
    ;;
  "run")
    shift
    python3 dodo $*
    ;;
  "test")
    shift
    pytest $*
    ;;
  "upgrade")
    pip list --outdated --local --format freeze  \
      | awk -F '==' '{print $1}'                 \
      | xargs pip install --upgrade
    pip freeze > "$project_root/requirements.txt"
    ;;
  *)
    echo "Python virtual environment is set up!"
    echo "Type '$0 help' to get started."
    ;;
esac
