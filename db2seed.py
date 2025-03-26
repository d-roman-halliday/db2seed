import os
import yaml
import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.sql.elements import quoted_name

def create_directory_if_not_exists(directory_path):
    """
    Creates a directory if it does not already exist.

    Args:
        directory_path (str): The path to the directory to create.
    """
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)  # Use makedirs to create nested directories
            print(f"Directory '{directory_path}' created successfully.")
        except OSError as e:
            print(f"Error creating directory '{directory_path}': {e}")

def convert_keys_to_strings(d):
    """
    Recursively convert dictionary keys to plain strings,
    fixing quoted_name issues (SQLAlchemy represents column names using quoted_name objects instead of plain strings).
    """
    if isinstance(d, dict):
        return {str(k) if isinstance(k, quoted_name) else k: convert_keys_to_strings(v) for k, v in d.items()}
    return d

# Load configuration from YAML file
def load_config(config_path='db_config.yml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Create a database connection
def get_db_engine(config):
    db_type = config['database']['type']
    user = config['database']['user']
    password = config['database']['password']
    host = config['database']['host']
    port = config['database']['port']
    db_name = config['database']['name']
    
    if db_type == 'sqlite':
        return create_engine(f'sqlite:///{db_name}')
    else:
        return create_engine(f'{db_type}://{user}:{password}@{host}:{port}/{db_name}')

# List tables in the database
def list_tables(engine):
    inspector = inspect(engine)
    return inspector.get_table_names()

# Export selected tables to CSV
def export_tables_to_csv(engine, tables, output_dir='output'):
    metadata = {}
    for table in tables:
        df = pd.read_sql_table(table, con=engine)
        df.to_csv(f'{output_dir}/{table}.csv', index=False)
        metadata[table] = infer_dbt_types(df)
    generate_dbt_yaml(metadata, output_dir)

# Infer dbt data types
def infer_dbt_types(df):
    dtype_mapping = {
        'int64': 'integer',
        'float64': 'float',
        'object': 'string',
        'bool': 'boolean',
        'datetime64[ns]': 'timestamp'
    }
    
    #for col, dtype in df.dtypes.items():
    #    print('col: {0}'.format(col))
    #    print('dt : {0}'.format(dtype))
    #    dtypemapped=dtype_mapping.get(str(dtype), 'string')
    #    print('dt : {0}'.format(dtypemapped))

    return {col: dtype_mapping.get(str(dtype), 'string') for col, dtype in df.dtypes.items()}

# Generate dbt seed configuration YAML
def generate_dbt_yaml(metadata, output_dir):
    # See: https://docs.getdbt.com/reference/seed-properties
    dbt_yaml = {'version': 2, 'seeds': []}
    for table, columns in metadata.items():
        dbt_yaml['seeds'].append({
            'name': table,
            'config': {
                    "column_types": convert_keys_to_strings(columns)
                }
            })
    with open(f'{output_dir}/seeds.yml', 'w') as file:
        yaml.dump(dbt_yaml, file, default_flow_style=False, sort_keys=False)

# Main script execution
if __name__ == '__main__':
    output_dir = 'output'

    config = load_config()
    engine = get_db_engine(config)
    tables = list_tables(engine)
    print("Available tables:", tables)
    selected_tables = input("Enter table names to export (comma separated): ").split(',')
    #selected_tables = 'customers,shopping_carts,shopping_cart_items,products'.split(',')
    create_directory_if_not_exists(output_dir)
    export_tables_to_csv(engine, [t.strip() for t in selected_tables], output_dir)
    print("CSV export and dbt seed YAML generation complete.")

