#!/usr/bin/python
#filename call.py

import change
import change2

h=change.handle()
today=h.change()

b=change2.back_up()
b.backup(today)
