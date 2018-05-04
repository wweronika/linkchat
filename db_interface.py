import sqlite3

conn = sqlite3.connect('data.db')

c = conn.cursor();


c.execute("CREATE TABLE `Users` (`ID` INT NOT NULL AUTO_INCREMENT,`nick` VARCHAR(255) NOT NULL UNIQUE,`password` VARCHAR(255) NOT NULL,PRIMARY KEY (`ID`))";
