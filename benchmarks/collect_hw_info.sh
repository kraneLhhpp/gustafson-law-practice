#!/bin/sh
# Task 24 helper - dump the facts needed for analysis/task24_hardware_audit.md   (Linux)
# usage: sh collect_hw_info.sh > ../analysis/hw_info.txt
run() { echo; echo "### $*"; "$@" 2>&1 || echo "(not available)"; }
run uname -a
run lscpu
run lscpu --caches
command -v numactl >/dev/null && run numactl --hardware
command -v lstopo-no-graphics >/dev/null && run lstopo-no-graphics --no-io
run free -h
echo; echo "### cpufreq governor / current frequencies"
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null
grep MHz /proc/cpuinfo 2>/dev/null | head -n 64
echo; echo "### SMT"; cat /sys/devices/system/cpu/smt/active 2>/dev/null
command -v dmidecode >/dev/null && echo && echo "### memory DIMMs (needs root)" && dmidecode -t memory 2>/dev/null | grep -E "Size|Speed|Locator" | head -n 40
