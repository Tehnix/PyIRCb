# PyBot #
An easily extensible IRC bot written in python 3...

### Table of Contents ###

- [Configuration of the bot](#configuration-of-the-bot)
- [Modules](#modules)
- [Module Development](#module-development)
- [Command line options](#command-line-options)
- [License](#license)

## Configuration of the bot ##
The configuration file uses JSON. You can create a default configuration file by running the program with the -c parameter.

`./main.py -c`

The following is an example of a configuration file. The config file should be placed in the root directory of the bot (i.e. the same directory as the src folder is placed in).
<pre>
    {
    "nickname": "PyBot", 
    "realname": "PyBot", 
    "operator": "$", 
    "servers": {
        "freenode": {
            "address": "irc.freenode.org",
            "port": 6697,
            "ssl": true, 
            "identify": false,
            "channels": ["#python"]
        }
    },
    "commands": {
        "cf": {
            "tkn": "cloudflare token", 
            "z": "site", 
            "email": "email"
        }
    }
}
</pre>

## Modules ##
At the moment there are several modules that go with the system by default. The plan is to later move some of these out into separate repositories, and keep some of the more essential ones.

- User module: Features a authentication system and other user related tools
- Project module: The ability to store projects and information about them. This module requires the user module.
- Git module: Features like git pull and git clone
- CloudFlare module (cf): Get statistics from your CloudFlare site, and also purge your CloudFlare cache.

## Module Development ##
You can generate a module with the scaffolding by doing `./main.py -m mymodule`, which creates the module mymodule for you in the modules directory.

#### A little bit about modules: ####

A module extends the `ModuleBase` class found in src/moduleBase. This provides some functionality to get easily started (though it is not required). The only thing special about a module is it's `__init__`  method, which can look like the following:

<pre>
    class User(src.moduleBase.ModuleBase):
        """Common user commands, and an auth system."""
    
        def __init__(self, cmdHandler, cmdName=None, cmdArgs=None):
            super(User, self).__init__(
                cmdHandler,
                cmdArgs=cmdArgs,
                authRequired=['rm']
            )
            self.db = 'database.sqlite3' # creates the database instance
            self._createTables([
                'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, nickname TEXT, password TEXT, server TEXT)'
            ])
            if cmdName is not None:
                self._execute(cmdName)
</pre>

This example shows the User module, which extends the `ModuleBase`, and inits it's superclass using `super()` with some additional parameters in the supers `__init__` . The `authRequired` keyword argument holds the names of the methods in the class which should require authentication. 

The only custom thing about the user `__init__` (other than the `authRequired`), is the creation of it's tables, which uses a method defined in the `ModuleBase` class to connect to a SQLite3 database file, and then create the tables.

There are some neat functions that the `ModuleBase` sets for you:
- `self.reply` - method to send a message to the IRC
- `self.username` - the user that executed the command
- `self.server` - the server object
- `self.db` - access to the database object (which has neat methods for easy insert, update etc. The file is located in src/database.py)
- `self.args` - unicode string containing the arguments passed to the module
- `self.bargs` - bytes string containing the arguments passed to the module
- `self.cmdHandler` - access to the commandHandler instance
- `self.authRequired` - methods that require authentication



## Command line options ##
All the command line options can be seen in the help menu of the bot, by typing `./main.py -h`:
<pre>
    usage: main.py [-h] [-c] [-v] module module

    A python based IRC bot

    optional arguments:
      -h, --help     show this help message and exit
      -c, --config   generate a default configuration file
      -v, --verbose  print output to stdout
      -m--module MODULE  generate a module scaffold
</pre>

## License ##
The source code is released under the BSD license. If you have any problems with this, or need another type of license, just contact me, and I'll fix it :)...
<pre>
    Copyright (c) 2012, Christian Kjær Laustsen (Tehnix)
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
        * Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in the
          documentation and/or other materials provided with the distribution.
        * Neither the name of the ZealDev nor the
          names of its contributors may be used to endorse or promote products
          derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL Christian Kjær Laustsen BE LIABLE FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
</pre>
