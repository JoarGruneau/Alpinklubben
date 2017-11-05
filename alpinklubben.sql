create table if not exists users (
id integer primary key autoincrement,
username text not null,
email text not null,
password text not null
);
create table if not exists cart (
id integer primary key autoincrement,
username text not null,
description text not null,
price i nnteger not null
);
