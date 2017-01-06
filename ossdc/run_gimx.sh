# The commands are described here: https://gimx.fr/wiki/index.php?title=Controller_Maps 
#sudo service bluetooth stop
#replace 00:00:00:00:00:00 with PS3 console address
gimx --src 127.0.0.1:51914 --status -t Sixaxis -b 00:00:00:00:00:00 &
sleep 2 && gimx --event "abs_axis_2(255)" --dst 127.0.0.1:51914 && sleep 3 && gimx --event "abs_axis_2(0)" --dst 127.0.0.1:51914 
sleep 2 && gimx --event "circle(255)" --dst 127.0.0.1:51914 && sleep 0.2 && gimx --event "circle(0)" --dst 127.0.0.1:51914 
sleep 2 && gimx --event "circle(255)" --dst 127.0.0.1:51914 && sleep 0.2 && gimx --event "circle(0)" --dst 127.0.0.1:51914 
sleep 2 && gimx --event "start(255)" --dst 127.0.0.1:51914 && sleep 0.2 && gimx --event "start(0)" --dst 127.0.0.1:51914 
sleep 2 && gimx --event "left(255)" --dst 127.0.0.1:51914 && sleep 0.1 && gimx --event "left(0)" --dst 127.0.0.1:51914
sleep 2 && gimx --event "right(255)" --dst 127.0.0.1:51914 && sleep 0.1 && gimx --event "right(0)" --dst 127.0.0.1:51914
sleep 2 && gimx --event "cross(255)" --dst 127.0.0.1:51914  && sleep 0.1 && gimx --event "cross(0)" --dst 127.0.0.1:51914 
sleep 5
killall gimx
