#PyBot
An easily extensible IRC bot written in python 3.

---

###Configuration
The configuration file uses JSON. You can create a default configuration file by running the program with the -c parameter.

The following is an example of a configuration file. The config file should be placed in the root directory of the bot (i.e. the same directory as the src folder is placed in).
<pre>
{
    "nickname": "PyBot", 
    "realname": "PyBot",  
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

---
###License
Is found in the license file. But also here:
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
        * Neither the name of the <organization> nor the
          names of its contributors may be used to endorse or promote products
          derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    # DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
</pre>