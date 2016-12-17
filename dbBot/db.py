# -*- coding: utf-8 -*-

# En MySql:

# mysql -u root -p test < db_script
# create database test;
# create user 'testuser'@'localhost' identified by 'testuser';
# use test
# grant all on test.* to 'testuser'@'localhost';


import MySQLdb as mdb

con = mdb.connect('localhost','testuser','testuser','test')

cur = con.cursor()

cur.execute("create table usuarios(chat_id int primary key, name varchar(25))")

cur.execute("SELECT COUNT(*) FROM users WHERE users.chat_id = 1 limit 1") # Si hay un user en la base de datos

cur.execute("select chat_id from users where (name = 'Juan')") # Sacar un nombre con un chat_id

rows = cur.fetchall()
