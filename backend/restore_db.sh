docker-compose exec db psql -U postgres -d template1 -c "CREATE DATABASE postgres;"
cat $1 | docker exec -i backend_db_1 psql -U postgres