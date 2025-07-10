--liquibase formatted sql

--changeset yakushevskiy:05-create-index-on-account-point
create index if not exists idx_account_point_position on account_point(account_id, position_index);