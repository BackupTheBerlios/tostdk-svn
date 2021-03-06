#==========================================================================
# tostdk :: tostlib :: command.py
# Command packet class
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


import packet
import opcodes
import data


#==========================================================================
PENDING  = 0
RUNNING  = 1
ABORTED  = 2
TIMEOUT  = 3
FINISHED = 4
#==========================================================================


#==========================================================================
class Command ( packet.Packet ):
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_opcode, p_data ):
	#----------------------------------------------------------------------

		packet.Packet.__init__(self, p_opcode, p_data)

		self.m_status = PENDING
		self.m_result = None

		self.m_timeout = 0.0
		self.m_guid    = None

		self.m_running_cb  = None
		self.m_aborted_cb  = None
		self.m_timeout_cb  = None
		self.m_finished_cb = None

	#----------------------------------------------------------------------
	def cleanup ( self ):
	#----------------------------------------------------------------------

		self.m_status = PENDING
		self.m_result = None

	#----------------------------------------------------------------------
	@classmethod
	def create ( cls, p_opcode, p_args, p_timeout = 0.0, p_guid = None ):
	#----------------------------------------------------------------------

		l_format = opcodes.command_format(p_opcode)

		if l_format == None:
			return None

		l_data = data.pack(l_format, p_args)

		if l_data == None:
			return None

		l_command = cls(p_opcode, l_data)

		l_command.set_timeout(p_timeout)
		l_command.set_guid(p_guid)

		return l_command

	#----------------------------------------------------------------------
	def is_pending  ( self ): return (self.m_status == PENDING)
	def is_running  ( self ): return (self.m_status == RUNNING)
	def is_finished ( self ): return (self.m_status == FINISHED)
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	def has_result ( self ): return (self.m_result != None)
	def get_result ( self ): return self.m_result
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	def has_timeout ( self ): return (self.m_timeout > 0.0)
	def get_timeout ( self ): return self.m_timeout
	def set_timout  ( self, p_timeout ): self.m_timeout = p_timeout
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	def has_guid ( self ): return bool(self.m_guid)
	def get_guid ( self ): return self.m_guid
	def set_guid ( self, p_guid ): self.m_guid = p_guid
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	def get_name ( self ):
	#----------------------------------------------------------------------

		return opcodes.command_name(self.get_opcode())

	#----------------------------------------------------------------------
	def get_format ( self ):
	#----------------------------------------------------------------------

		return opcodes.command_format(self.get_opcode())

	#----------------------------------------------------------------------
	def get_args ( self ):
	#----------------------------------------------------------------------

		l_format = self.get_format()

		if l_format == None:
			return None

		return data.unpack(l_format, self.get_data())

	#----------------------------------------------------------------------
	def get_args_readable ( self ):
	#----------------------------------------------------------------------

		l_format = self.get_format()

		if l_format == None:
			return None

		return data.unpack_readable(l_format, self.get_data())

	#----------------------------------------------------------------------
	def set_callbacks ( self, p_callbacks ):
	#----------------------------------------------------------------------

		if p_callbacks.has_key(RUNNING):
			self.m_running_cb  = p_callbacks[RUNNING]

		if p_callbacks.has_key(ABORTED):
			self.m_aborted_cb  = p_callbacks[ABORTED]

		if p_callbacks.has_key(TIMEOUT):
			self.m_timeout_cb  = p_callbacks[TIMEOUT]

		if p_callbacks.has_key(FINISHED):
			self.m_finished_cb = p_callbacks[FINISHED]

	#----------------------------------------------------------------------
	def running_cb  ( self ):
	#----------------------------------------------------------------------

		if self.m_running_cb:
			self.m_running_cb(self)

	#----------------------------------------------------------------------
	def aborted_cb  ( self ):
	#----------------------------------------------------------------------

		if self.m_aborted_cb:
			self.m_aborted_cb(self)

	#----------------------------------------------------------------------
	def timeout_cb  ( self ):
	#----------------------------------------------------------------------

		if self.m_timeout_cb:
			return self.m_timeout_cb(self)
		return False

	#----------------------------------------------------------------------
	def finished_cb ( self ):
	#----------------------------------------------------------------------

		if self.m_finished_cb:
			return self.m_finisehd_cb(self)
		return True


#==========================================================================
# End
#==========================================================================
