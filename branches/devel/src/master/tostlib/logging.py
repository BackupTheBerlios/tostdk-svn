#==========================================================================
# tostdk :: tostlib :: logging.py
# Logging functions
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


import os
import sys

import configuration


#==========================================================================
if sys.platform == 'win32':
	LOGFILE = os.path.join(os.getcwd(), 'tostdk.log')
else:
	LOGFILE = '/var/log/tostdk.log'
#==========================================================================


#==========================================================================
def reset_logfile ( ):
#==========================================================================

	if os.path.exists(LOGFILE):
		try:
			os.path.remove(LOGFILE)
		except:
			sys.stderr.write("[LOGGING] Can't reset log file: " + LOGFILE + os.linesep)

#==========================================================================
def write_logfile ( p_string ):
#==========================================================================

	try:
		l_handle = open(LOGFILE, 'a+b')
		l_handle.write(p_string + os.linesep)
		l_handle.close()
	except:
		return False

	return True

#==========================================================================
def message ( p_string ):
#==========================================================================

	write_logfile(p_string)

	l_config = configuration.Configuration.get_instance()
	if l_config.get_option_value('general', 'verbose'):
		sys.stdout.write(p_string + os.linesep)

#==========================================================================
def warning ( p_string ):
#==========================================================================

	l_string = '[WARNING] ' + p_string
	write_logfile(l_string)

	l_config = configuration.Configuration.get_instance()

	if l_config.get_option_value('general', 'verbose'):
		sys.stderr.write(l_string + os.linesep)

#==========================================================================
def error ( p_string ):
#==========================================================================

	l_string = '[ERROR] ' + p_string
	write_logfile(l_string)

	l_config = configuration.Configuration.get_instance()

	if l_config.get_option_value('general', 'debug'):
		raise RuntimeError

	if l_config.get_option_value('general', 'verbose'):
		sys.stderr.write(l_string + os.linesep)


#==========================================================================
# End
#==========================================================================
