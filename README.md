--> This script contains the code to identify those tables in database that are having auto-increment ids and are running short off those ids. Once it identifies those tables it will send an alert to slack using the webhook through the script. Lets visualize this scenario through the screenshots.

--> This pic below shows that currently I have two tables in my postamn(name of the database) database, table T1 and table T2. Each table has auto-increment id. In table T1 the auto-increment id starts by default from index 1. while in table T2 the auto-increment id starts from index 100000000. Both the tables have sufficient ids because the max value of the int(11) is 2147483647. Here int(11) is the data type of the primary keys in both tables.

![pic2](https://user-images.githubusercontent.com/15075776/47616953-ebe94000-dae8-11e8-8b95-16dbc7910502.png)

--> When you run the python script, following messages will appear on the slack #general channel screeen. We can send the alert to any channel accordingly the url will change. Here you can see that message reads --> "hello, everything is fine", that means everything is fine and ids are not running short of indexes. You see so many messages of same type because I used a timer due which it sends the update every 5 mins.

![pic1](https://user-images.githubusercontent.com/15075776/47616944-e0961480-dae8-11e8-89f7-403853476c42.png)

--> Now in next step what I do is, I will change the auto-increment value of table T2 to some very big number such that the number        is >2147483647.
I did this opertion using alter table command.
![pic3](https://user-images.githubusercontent.com/15075776/47616956-ee4b9a00-dae8-11e8-8ad3-5a8c6c9cfc43.png)


--> Now when you run python script, see what happens. Look at the last message in the pic. It reads --> table T2 are about to run short of auto-increment id.  
![pic4](https://user-images.githubusercontent.com/15075776/47616957-f0adf400-dae8-11e8-8af6-b3bfeafcb699.png)


--> This is the query I used, to identify whether there is any table in database that is running short of auto-incement ids.

SELECT
  TABLE_SCHEMA,
  TABLE_NAME,
  COLUMN_NAME,
  DATA_TYPE,
  COLUMN_TYPE,
  IF(
    LOCATE('unsigned', COLUMN_TYPE) > 0,
    1,
    0
  ) AS IS_UNSIGNED,
  (
    CASE DATA_TYPE
      WHEN 'tinyint' THEN 255
      WHEN 'smallint' THEN 65535
      WHEN 'mediumint' THEN 16777215
      WHEN 'int' THEN 4294967295
      WHEN 'bigint' THEN 18446744073709551615
    END >> IF(LOCATE('unsigned', COLUMN_TYPE) > 0, 0, 1)
  ) AS MAX_VALUE,
  AUTO_INCREMENT,
  AUTO_INCREMENT / (
    CASE DATA_TYPE
      WHEN 'tinyint' THEN 255
      WHEN 'smallint' THEN 65535
      WHEN 'mediumint' THEN 16777215
      WHEN 'int' THEN 4294967295
      WHEN 'bigint' THEN 18446744073709551615
    END >> IF(LOCATE('unsigned', COLUMN_TYPE) > 0, 0, 1)
  ) AS AUTO_INCREMENT_RATIO
FROM
  INFORMATION_SCHEMA.COLUMNS
  INNER JOIN INFORMATION_SCHEMA.TABLES USING (TABLE_SCHEMA, TABLE_NAME)
WHERE
  TABLE_SCHEMA NOT IN ('mysql', 'INFORMATION_SCHEMA', 'performance_schema')
  AND EXTRA='auto_increment';
  
  --> This query gives a beautiful table that contains the auto-increment ratio of each table in database. If this ratio is around 0.954, that means about 95% of the ids are used up and are about to run short of ids.
  
