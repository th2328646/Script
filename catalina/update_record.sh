#! /bin/bash
if [ -f "record.txt" ];then
	rm -r "record.txt"
fi

touch record.txt

echo "0,1" >> record.txt
