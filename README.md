# retrofeConvert
Script to convert sselph scraper metadata for Emulation Station into RetroFE Hyperspin style format and extract story files.

Purpose: Take the gamelist.xml generated from thegamesdb and other sources by the sselph scraper: https://github.com/sselph/scraper for emulationsstation and retropie, convert it to the hyperspin-style xml format with RetroFE uses to pull metadata. It also generates individual story files in a sub-directory for each named game in the xml if sselph was able to pull a description field from thegamesdb or mamedb.

DISCLAIMER: I'm not a programmer. I took up Python specifically to do this, and because I thought it would be a good skill to pickup.  8)
Update: Does not currently work with Nintendo DS set renamed through No-intro dat. (Probably do to some of my hack methods of field renaming).
Update 2: MAME version taken down for bug-fixing. Stick with normal for No-intro sets currently.
Update 3: Current files removed, new merged version incoming shortly.
Update 4: Version 1.0 MAME and Standard versions merged, bugs fixed. See Things to Know.
Update 5: 1.1 - Light Cleanup of code, added comments back in.

Things to know: Currently case sensitive in some spots. For sets like MAME or Nintendo DS some of the functions are modified due to the way game name is handled. The program knows this based on the system type you give it. Currently Arcade, MAME or Nintendo DS (not case sensitive) will automatically work. This should work for any scenario like this, but I will need to add the system names that require the code variation, currently (DS, MAME, Intellivision). SEE TESTED.
It will error out or produce poor output if there are weird characters (usually malformed from a bad pull) in your game titles (?,/,etc) 

GameListConvert 1.1 (Executable)
https://drive.google.com/open?id=0B-w601r8Y_lXNGM4VF96ZHdGQ1U
GameListConvert 1.1 (Python Script)
https://drive.google.com/open?id=0B-w601r8Y_lXNVFldS1hcDdSdWM
Sample MAME and SNES gamelist.xml files attached to post for testing.

How to use:
Place in directory with the xml you want to convert.
Run program.
Give it the case-senstitive filename ex: gamelist.xml
Give it the name of the system which will also be the output file (no extension needed) ex: Nintendo Entertainment System
Place the xml it generates into your RetroFE meta folder.
Delete existing meta.db and run RetroFE

Should be fairly quick and leave you with your original source file, the output file and a story subdirectory housing the story text files.

TESTED WITH VERSION (1.0):
System	Format
Atari 2600	Rom Hunter v11.0
Atari 5200	No-Intro
Atari 7800	No-Intro
Nintendo DS	Scene Converted to No-Intro
MAME	MAME .178 Roms
Super Nintendo	No-Intro
Super Nintendo	No-Intro
Mattel Intellivision	GoodRoms



ToDo:
Rewrite cleaner code: Needs more consistent variable naming, general cleanup etc.
Remove case sensitivity: Pretty easy I believe, an oversight on my part. Likely soon.
Integrate MAME/Arcade with the standard program: probably defined by the system you input ie MAME, FinalBurn or the like. Likely soon[/s].
Rescore based on the old rating element: Tried to get this working today without much success as xml elements don't work as floats... and I don't know what I'm doing ;)
Checks for existing files: Don't write the story file if it already exists.
If No <description> element exists or is blank/none then skip outputting story file: Currently outputs blank or "None" in text file. Had trouble with this one as well :p
I've requested <rating> (esrb) and <cloneof> fields in the sselph process. If those are implement they will be passed through the program and help with MAME for clones and ESRB ratings obviously.

ToDo Much Later
Drag n' drop UI: May happen.
Checkboxes: Don't extract story files, or ignore certain fields. Integrate changed fields into existing xml. Less Likely.

Feedback is appreciated should anyone use it. Go ahead and throw bugs my way though no promises on the fix.
It should not touch your source file ever. Hasn't in any of my extensive testing, but no promises. Don't try to name your new file the same as your source (forgot to test this, will probably break the program, but if successful you would lose your source file in this case).

Any real, nice, python programmers who would want to be generous and look at the code and show me all the glaring inefficiencies (there are a ton) I would welcome that too.
