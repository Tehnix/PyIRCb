##Information / README / Documentation / Installation
####0x01        Intro
T3hb0t is an IRC bot client capable of connecting to multiple servers
and channels. Easily customized and easy to add commands.

####0x02        License
Is found in the license file. But also here:
<pre>
    Copyright (C) 2012 

    This program is free software; you can redistribute it and/or modify it 
    under the terms of the GNU General Public License as published by the Free 
    Software Foundation; either version 2 of the License, or (at your option) 
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT 
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
    more details.

    You should have received a copy of the GNU General Public License along with 
    this program; if not, write to the Free Software Foundation, Inc., 59 Temple 
    Place, Suite 330, Boston, MA 02111-1307 USA.
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

