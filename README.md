# Nw2esper

Prerequisite:
  - need python 3 (unless you use the EXE)
  - download from https://www.python.org/downloads/
  - check the box "show debug information" from the settings dropdown in the top right corner of the investigation screen in NetWitness.

Directions:
  - Run application [Download](https://github.com/trevormiller6/nw2esper/blob/master/Nw2esper.exe)
  - copy query from SIEM. This is important as you need the time range. (If you dont see the query as pictured below, see bullet 3 in Prerequisite)

![IMAGE](https://community.rsa.com/servlet/JiveServlet/downloadImage/2-899003-352385/770-275/investigation.png)


![IMAGE](https://github.com/trevormiller6/nw2esper/blob/master/screenshot.PNG)
  - Paste into Query Field
  - enter username/password
  - name the output file (appends date and time to name) (opional)
  - Hit Start button
  - open output file with events and Schema
  - the schema is at the very bottom of the output file.
  - Enter Schema in left pane and events in center pane.

  ![IMAGE](https://community.rsa.com/servlet/JiveServlet/downloadImage/2-899003-352389/770-634/esper+tryout+page.png)

**Known Issues**
*  None Known. Let me know if issues arise.

Adapted by Trevor & Julian originally created by Maximiliano Cittadini. Original source https://community.rsa.com/thread/193397
