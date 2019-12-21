#!/usr/bin/env python3

import sys
from rcj import Rcj
from argparse import ArgumentParser

# usage:
# 
# rcj_cli init <schema> # initialize the database with the given schema file:
# rcj_cli referee list # lists all referees
# rcj_cli referee add <username> <pass> # adds referee to database
# rcj_cli referee check <username> <password> # checks if referee has given password
#
#    - show: print path and content
# referee
#    - list: list all referees
#    - show <username> shows referee info

def main(argv):
	parser = ArgumentParser(prog='rcj_cli')
	subparsers = parser.add_subparsers(help='COMMAND', dest='command')
	# database init
	init = subparsers.add_parser('init')
	init.add_argument('schema')
	# commands to handle referees
	referee = subparsers.add_parser('referee')
	sub_referee = referee.add_subparsers(help='ACTION', dest='ref_action', required=True)
	referee_add = sub_referee.add_parser('add')
	referee_add.add_argument('username')
	referee_add.add_argument('password')
	referee_list = sub_referee.add_parser('list')
	referee_check = sub_referee.add_parser('check')
	referee_check.add_argument('username')
	referee_check.add_argument('password')
	args = parser.parse_args()
	print(args)

	rcj = Rcj('database.sqlite')
	if args.command == 'init':
		rcj.create_database(args.schema)
	elif args.command == 'referee':
		if args.ref_action == 'add':
			rcj.update_referee(args.username, args.password)
		elif args.ref_action == 'list':
			print(rcj.get_referees())
		elif args.ref_action == 'check':
			print(rcj.check_referee_password(args.username, args.password))
			
	
if __name__ == '__main__':
	main(sys.argv)
