This script contains the code to identify those tables in database that are having auto-increment ids and are running short off those ids. Once it identifies those tables it will send an alert to slack using the webhook through the script. Lets visualize this scenario through the screenshots.

This pic below shows that currently I have two tables in my postamn(name of the database) database, table T1 and table T2. Each table has auto-increment id. In table T1 the auto-increment id starts by default from index 1. while in table T2 the auto-increment id starts from index 100000000. Both the tables have sufficient ids because the max value of the int(11) is 2147483647. Here int(11) is the data type of the primary keys in both tables.

![pic2](https://user-images.githubusercontent.com/15075776/47616953-ebe94000-dae8-11e8-8b95-16dbc7910502.png)

--> When you run the python script, following messages will appear on the slack #general channel screeen. We can send the alert to any channel accordingly the url will change. Here you can see that message reads --> "hello, everything is fine", that means everything is fine and ids are not running short of indexes. You see so many messages of same type because I used a timer due to which it sends the update to slack every 5 mins.

![pic1](https://user-images.githubusercontent.com/15075776/47616944-e0961480-dae8-11e8-89f7-403853476c42.png)

--> Now in next step what I do is, I will change the auto-increment value of table T2 to some very big number such that the number is >2147483647(max limit of auto-increment id).
I did this opertion using alter table command.

![pic3](https://user-images.githubusercontent.com/15075776/47616956-ee4b9a00-dae8-11e8-8ad3-5a8c6c9cfc43.png)


--> Now when you run python script, see what happens. Look at the last message in the pic. It reads --> "table T2 are about to run short of auto-increment id".  

![pic4](https://user-images.githubusercontent.com/15075776/47616957-f0adf400-dae8-11e8-8af6-b3bfeafcb699.png)


--> This is the query I used, to identify whether there is any table in database that is running short of auto-incement ids.

![pic5](https://user-images.githubusercontent.com/15075776/47617492-a2e7ba80-daed-11e8-8fd5-b76c51230ecb.png)

  
  --> This query gives a beautiful table that contains the auto-increment ratio of each table in database. If this ratio is around 0.954, that means about 95% of the ids are used up and are about to run short of ids.

![pic6](https://user-images.githubusercontent.com/15075776/47617495-a5e2ab00-daed-11e8-9876-7dda0e76e6c2.png)

--> Formula to calculate auto-increment ratio is:

![pic7](https://user-images.githubusercontent.com/15075776/47617677-93697100-daef-11e8-811a-2f7b06ea0e98.png)



--> Hope this readme was useful in understanding what exactly my scrip does. Feel free to explore and edit.
