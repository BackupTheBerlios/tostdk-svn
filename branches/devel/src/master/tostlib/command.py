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
#==========================================================================


#==========================================================================
class Command ( packet.Packet ):
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_opcode, p_data = '' ):
	#----------------------------------------------------------------------

		packet.Packet.__init__(self, p_opcode, p_data)

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
	def running_cb  ( self ): pass
	def finished_cb ( self ): pass
	def abort_cb    ( self ): pass
	#----------------------------------------------------------------------


#==========================================================================
# End
#==========================================================================
