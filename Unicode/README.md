# Presentation - Unicode
## Created as a talk for [MUG](http://www.mug.org) - August 8, 2017

## Synopsis
Presentation for the MUG Detroit metro area user group on getting your head around Unicode.  From getting back into programming for the last couple years I have repeated run into snags such as:
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

## Links
* [MUG user group information on presentation](http://www.mug.org/2017/07/august-8th-2017-mug-meeting/)
* [Presentation recording (YouTube)](https://www.youtube.com/watch?v=ONf1x7pOZNg)

## Directory Contents:
* PowerPoint presentation
    * Note:  Corrections tracked in GitHub if you/someone wants details
* PDF version of PowerPoint presentation

## Notes on presentation files
* The .pptx file was created in Microsoft PowerPoint 2013 albeit using an old template file
  * This version has the speaker notes
  * Annoyingly though, the embedded hyperlinks (i.e., in the Reference slides) aren't clickable.  Instead, you have to "right-click" and select Open Hyperlink.
* The .pdf file was exported from PowerPoint 2013
  * This version has clickable hyperlinks but unfortunately no speaker notes
  * It is possible to export a full page PDF which includes the speaker notes.  However, the template I'm using has a bunch of cruft that it puts in there.  In order to publish this version of the slides I'd have to do some cleanup.  Perhaps in the future...
