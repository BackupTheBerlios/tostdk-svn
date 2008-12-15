#==========================================================================
# tostdk :: tostlib :: singleton.py
# Singleton base class
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


#==========================================================================
class Singleton:
#==========================================================================

	# NOTE: s_instance class attribute must be declared
	#       in the derived class!

	#----------------------------------------------------------------------
	@classmethod
	def get_instance ( cls ):
	#----------------------------------------------------------------------

		if cls.s_instance == None:
			cls.s_instance = cls()

		return cls.s_instance

	#----------------------------------------------------------------------
	@classmethod
	def create_instance ( cls ):
	#----------------------------------------------------------------------

		if cls.s_instance == None:
			cls.s_instance = cls()

	#----------------------------------------------------------------------
	@classmethod
	def del_instance ( cls ):
	#----------------------------------------------------------------------

		cls.s_instance = None

	#----------------------------------------------------------------------
	def __init__ ( self ):
	#----------------------------------------------------------------------

		assert (self.s_instance == None)


#==========================================================================
# End
#==========================================================================
