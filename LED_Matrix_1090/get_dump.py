#!/usr/bin/env python
# encoding: utf-8

import socket
import datetime
import sqlite3
import argparse
import time

#defaults
HOST = "192.168.1.1"
PORT = 8080
DB = "adsb_messages.db"
BUFFER_SIZE = 100
BATCH_SIZE = 1
CONNECT_ATTEMPT_LIMIT = 10
CONNECT_ATTEMPT_DELAY = 5.0


def getdump():

	#set up command line options
	"""
	parser = argparse.ArgumentParser(description="A program to process dump1090 messages then insert them into a database")
	parser.add_argument("-l", "--location", type=str, default=HOST, help="This is the network location of your dump1090 broadcast. Defaults to %s" % (HOST,))
	parser.add_argument("-p", "--port", type=int, default=PORT, help="The port broadcasting in SBS-1 BaseStation format. Defaults to %s" % (PORT,))
	parser.add_argument("-d", "--database", type=str, default=DB, help="The location of a database file to use or create. Defaults to %s" % (DB,))
	parser.add_argument("--buffer-size", type=int, default=BUFFER_SIZE, help="An integer of the number of bytes to read at a time from the stream. Defaults to %s" % (BUFFER_SIZE,))
	parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="An integer of the number of rows to write to the database at a time. If you turn off WAL mode, a lower number makes it more likely that your database will be locked when you try to query it. Defaults to %s" % (BATCH_SIZE,))
	parser.add_argument("--connect-attempt-limit", type=int, default=CONNECT_ATTEMPT_LIMIT, help="An integer of the number of times to try (and fail) to connect to the dump1090 broadcast before qutting. Defaults to %s" % (CONNECT_ATTEMPT_LIMIT,))
	parser.add_argument("--connect-attempt-delay", type=float, default=CONNECT_ATTEMPT_DELAY, help="The number of seconds to wait after a failed connection attempt before trying again. Defaults to %s" % (CONNECT_ATTEMPT_DELAY,))

	# parse command line options
	# print args.accumulate(args.in)
	args = parser.parse_args()
	"""

	count_since_commit = 0
	count_total = 0
	count_failed_connection_attempts = 1

	start_time = datetime.datetime.utcnow()

	# open a socket connection
	while count_failed_connection_attempts < args.connect_attempt_limit:
		try:
			s = connect_to_socket(args.location, args.port)
			count_failed_connection_attempts = 1
			print "Connected to dump1090 broadcast"
			break
		except socket.error:
			count_failed_connection_attempts += 1
			print "Cannot connect to dump1090 broadcast. Making attempt %s." % (count_failed_connection_attempts)
			time.sleep(args.connect_attempt_delay)
	else:
		quit()

	data_str = ""

	try:
		#loop until an exception
		while True:
			try:
				message = ""
				message = s.recv(args.buffer_size)
				data_str += message.strip("\n")
			except socket.error:
				# this happens if there is no connection and is delt with below
				pass

			if len(message) == 0:
				print ts, "No broadcast received. Attempting to reconnect"
				time.sleep(args.connect_attempt_delay)
				s.close()

				while count_failed_connection_attempts < args.connect_attempt_limit:
					try:
						s = connect_to_socket(args.location, args.port)
						count_failed_connection_attempts = 1
						print "Reconnected!"
						break
					except socket.error:
						count_failed_connection_attempts += 1
						print "The attempt failed. Making attempt %s." % (count_failed_connection_attempts)
						time.sleep(args.connect_attempt_delay)
				else:
					quit()

				continue

			# it is possible that more than one line has been received
			# so split it then loop through the parts and validate

			data = data_str.split("\n")

			for d in data:
				line = d.split(",")

				#if the line has 22 items, it's valid
				if len(line) == 22:
					print(line)
						count_total += 1
						count_since_commit += 1



					# since everything was valid we reset the stream message
					data_str = ""
				else:
					# the stream message is too short, prepend to the next stream message
					data_str = d
					continue

	except KeyboardInterrupt:
		print "\n%s Closing connection" % (ts,)
		s.close()

		conn.commit()
		conn.close()
		print ts, "%s squitters added to your database" % (count_total,)

	except sqlite3.ProgrammingError:
		print "Error with ", line
		quit()

def connect_to_socket(loc,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((loc, port))
	return s

