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
import driver
import packet
import command
import result


#==========================================================================
class Queue ( singleton.Singleton ):
#==========================================================================

	s_instance = None

	#----------------------------------------------------------------------
	STATE_IDLE      = 0
	STATE_SENDING   = 1
	STATE_RECEIVING = 2
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	def __init__ ( self ):
	#----------------------------------------------------------------------

		singleton.Singleton.__init__(self)

		self.m_queue   = []

		self.m_state   = self.STATE_IDLE
		self.m_running = None
		self.m_time    = 0.0
		self.m_timeout = 0.0

		self.m_buffer  = ''

	#----------------------------------------------------------------------
	def __del__ ( self ):
	#----------------------------------------------------------------------

		driver.Driver.del_instance()

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
			l_command.m_state = command.ABORTED
			l_command.aborted_cb()

		self.m_buffer = ''
		self.m_state  = self.STATE_IDLE

	#----------------------------------------------------------------------
	def process ( self ):
	#----------------------------------------------------------------------

		if self.m_state == self.STATE_IDLE:

			if not self.__state_idle():
				return False

		elif self.m_state == self.STATE_SENDING:

			if not self.__state_sending():
				return False

		elif self.m_state == self.STATE_RECEIVING:

			if not self.__state_receiving():
				return False

		if not self.__check_timeout():
			return False

		return True

	#----------------------------------------------------------------------
	def __state_idle ( self ):
	#----------------------------------------------------------------------

		if not self.m_queue:
			return False

		self.m_state   = self.STATE_SENDING
		self.m_running = self.m_queue.pop(0)

		self.m_running.m_state = command.RUNNING
		self.m_running.running_cb()

		self.m_time    = time.time()
		self.m_timeout = self.m_running.get_timeout()
		self.m_buffer  = self.m_running.pack()

		return True

	#----------------------------------------------------------------------
	def __state_sending ( self ):
	#----------------------------------------------------------------------

		if not self.__send():
			logging.error("Can't send data to driver")
			self.abort()
			return False

		if not self.m_buffer:
			self.m_state = self.STATE_RECEIVING

		return True

	#----------------------------------------------------------------------
	def __state_receiving ( self ):
	#----------------------------------------------------------------------

		if not self.__receive():
			logging.error("Can't receive data from driver")
			self.abort()
			return False

		l_check = packet.Packet.check(self.m_buffer)

		if l_check == packet.Packet.VALID:

			l_running = self.m_running
			l_result  = result.Result.unpack(self.m_buffer)

			self.m_state   = self.STATE_IDLE
			self.m_running = None
			self.m_buffer  = ''

			l_running.m_status = command.FINISHED
			l_running.m_result = l_result

			if not l_running.finished_cb():
				self.abort()
				return False

		elif l_check == packet.Packet.TAG_ERROR:
			logging.error("Invalid packet tag")
			self.abort()
			return False

		elif l_check == packet.Packet.CHECKSUM_ERROR:
			logging.error("Invalid packet checksum")
			self.abort()
			return False

		elif l_check == packet.Packet.CRC8_ERROR:
			logging.error("Invalid packet crc")
			self.abort()
			return False

		return True

	#----------------------------------------------------------------------
	def __check_timeout ( self ):
	#----------------------------------------------------------------------

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
	def __send ( self ):
	#----------------------------------------------------------------------

		l_driver = driver.Driver.get_instance()

		if not l_driver:
			return False

		if self.m_buffer:
			l_length = l_driver.write(self.m_buffer)
			self.m_buffer = self.m_buffer[l_length:]

		return True

	#----------------------------------------------------------------------
	def __receive ( self ):
	#----------------------------------------------------------------------

		l_driver = driver.Driver.get_instance()

		if not l_driver:
			return False

		self.m_buffer += l_driver.read()

		return True


#==========================================================================
# End
#==========================================================================
