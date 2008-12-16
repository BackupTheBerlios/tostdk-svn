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


#==========================================================================
PENDING  = 0
RUNNING  = 1
FINISHED = 2
ABORTED  = 3
TIMEOUT  = 4
#==========================================================================


#==========================================================================
class Command ( packet.Packet ):
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_opcode, p_data = '', p_timeout = 0.0, p_guid = None ):
	#----------------------------------------------------------------------

		packet.Packet.__init__(self, p_opcode, p_data)

		self.m_status  = PENDING
		self.m_result  = None
		self.m_timeout = p_timeout

		self.m_guid = p_guid

		self.m_running_cb  = None
		self.m_finished_cb = None
		self.m_aborted_cb  = None
		self.m_timeout_cb  = None
		self.m_finished_cb = None

	#----------------------------------------------------------------------
	def cleanup ( self ):
	#----------------------------------------------------------------------

		self.m_status = PENDING
		self.m_result = None

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
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	def has_guid ( self ): return bool(self.m_guid)
	def get_guid ( self ): return self.m_guid
	#----------------------------------------------------------------------


	#----------------------------------------------------------------------
	def set_running_cb  ( self, p_func ): self.m_running_cb  = p_func
	def set_aborted_cb  ( self, p_func ): self.m_aborted_cb  = p_func
	def set_timeout_cb  ( self, p_func ): self.m_timeout_cb  = p_func
	def set_finished_cb ( self, p_func ): self.m_finished_cb = p_func
	#----------------------------------------------------------------------

	#----------------------------------------------------------------------
	def set_callbacks ( self, p_callbacks ):
	#----------------------------------------------------------------------

		if p_callbacks.has_key('running'):
			self.m_running_cb  = p_callbacks['running']

		if p_callbacks.has_key('aborted'):
			self.m_aborted_cb  = p_callbacks['aborted']

		if p_callbacks.has_key('timeout'):
			self.m_timeout_cb  = p_callbacks['timeout']

		if p_callbacks.has_key('finished'):
			self.m_finished_cb = p_callbacks['finished']

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
