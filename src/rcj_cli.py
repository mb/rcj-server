#!/usr/bin/env python3

import sys
from rcj import Rcj

# usage:
# rcj_cli database
#    - init: initialize database
#    - show: print path and content
# referee
#    - list: list all referees
#    - show <username> shows referee info

def main(argv):
	if len(argv) == 0:
		print('usage: rcj_cli referee list')
	
	rcj = Rcj('database.sqlite')
	if argv[1] == 'init':
		rcj.create_database()
		
	


if __name__ == '__main__':
	main(sys.argv)
