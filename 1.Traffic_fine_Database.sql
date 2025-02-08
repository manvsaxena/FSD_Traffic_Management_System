-- Drop the database if it exists
DROP DATABASE IF EXISTS trafficfine;

-- Create the database
CREATE DATABASE trafficfine;
USE trafficfine;

CREATE TABLE login (
    u_id INT PRIMARY KEY,
    un VARCHAR(20),
    pass INT(20)
);

INSERT INTO login(u_id, un, pass) VALUES(1, 'sumukha_kashyap',2003);
INSERT INTO login(u_id, un, pass) VALUES(2, 'somashekar',2006);


create table RTO_Vehicle(reg_dt DATE,
                         vehicle_no varchar(20) PRIMARY KEY NOT NULL,
                         vehicle_year INT CHECK (vehicle_year > 1900),
                         vehicle_model varchar(30),
                         owner_id int,
                         zone_id int);

create table violation (violation_id int PRIMARY KEY,
                        viol_type varchar(20),
                        dt_time TIMESTAMP,
                        amount int NOT NULL,
                        loc varchar(20),
                        zone_id int,
                        vehicle_no varchar(20) NOT NULL,
                        viol_img longblob);

create table paid_violation(violation_id int PRIMARY KEY,
                            viol_type varchar(20),
                            dt_time TIMESTAMP,
                            amount int NOT NULL,
                            loc varchar(20),
                            zone_id int,
                            vehicle_no varchar(20) NOT NULL);

create table payment (payment_id int PRIMARY KEY,
                      violation_id int,
                      amount int, 
                      dt_time TIMESTAMP,
                      stat ENUM('success','failure'));

create table citizen(aadhaar_id int PRIMARY KEY,
                     c_name varchar(30),
                     dl_no varchar(10),
                     addr varchar(100),
                     gender enum('M','F','O'),
                     phno varchar(20));

create table zone (zone_id int PRIMARY KEY,
                   zone_name varchar(20),
                   zonal_officer varchar(20));
