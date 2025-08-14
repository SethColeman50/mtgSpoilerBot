#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

mkdir -p $SCRIPT_DIR/testing_html

curl https://www.magicspoiler.com/mtg-set/avatar-the-last-airbender/ > $SCRIPT_DIR/testing_html/avatar-the-last-airbender.html
curl https://www.magicspoiler.com/mtg-set/spider-man/ > $SCRIPT_DIR/testing_html/spider-man.html
curl https://www.magicspoiler.com/mtg-set/lorwyn-eclipsed/ > $SCRIPT_DIR/testing_html/lorwyn-eclipsed.html
curl https://www.magicspoiler.com/mtg-spoilers/ > $SCRIPT_DIR/testing_html/setListPage.html
curl https://www.magicspoiler.com/mtg-spoiler/summon-bahamut/ > $SCRIPT_DIR/testing_html/cardPageWithDescription.html