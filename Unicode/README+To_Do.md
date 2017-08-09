####################################################################################################
#
# Unicode Presentation for [MUG](http://www.mug.org/2017/07/august-8th-2017-mug-meeting/)

This presentation was delivered at the Farmington Public Library on August 9, 2017.  From getting back into programming for the last couple years I have repeated run into snags such as:
* Garbled Ouput
  * When I ssh into a Linux system (terminal emulation), why is some of the output gibberish?
    * Seems like non-ASCII characters (outside of 0-127 range) aren't interpreted correctly
  * e.g., viewing man pages, using TUI apps (similar to above)
* File Interpretation Problems
  * When I open a file, why do I see lots of gobbledygook instead of text?
    * It seems like Windows and Linux encode text files differently - and I'm not talking about line endings but rather the actual text representation.
  * Why does my program freak out when I paste something from a web page?
    * Seems like web pages have non-ASCII characters (outside of 0-127 range) that many CLI tools don't like or can't deal with
  * More problems when my code/config has non-ASCII characters (outside of 0-127 range):
    * Git sees my text/code as a binary as opposed to text
    * Deploying to Heroku fails - buildpack blows up, worthless error message
    * Ansible "push" fails, worthless error message
* Modern apps/web sites/documents need to support more than just basic ASCII characters
  * Math, Science, Music symbols, Emojis, Icon fonts - Unicode is clearly useful but I don't feel like I really grok Unicode

When I'd run into these issues, I couldn't find anyone who seems to be a Unicode or character encoding expert.  The answers I'd get were along the lines of you found a solution so don't worry about it.  As this was less than satisfying to me I decided to create this presentation to get my head around Unicode and character encoding.  I hope you like it.  Feel free to leave a comment or open an issue if you see something wrong/missing.


# Unicode Preso - Possible Improvements

* Could better organize the reference section

