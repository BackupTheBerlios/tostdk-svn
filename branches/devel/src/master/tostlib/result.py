#==========================================================================
# tostdk :: tostlib :: result.py
# Result packet class
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
class Result ( packet.Packet ):
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_opcode, p_data ):
	#----------------------------------------------------------------------

		packet.Packet.__init__(self, p_opcode, p_data)


#==========================================================================
# End
#==========================================================================
