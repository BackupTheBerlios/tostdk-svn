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
import opcodes
import data


#==========================================================================
class Result ( packet.Packet ):
#==========================================================================

	#----------------------------------------------------------------------
	def __init__ ( self, p_opcode, p_data ):
	#----------------------------------------------------------------------

		packet.Packet.__init__(self, p_opcode, p_data)

	#----------------------------------------------------------------------
	@classmethod
	def create ( cls, p_name, p_args ):
	#----------------------------------------------------------------------

		l_opcode = opcodes.result_opcode(p_name)
		l_format = opcodes.result_format(p_name)

		if l_opcode == None or l_format == None:
			return None

		l_data = data.pack(l_format, p_args)

		if l_data == None:
			return None

		return cls(l_opcode, l_data)

	#----------------------------------------------------------------------
	def is_ok ( self ):
	#----------------------------------------------------------------------

		return opcodes.is_ok_result(self.get_opcode())

	#----------------------------------------------------------------------
	def is_error ( self ):
	#----------------------------------------------------------------------

		return opcodes.is_error_result(self.get_opcode())

	#----------------------------------------------------------------------
	def get_name ( self ):
	#----------------------------------------------------------------------

		return opcodes.result_name(self.get_opcode())

	#----------------------------------------------------------------------
	def get_format ( self ):
	#----------------------------------------------------------------------

		l_name = self.get_name()

		if l_name == None:
			return None

		return opcodes.result_format(l_name)

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


#==========================================================================
# End
#==========================================================================
