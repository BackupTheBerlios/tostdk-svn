#==========================================================================
# tostdk :: tostlib :: command_queue.py
# Command queue class
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


import struct

import logging
import singleton

import result
import command

import driver


#==========================================================================
class CommandQueue ( singleton.Singleton ):
#==========================================================================

	s_instance = None

	#----------------------------------------------------------------------
	def __init__ ( self ):
	#----------------------------------------------------------------------

		self.m_running = None
		self.m_queue   = []

		self.m_input_buffer  = ''
		self.m_output_buffer = ''

	#----------------------------------------------------------------------
	def is_empty ( self ): return (not self.m_queue)
	#----------------------------------------------------------------------

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

		for l_command in self.m_queue:
			l_command.abort_cb()

		self.m_queue = []

	#----------------------------------------------------------------------
	def process ( self ):
	#----------------------------------------------------------------------

		if not self.m_running:

			if not self.m_queue:
				return True

			self.m_running = self.m_queue.pop(0)
			self.__encode()

			self.m_running.m_state = command.RUNNING
			self.m_running.running_cb()

		l_driver = driver.Driver.get_instance()

		if self.m_output_buffer:
			if not self.__send(l_driver):
				logging.error("Can't send data to driver")
				self.abort()
				return False

		else:
			l_result = self.__decode()

			if l_result != None:
				self.m_running.m_status = command.FINISHED
				self.m_running.m_result = l_result
				self.m_running.finished_cb()
				self.m_running = None

			else:
				if not self.__receive(l_driver):
					logging.error("Can't read data from driver")
					self.abort()
					return False

		return True

	#----------------------------------------------------------------------
	def __encode ( self ):
	#----------------------------------------------------------------------

		l_opcode = self.m_running.get_opcode()
		l_data   = self.m_running.get_data()

		self.m_output_buffer = struct.pack('>BH', l_opcode, len(l_data)) + l_data

	#----------------------------------------------------------------------
	def __decode ( self ):
	#----------------------------------------------------------------------

		if len(self.m_input_buffer) >= 3:
			l_opcode, l_length = struct.unpack('>BH', self.m_input_buffer[:3])

			if l_length and len(self.m_input_buffer) >= (l_length + 3):
				l_data = self.m_input_buffer[3:l_length+3]
				self.m_input_buffer = self.m_input_buffer[l_length+3:]

				return result.Result(l_opcode, l_data)

		return None

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

		return False


#==========================================================================
# End
#==========================================================================
