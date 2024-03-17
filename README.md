### Job между PE и Origination
Напрямую нет взаимодействия между двумя сервисами, все происходит через него.  
Что происходит? Он берет все договора в статусе NEW из PE и отправляет в Origination, дожидаясь OK, 
после которого меняет статус на SCORING в PE.  
Что может пойти не так?
*  Запрос на post не дойдет -> в следующий интервал заново произойдет запрос
*  Origination добавит у себя договор, но не дойдет OK обратно -> в следующий интервал заново произойдет запрос, но 
Origination проверит если такой договор у него и отправит его данные в случае нахождения

### Job между Origination и Scoring
Берет все договора в Origination и отправляет в Scoring заглушку, в случае обратного OK меняет статус на SCORING.  
Что может пойти не так?
*  Запрос на post не дойдет -> в следующий интервал заново произойдет запрос
*  Не дойдет OK обратно -> в следующий интервал заново произойдет запрос