-- Taken from: https://github.com/d-roman-halliday/simple_shop_data_generator/blob/main/database_setup/database_and_users_postgres.sql

-- Create the database
CREATE DATABASE simple_shop;

-- Create users
CREATE USER simple_shop_admin   WITH ENCRYPTED PASSWORD 'admin_password';
CREATE USER simple_shop_updater WITH ENCRYPTED PASSWORD 'updater_password';
CREATE USER simple_shop_reader  WITH ENCRYPTED PASSWORD 'reader_password';


/******************************************************************************
Postgres 14 adds the predefined, non-login roles pg_read_all_data / pg_write_all_data.
They have SELECT / INSERT, UPDATE, DELETE privileges for all tables, views, and sequences. Plus USAGE on schemas. We can GRANT membership in these roles:
******************************************************************************/
-- Grant admin privileges
GRANT ALL PRIVILEGES ON DATABASE simple_shop TO simple_shop_admin;
-- Connect to the database
\c simple_shop;

GRANT ALL ON SCHEMA public TO simple_shop_admin;

-- Grant privileges for simple_shop_updater (modify data but no DDL)
GRANT CONNECT ON DATABASE simple_shop TO simple_shop_updater;
GRANT USAGE ON SCHEMA public TO simple_shop_updater;
GRANT pg_write_all_data TO simple_shop_updater;

-- Grant privileges for simple_shop_reader (read-only access)
GRANT CONNECT ON DATABASE simple_shop TO simple_shop_reader;
GRANT USAGE ON SCHEMA public TO simple_shop_reader;
GRANT pg_read_all_data TO simple_shop_reader;

