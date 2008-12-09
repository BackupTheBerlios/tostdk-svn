#==========================================================================
# tostdk :: drivers :: __init__.py
# Drivers package
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


import driver
import files_driver.files_driver as files_driver


#==========================================================================
DRIVERS = {
#==========================================================================
	'files_driver': files_driver.Driver
}


#==========================================================================
def get_driver_instance ( p_driver_name ):
#==========================================================================

	driver.Driver.del_instance()

	if DRIVERS.has_key(p_driver_name):
		return DRIVERS[p_driver_name].get_instance()

	return None


#==========================================================================
# End
#==========================================================================
