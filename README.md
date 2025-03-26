# db2seed
A simple python script to connect to a database and export tables as dbt seeds (including a ''properties.yml'' file). Initialy created using ChatGPT, then modified to fix bugs.

The intention is a simple way to export (and then be able to import using dbt) data. It's intended for moving sample data around between database environments/making sample data database agnostic.

Here's a Python script that:
1. Reads database connection details from a YAML config file.
2. Connects to the database using sqlalchemy.
3. Lists tables in the database.
4. Enables selection of individual tables.
5. Exports selected tables to CSV.
6. Generates a dbt seed configuration YAML file to define data types.

Only tested with PostgreSQL (should work with others), basic functionality.

# Notes & Testing

```
git clone git@github.com:d-roman-halliday/db2seed.git
cd db2seed/
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

```
python db2seed.py
```

## Testing generated data

```
(venv) david@osdse:~/db2seed_test$ dbt init

13:44:46  Running with dbt=1.9.3
13:44:46  [ConfigFolderDirectory]: Unable to parse logging event dictionary. Failed to parse dir field: expected string or bytes-like object, got 'PosixPath'.. Dictionary: {'dir': PosixPath('/home                                                         /david/.dbt')}
13:44:46  Creating dbt configuration folder at
Enter a name for your project (letters, digits, underscore): db2seed_test
13:45:12
Your new dbt project "db2seed_test" was created!

For more information on how to configure the profiles.yml file,
please consult the dbt documentation here:

  https://docs.getdbt.com/docs/configure-your-profile

One more thing:

Need help? Don't hesitate to reach out to us via GitHub issues or on Slack:

  https://community.getdbt.com/

Happy modeling!

13:45:12  Setting up your profile.
Which database would you like to use?
[1] duckdb

(Don't see the one you want? https://docs.getdbt.com/docs/available-adapters)

Enter a number: 1
13:45:16  Profile db2seed_test written to /home/david/.dbt/profiles.yml using target's sample configuration. Once updated, you'll be able to start developing with dbt.

(venv) david@osdse:~/db2seed_test$ ll

total 20
drwxrwxr-x  5 david david 4096 Mar 26 13:45 ./
drwxr-x--- 12 david david 4096 Mar 26 13:44 ../
drwxrwxr-x  8 david david 4096 Mar 26 13:44 db2seed_test/
drwxrwxr-x  2 david david 4096 Mar 26 13:44 logs/
drwxrwxr-x  5 david david 4096 Mar 26 13:43 venv/

(venv) david@osdse:~/db2seed_test$ cd db2seed_test/

(venv) david@osdse:~/db2seed_test/db2seed_test$ ll

total 44
drwxrwxr-x 8 david david 4096 Mar 26 13:44 ./
drwxrwxr-x 5 david david 4096 Mar 26 13:45 ../
-rw-rw-r-- 1 david david   29 Mar 26 13:44 .gitignore
-rw-rw-r-- 1 david david  571 Mar 26 13:44 README.md
drwxrwxr-x 2 david david 4096 Mar 26 13:44 analyses/
-rw-rw-r-- 1 david david 1250 Mar 26 13:45 dbt_project.yml
drwxrwxr-x 2 david david 4096 Mar 26 13:44 macros/
drwxrwxr-x 3 david david 4096 Mar 26 13:44 models/
drwxrwxr-x 2 david david 4096 Mar 26 13:44 seeds/
drwxrwxr-x 2 david david 4096 Mar 26 13:44 snapshots/
drwxrwxr-x 2 david david 4096 Mar 26 13:44 tests/

(venv) david@osdse:~/db2seed_test/db2seed_test$ cd seeds/

(venv) david@osdse:~/db2seed_test/db2seed_test/seeds$ ll

total 8
drwxrwxr-x 2 david david 4096 Mar 26 13:44 ./
drwxrwxr-x 8 david david 4096 Mar 26 13:44 ../
-rw-rw-r-- 1 david david    0 Mar 26 13:44 .gitkeep

(venv) david@osdse:~/db2seed_test/db2seed_test/seeds$ cp ../../../db2seed/output/* .

(venv) david@osdse:~/db2seed_test/db2seed_test/seeds$ ll

total 892
drwxrwxr-x 2 david david   4096 Mar 26 13:46 ./
drwxrwxr-x 8 david david   4096 Mar 26 13:44 ../
-rw-rw-r-- 1 david david      0 Mar 26 13:44 .gitkeep
-rw-rw-r-- 1 david david 389933 Mar 26 13:46 customers.csv
-rw-rw-r-- 1 david david  10726 Mar 26 13:46 products.csv
-rw-rw-r-- 1 david david    569 Mar 26 13:46 seeds.yml
-rw-rw-r-- 1 david david 208105 Mar 26 13:46 shopping_cart_items.csv
-rw-rw-r-- 1 david david 285283 Mar 26 13:46 shopping_carts.csv

(venv) david@osdse:~/db2seed_test/db2seed_test/seeds$ cd ..

(venv) david@osdse:~/db2seed_test/db2seed_test$ dbt seed

13:46:21  Running with dbt=1.9.3
13:46:22  Registered adapter: duckdb=1.9.2
13:46:22  Unable to do partial parsing because saved manifest not found. Starting full parse.
13:46:24  Found 2 models, 4 seeds, 4 data tests, 426 macros
13:46:24
13:46:24  Concurrency: 1 threads (target='dev')
13:46:24
13:46:24  1 of 4 START seed file main.customers .......................................... [RUN]
13:46:24  1 of 4 OK loaded seed file main.customers ...................................... [INSERT 6600 in 0.15s]
13:46:24  2 of 4 START seed file main.products ........................................... [RUN]
13:46:24  2 of 4 OK loaded seed file main.products ....................................... [INSERT 200 in 0.02s]
13:46:24  3 of 4 START seed file main.shopping_cart_items ................................ [RUN]
13:46:24  3 of 4 OK loaded seed file main.shopping_cart_items ............................ [INSERT 13521 in 0.09s]
13:46:24  4 of 4 START seed file main.shopping_carts ..................................... [RUN]
13:46:24  4 of 4 OK loaded seed file main.shopping_carts ................................. [INSERT 4505 in 0.27s]
13:46:24
13:46:24  Finished running 4 seeds in 0 hours 0 minutes and 0.70 seconds (0.70s).
13:46:24
13:46:24  Completed successfully
13:46:24
13:46:24  Done. PASS=4 WARN=0 ERROR=0 SKIP=0 TOTAL=4



(venv) david@osdse:~/db2seed_test/db2seed_test$ duckcli dev.duckdb


Version: 0.2.1
GitHub: https://github.com/dbcli/duckcli

dev.duckdb> .tables
+---------------------+
| table_name          |
+---------------------+
| customers           |
| products            |
| shopping_carts      |
| shopping_cart_items |
+---------------------+
Time: 0.014s

dev.duckdb> DESCRIBE products;
+-------------+-------------+------+--------+---------+--------+
| column_name | column_type | null | key    | default | extra  |
+-------------+-------------+------+--------+---------+--------+
| id          | INTEGER     | YES  | <null> | <null>  | <null> |
| name        | VARCHAR     | YES  | <null> | <null>  | <null> |
| description | VARCHAR     | YES  | <null> | <null>  | <null> |
| price       | FLOAT       | YES  | <null> | <null>  | <null> |
+-------------+-------------+------+--------+---------+--------+
4 rows in set
Time: 0.010s

dev.duckdb> SELECT * FROM products LIMIT 10;
+----+-----------+--------------------------------------------------------+--------------------+
| id | name      | description                                            | price              |
+----+-----------+--------------------------------------------------------+--------------------+
| 1  | important | Success book ready image success.                      | 109.80999755859375 |
| 2  | wear      | Education technology dream fact affect teach work.     | 255.50999450683594 |
| 3  | develop   | Morning present very avoid.                            | 114.38999938964844 |
| 4  | room      | Effect Mrs special operation reach.                    | 323.8599853515625  |
| 5  | establish | A oil Mrs question price read middle.                  | 93.31999969482422  |
| 6  | here      | Thousand hope carry image house indeed citizen future. | 222.3000030517578  |
| 7  | second    | Some experience true at hot.                           | 153.13999938964844 |
| 8  | art       | Rather fact nearly.                                    | 94.30000305175781  |
| 9  | pretty    | Personal writer value song front close.                | 109.73999786376953 |
| 10 | company   | Recent choose before trade fine say main.              | 53.869998931884766 |
+----+-----------+--------------------------------------------------------+--------------------+
10 rows in set
Time: 0.006s
```
