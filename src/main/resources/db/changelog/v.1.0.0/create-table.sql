--liquibase formatted sql

--changeset yakushevskiy:01-create-account-table
create table if not exists account (
    id uuid primary key,
    login varchar(64) not null unique,
    email varchar(128) not null unique,
    is_enabled boolean not null default true,
    created_at timestamp not null default now()
);

--changeset yakushevskiy:02-create-password-hash-table
create table if not exists password_hash (
    account_id uuid not null,
    hash text not null,
    created_at timestamp not null default now(),
    primary key(account_id, hash),
    foreign key (account_id) references account(id) on delete cascade
);

--changeset yakushevskiy:03-create-profile-table
create table if not exists profile (
    account_id uuid not null unique,
    first_name varchar(64),
    last_name varchar(64),
    birth_date date,
    foreign key (account_id) references account(id) on delete cascade
);

--changeset yakushevskiy:04-create-account-point-table
create table if not exists account_point (
    account_id uuid not null,
    x integer not null,
    y integer not null,
    position_index integer not null, -- порядок ввода
    hash text not null,
    created_at timestamp not null default now(),
    primary key(account_id, x, y),
    foreign key (account_id) references account(id) on delete cascade
);
