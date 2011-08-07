all:
	pyuic4 mainwindow.ui -o ui_mainwindow.py
	pyuic4 grabdialog.ui -o ui_grabdialog.py

clean:
	-rm *.pyc ui_*.py
