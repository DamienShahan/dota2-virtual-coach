# Dota 2 Virtual Coach release 1.1
A virtual coach, helping you keep an eye on things, for example calling out 15 second before a rune will spawn.\
  ![main.exe](https://i.imgur.com/XErjOjz.png)
 
Release changelog found here: https://github.com/DamienShahan/dota2-virtual-coach#Changelog

# Download and usage guide
* Click on the [latest release](https://github.com/DamienShahan/dota2-virtual-coach/releases):\
  ![latest release](https://i.imgur.com/CXmSXY7.png)
* Download and extract dota2-virtual-coach.zip. The extracted folder is about 432.mb 
* Then run the file main.exe. A console window will open, just go back into the game.\
  ![main.exe](https://i.imgur.com/7BSqpjj.png)
* In the console, the script with write the current ingame time. Additionally, it will output a short message, if it is time to call out that an event is about to happen and play the associated .mp3 file.\
  ![main.exe](https://i.imgur.com/XErjOjz.png)
* To stop the script, just close the opened console window.

# Events being called out
* Bounty runes: every 3 minutes starting at 3:00
* Lotus pools: every 3 minutes starting at 3:00
* Power runes: every 2 minutes starting at 6:00
* Water runes: at 2:00 and 4:00
* XP runes: every 7 minutes starting at 7:00

# Voice pack options
There are 3 voice pack options.
1. Jenny: https://www.youtube.com/watch?v=qpzR8yDuHCE
2. Davis: https://www.youtube.com/watch?v=wxzASiHeOT0
3. Sonia: https://www.youtube.com/watch?v=2y4L1b40NCs

By default the 3. pack (female) is used. You can change this by changing the number in resource/timers.yaml on line 33: voice_pack.\
  ![main.exe](https://i.imgur.com/ugzbQ6p.png)

# Customizable settings
All timer settings can be found and changed or updated in resource/timers.yaml.\
  ![main.exe](https://i.imgur.com/X3GHrAq.png)

# Supported resolutions
* 2k (1440p)

# Future features
* Image enhancement to improve OCR results
* Further post processing of OCR results to imporve bad outputs

## Planned supported resolutions
* HD (1080p)
* 4k (2160p)

# Changelog
## v1.1
* Imporved the post processing of the OCR output
## v1.0
* Initial release

# Donations
* Any donations are greatly appreciated: https://www.paypal.com/donate/?hosted_button_id=KA7EN3NAXJ3U8
* I hope you have fun with the Dota 2 virtual coach