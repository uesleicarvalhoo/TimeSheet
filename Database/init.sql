CREATE DATABASE timesheet;

USE timesheet;

CREATE TABLE user(
    id integer primary key auto_increment,
    name varchar(50) not null,
    username varchar(30) not null,
    password varchar(150) not null,
    workload integer,
    admin tinyint(1),
    active tinyint(1),
    created_at datetime(6),
    updated_at datetime(6)
);

CREATE TABLE register(
    id Integer primary key auto_increment,
    user_id integer not null,
    date datetime(6),
    entry time(6),
    finish time(6),
    created_at datetime(6),
    updated_at datetime(6)

);

CREATE TABLE pauses(
    id integer primary key auto_increment,
    register_id integer,
    pause_id integer,
    init time(6),
    finish time(4),
    created_at datetime(6),
    updated_at datetime(6)
);

CREATE TABLE pause_infos(
    id integer primary key auto_increment,
    init_label varchar(50) not null,
    end_label varchar(50) not null,
    time integer not null
);
