DELETE t1 FROM weather_data t1
INNER JOIN weather_data t2
WHERE
    t1.id > t2.id AND
    t1.ville = t2.ville AND
    t1.scrape_date = t2.scrape_date;

GRANT ALL PRIVILEGES ON First_Data.* TO 'davy'@'localhost';
FLUSH PRIVILEGES;