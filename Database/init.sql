CREATE DATABASE timesheet;

USE timesheet;

CREATE TABLE timesheet(
    id Integer primary key auto_increment,
    user_id integer not null,
    date datetime(6),
    update_at datetime(6),
    hour time(6),
    pause_name varchar(15),
    event_name varchar(15)
);

CREATE TABLE user(
    id Integer primary key auto_increment,
    name varchar(50) not null,
    username varchar(30) not null,
    password varchar(150) not null,
    is_admin tinyint(1),
    is_active tinyint(1),
    create_at datetime(6),
    update_at datetime(6)
)
