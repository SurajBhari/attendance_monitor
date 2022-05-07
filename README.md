# attendance_monitor

Takes your College/Class Schedule as in JSON file and then post a webhook on the time 
which is then taken by the BOT that DM's the owner of the bot (probably you) and ask for the input
later take the same data into account and show it in a better way 


# How to use it ? 
1. Configure schedule.json as per your needs
2. run main.py as a cron job - "*/5 * * * * cd /home/ubuntu/attendance_monitor && python3 main.py"
3. run recv.py as a background job "nohup python3 recv.py &" - "&" here means to run the command in background

# Screenshots - </br>
![image](https://user-images.githubusercontent.com/45149585/166979152-eacc60ae-7712-4a14-9c2c-17971ee503ed.png)</br>
WebHook - </br>![image](https://user-images.githubusercontent.com/45149585/166979261-63828571-9f6b-4b59-81d7-2ce02363bbdf.png)</br>
Bot Response - </br>![image](https://user-images.githubusercontent.com/45149585/166979276-97d53b07-c7d7-47d5-b0c6-316de5c7cfcf.png)</br>
On accepting - </br>![image](https://user-images.githubusercontent.com/45149585/166979380-ccc27663-e42c-4043-9ecb-d020668cffeb.png)</br>

# Commands - 
<img src="https://user-images.githubusercontent.com/45149585/166979654-fdf3ad39-5451-4805-afd0-d909d8bbbc4b.jpg" height="1132" width="243">

