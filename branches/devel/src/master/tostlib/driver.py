#==========================================================================
# tostdk :: drivers :: driver.py
# Drivers wrapper
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


import logging
import configuration

import drivers.files_driver


#==========================================================================
DRIVERS = {
#==========================================================================
	'files_driver':		drivers.files_driver.FilesDriver
}


#==========================================================================
class Driver:
#==========================================================================

	# NOTE: this is not a real singleton, this class isn't supposed
	#       to be instantiated

	s_instance = None

	#----------------------------------------------------------------------
	@classmethod
	def get_instance ( cls ):
	#----------------------------------------------------------------------

		l_configuration = configuration.Configuration.get_instance()
		l_driver_name   = l_configuration.get_option_value('drivers', 'driver_name')

		if DRIVERS.has_key(p_name):
			l_class = DRIVERS[p_name]

			if cls.s_instance == None or not isinstance(cls.s_instance, l_class):
				cls.s_instance = l_class(l_configuration)

		else:
			logging.error("Can't find driver class: " + p_name)
			cls.s_instance = None

		return cls.s_instance

	#----------------------------------------------------------------------
	@classmethod
	def del_instance ( cls ):
	#----------------------------------------------------------------------

		cls.s_instance = None

	#----------------------------------------------------------------------
	def __init__ ( self ):
	#----------------------------------------------------------------------

		raise RuntimeError


#==========================================================================
# End
#==========================================================================
