##Information / README / Documentation / Installation
####0x01        Intro
T3hb0t is an IRC bot client capable of connecting to multiple servers
and channels. Easily customized and easy to add commands.

####0x02        License
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


####0x03        Installation
Clone the repository

<code>$ git clone git@github.com:ZealDev/T3hb0t.git</code>


- - -
##Files & Usage
####1x01        commands_list.py
This is the file where you put all your commands. All public methods (without a _ infront) will be available through the bot by doing: 
<code>$methodName &lt;arg1&gt; &lt;arg2&gt; .</code>
All private methods (with _ infront of method name) will not be accessible through the bot, but will ofcourse be accessible in the class.

The commands usage is documented in the docstring of the method. This is then used when you do $help to get a list of commands and how to use them.

Standard commands are:

<code>$help</code>

Outputs the available commands and their usage.

<code>$note : Usage: note &lt;to nickname&gt; &lt;note&gt;</code>

If &lt;to nickname&gt; &lt;note&gt; is supplied, it saves a note to the given nickname.
If &lt;to nickname&gt; &lt;note&gt; is omitted, it lists out all notes that are not set to 'read'.

<code>$notelist : Usage: notelist</code>

Outputs a list of all notes with their corresponding id's.

<code>$noteread : Usage: noteread &lt;id&gt;</code>

Gives a note the status of 'read', so it doesn't show in $note.

<code>$backin : Usage: backin &lt;time&gt;</code>

Saves a your expected time of return. Used like this: 

`$backin 2.5h` (for 2 and a half hours)

`$backin 30m` (for 30 minutes)

<code>$back : Usage: back &lt;nickname&gt;</code>

Outputs when the given nickname (person) will be back (if the person saved it with $backin).

