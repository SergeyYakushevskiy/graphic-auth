create or replace function check_account_point_limit()
returns trigger as $func$
declare
    point_count integer;
begin
    select count(*) into point_count
    from account_point
    where account_id = new.account_id;

    point_count := point_count + 1;

    if point_count > 6 then
        raise exception 'Превышено допустимое количество точек (макс. 6) для account_id=%', new.account_id;
    end if;

    return new;
end;
$func$
language plpgsql;

create or replace trigger trg_check_account_point_limit
before insert on account_point
for each row
execute function check_account_point_limit();
