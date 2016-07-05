
clean:
	mv wiki-Vote.txt wiki
	rm -f *.pyc
	rm -f slave*/*.pyc
	rm -f *.txt
	rm -f slave*/*.txt
	mv wiki wiki-Vote.txt
