## CRUD sql stuff

`python3 ./test_sqlite_crud.py`

This shows the id of the record inserted, the record selected (as a dictionary), the number of records updated (and the email used to execute the update), and the number of records deleted.

Additionaly stub data was added to demo the delete functionality but this was left commented out.  The evaluator may choose to uncomment this and see the delete function performing a delete.

I chose not to truncate the table if a gender was not received in the delete function.  Instead to avoid errors on each fresh test run the table is wiped clean in the constructor of the DbUser class.

-cheers

