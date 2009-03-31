#==========================================================================
# tostdk :: tostlib :: shell_sync.py
# Shell main
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

import shell
import shell_misc
import shell_help
import shell_config
import shell_create
import shell_add
import shell_remove
import shell_rename
import shell_update
import shell_sync

#==========================================================================
def main ( ):
#==========================================================================

	shell_misc.register()
	shell_help.register()
	shell_config.register()
	shell_create.register()
	shell_add.register()
	shell_remove.register()
	shell_rename.register()
	shell_update.register()
	shell_sync.register()

	shell.main()

#==========================================================================
# End
#==========================================================================
