# based-file-converter
a file converter that isn't malware and is simple. it just works. that's it.
A simple, free, and open-source Python-based file converter. The current version supports converting PDF to DOCX, and it includes image extraction and basic text formatting. Now with MOV to MP4 and other audio and video file extensions, with more (obscure ones) being added later on.

- Extracts text and images from the PDF.
- Preserves basic text formatting.
- Simple status bar at the bottom
- Extremely plain and painfully easy to use GUI
- Bi- directional conversion of applicable file types
- drop down menu instead of huge stupid buttons
- Uses FFMPEG 
 
          *file types*
  PDF, DOCX, MP4, MP3, WAV, AAC, FLAC, MOV, M4A, WMA, MPG (mpeg), WEBM, WEBP

  *more added soon*
  

  it seems like nowadays, converting a file requires us to download VLC or some other program like audacity or use
  some online file converter that looks sketchy af. And recent reports of malware/ransomware in file converters is just.....
  plain stupidity. download python, FFmpeg, and use this instead. its free, its open-source, do
  whatever you want with it. i'm just here to learn more about python and have some fun along the way.

  *other features, file formats, and more will be added soon.... when i have some time.....*

  6/19/25
  more error handling,
  removed buttons entirely (pdf and docx are in dropdowns now),
  grouped file types next to each other,
  crappy dark mode toggle (it will look better soon),
  image -> image should work now using pillow (jpg -> png, webp -> bmp, etc.)
  logging was also added. a box below will tell you everything that happens and will be logged, along with event and error messages that apply,
  an output destination folder selection was also added (its a button. you can't miss it)






# Installation
0. Install python (3.11 or higher)
1. Clone the repository
2. install the requirements.txt (you need python to run this)
3. Install FFmpeg (you need this) *gyan.dev has a build for windows*
4. Add FFmpeg to your system path on windows (or put it in the same folder as the script)
5. download Pillow (pip install pillow)
6. be based and libre-pilled

