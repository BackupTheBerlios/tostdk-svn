#==========================================================================
# tostdk :: tostlib :: queue.py
# Command queue manager
#--------------------------------------------------------------------------
# Copyright 2009 Jean-Baptiste Berlioz
#--------------------------------------------------------------------------
# This file is part of Tostdk.
#
# Tostdk is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tostdk is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tostdk.  If not, see <http://www.gnu.org/licenses/>.
#==========================================================================


import time
import struct

import logging
import singleton
import command
import result
import driver


#==========================================================================
class Queue ( singleton.Singleton ):
#==========================================================================

	s_instance = None

	#----------------------------------------------------------------------
	def __init__ ( self ):
	#----------------------------------------------------------------------

		self.m_queue   = []

		self.m_running = None
		self.m_time    = 0.0
		self.m_timeout = 0.0

		self.m_input_buffer  = ''
		self.m_output_buffer = ''

	#----------------------------------------------------------------------
	def is_empty ( self ): return (not self.m_queue)
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	def insert ( self, p_command ):
	#----------------------------------------------------------------------

		if not p_command.is_pending():
			logging.error("Can't queue running or finished commands")
			return False

		self.m_queue.insert(0, p_command)
		return True

	#----------------------------------------------------------------------
	def append ( self, p_command ):
	#----------------------------------------------------------------------

		if not p_command.is_pending():
			logging.error("Can't queue running or finished commands")
			return False

		self.m_queue.append(p_command)
		return True

	#----------------------------------------------------------------------
	def abort ( self ):
	#----------------------------------------------------------------------

		logging.message("Aborting command queue")

		l_running = self.m_running
		l_queue   = self.m_queue[:]

		self.m_running = None
		self.m_queue   = []

		if l_running:
			l_running.m_state = command.ABORTED
			l_running.aborted_cb()

		for l_command in l_queue:
			l_command.aborted_cb()

		self.m_input_buffer  = ''
		self.m_output_buffer = ''

	#----------------------------------------------------------------------
	def process ( self ):
	#----------------------------------------------------------------------

		if not self.m_running:

			if not self.m_queue:
				return False

			self.m_running = self.m_queue.pop(0)

			self.m_running.m_state = command.RUNNING
			self.m_running.running_cb()

			self.m_time = time.time()
			self.m_timeout = self.m_running.get_timeout()
			self.m_output_buffer = self.m_running.pack()

		l_driver = driver.Driver.get_instance()

		if self.m_output_buffer:
			if not self.__send(l_driver):
				logging.error("Can't send data to driver")
				self.abort()
				return False

		else:
			l_result = result.Result.unpack(self.m_input_buffer)

			if l_result != None:
				self.m_input_buffer = ''

				l_running = self.m_running
				self.m_running = None

				l_running.m_status = command.FINISHED
				l_running.m_result = l_result
				if not l_running.finished_cb():
					self.abort()
					return False

			else:
				if not self.__receive(l_driver):
					logging.error("Can't receive data from driver")
					self.abort()
					return False

		if self.m_running and self.m_timeout > 0.0:
			if (time.time() - self.m_time) > self.m_timeout:
				logging.error("Timeout!")

				l_running = self.m_running
				self.m_running = None

				l_running.m_status = command.TIMEOUT
				if not l_running.timeout_cb():
					self.abort()
					return False

		return True

	#----------------------------------------------------------------------
	def __send ( self, p_driver ):
	#----------------------------------------------------------------------

		while self.m_output_buffer and p_driver.can_write():
			l_byte = self.m_output_buffer[0]

			if not p_driver.write_byte(l_byte):
				return False

			self.m_output_buffer = self.m_output_buffer[1:]

		return True

	#----------------------------------------------------------------------
	def __receive ( self, p_driver ):
	#----------------------------------------------------------------------

		while p_driver.can_read():
			l_byte = p_driver.read_byte()

			if l_byte == None:
				return False

			self.m_input_buffer += l_byte

		return True


#==========================================================================
# End
#==========================================================================