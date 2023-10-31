#!/bin/bash
# Copyright (c) 2021-present Tommy Nguyen
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)

set -eu

project_root=$(cd -P "$(dirname $0)" && pwd)

export POETRY_HOME=$project_root/.poetry

function poetry {
  $POETRY_HOME/bin/poetry $@
}

if [[ ! -d "$POETRY_HOME/venv" ]]; then
  python3 $POETRY_HOME/install-poetry.py --version 1.6.1
fi

case ${1-} in
  "check")
    poetry run pylint dodo
    poetry run mypy --strict dodo
    ;;
  "ci")
    ./py format
    ./py check
    ./py test
    ;;
  "format")
    poetry run black dodo
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
    sudo pip3 install inky[rpi] ${dependencies[*]}
    sudo echo "* * * * * python3 $project_root/dodo -c $project_root/config.json" >> /etc/crontab
    sudo systemctl enable cron
    ;;
  "run")
    shift
    poetry run python dodo $*
    ;;
  "test")
    shift
    poetry run pytest $*
    ;;
  "update")
    poetry update
    ;;
  *)
    echo "Python virtual environment is set up!"
    echo "Type '$0 help' to get started."
    ;;
esac
