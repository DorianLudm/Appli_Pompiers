delimiter |
create trigger ajoutHistorique after insert on DOCUMENT 
begin 
    insert into HISTORIQUE_DOCUMENT values (new.idDoc, NOW());
end|


create trigger ajoutHistorique_update after update on DOCUMENT 
begin 
    insert into HISTORIQUE_DOCUMENT values (new.idDoc, NOW());
end|
delimiter ;
