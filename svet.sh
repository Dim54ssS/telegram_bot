#!/bin/bash
ERR=`ping 178.150.234.63 -c 2 2>&1 > /dev/null` && echo "Є,давай вали додому" || { echo "Нема, можеш погулять на свіжому повітрі" && exit;}
