SELECT 'CREATE DATABASE wealth'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'wealth')\gexec

GRANT ALL PRIVILEGES ON DATABASE wealth TO postgres;