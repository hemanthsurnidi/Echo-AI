import os, sys
sys.path.insert(0, os.getcwd())
import app.web_demo as wd
s = wd.HTML_CONTENT
start = s.index('<div class="recorder-controls"')
print(s[start-250:start+300])
