#! /bin/bash
fdisk /dev/sdb <<EOF
n
p
1
2048
496127
w
EOF
