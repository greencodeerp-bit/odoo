#!/usr/bin/env python3
"""Create Odoo database via XML-RPC with retries."""
import os
import time
import xmlrpc.client

DB_NAME = os.environ.get('DB_NAME', 'prod_db')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'admin123')
HOST = os.environ.get('HOST', 'http://localhost:8069')

def create_db():
    common = xmlrpc.client.ServerProxy(f"{HOST}/xmlrpc/2/common")
    db = xmlrpc.client.ServerProxy(f"{HOST}/xmlrpc/2/db")
    try:
        version = common.version()
        print('Connected to Odoo. Version:', version)
    except Exception as e:
        print('Cannot connect to Odoo:', e)
        return False

    # Check if DB exists
    try:
        db_list = db.list()
        if DB_NAME in db_list:
            print(f'Database {DB_NAME} already exists')
            return True
    except Exception:
        pass

    try:
        print(f'Creating database {DB_NAME}...')
        res = db.create_database(ADMIN_PASS, DB_NAME, False, None, None)
        print('create_database response:', res)
        return True
    except Exception as e:
        print('Failed to create database:', e)
        return False

if __name__ == '__main__':
    retries = 12
    for i in range(retries):
        if create_db():
            print('Done')
            exit(0)
        print('Retrying in 5s...')
        time.sleep(5)
    print('Giving up')
    exit(1)
