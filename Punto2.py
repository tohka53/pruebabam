import mysql.connector
import pandas as pd
import logging
import sys

def execute_query(sql_file, db_dest, log_file):
    
    db_host = "localhost"
    db_user = "root"
    db_name = "prueba"
    db_port = 3306
        
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    try:
       
        with open(sql_file, 'r') as file:
            sql_query = file.read()
        
        logging.info("La consulta se ejecuto correctamente.")

      
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            database=db_name,
            port=db_port
        )
        logging.info(f"Conectado a la base de datos origen: {db_name}")

      
        df = pd.read_sql_query(sql_query, conn)
        logging.info("Query ejecutado correctamente.")
        
        
        conn_dest = mysql.connector.connect(
            host=db_host,
            user=db_user,
            database=db_name,
            port=db_port
        )
        cursor = conn_dest.cursor()
        
       
        table_name = db_dest
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join([f'{col} TEXT' for col in df.columns])}
        );
        """
        cursor.execute(create_table_query)
        logging.info(f"La tabla '{table_name}' se creo correctamente")

     
        for index, row in df.iterrows():
            placeholders = ', '.join(['%s'] * len(row))
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
            cursor.execute(insert_query, tuple(row))
        
        conn_dest.commit()
        logging.info("Se incertaron los datos de la consulta realizada")

    except Exception as e:
        logging.error(f"Error: {str(e)}")
    finally:
        conn.close()
        conn_dest.close()
        logging.info("END")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python script.py <sql_file> <db_dest> <log_file>")
    else:
        sql_file = sys.argv[1]
        db_dest = sys.argv[2]
        log_file = sys.argv[3]
        
        execute_query(sql_file, db_dest, log_file)
