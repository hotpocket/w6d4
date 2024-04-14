import sqlite3

'''A class to demonstrate CRUD operations on freshly created sqlite3 database'''
class DbUser:

    '''Drop & recreate user table to ensure a blank slate on each instance of DbUser.
       This is not ideal for production code, but it's fine for a classroom exercise.'''
    def __init__(self):
        self.conn = sqlite3.connect('user_database.db')
        self.conn.row_factory = sqlite3.Row  # to return rows as dictionaries
        self.cursor = self.conn.cursor()
        self.cursor.execute('DROP TABLE IF EXISTS user')
        self.cursor.execute('''
            CREATE TABLE user (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL UNIQUE,
              email TEXT NOT NULL UNIQUE,
              password TEXT,
              age INTEGER,
              gender CHAR(1),
              address TEXT
            );
        ''')
        self.conn.commit()

    '''Insert a new user into the database. Return the id of the new user.'''
    def insert(self, name, email, password, age=None, gender=None, address=None):
        sql = 'INSERT INTO user (name, email, password, age, gender, address) VALUES (?, ?, ?, ?, ?, ?)'
        try:
            self.cursor.execute(sql, (name, email, password, age, gender, address))
            self.conn.commit()
            return {"id": self.cursor.lastrowid}
        except sqlite3.OperationalError as e:
            return f"Operational Error: {e}" # the query may not be valid sqlite syntax
        except sqlite3.IntegrityError as e:
            return f"Record Exists: {e}"
        except sqlite3.DatabaseError as e:
            return f"Unknown Database Error: {e}"
        except Exception as e:
            return f"Unknown Error: {e}"

    '''Select users from the database based on the given criteria. Return a list of dictionaries.'''
    def select(self, min_age=None, max_age=None, gender=None):
        sql = 'SELECT * FROM user'
        where = ''
        fields  = [min_age, max_age, gender]
        filters = ['age >= ?', 'age <= ?', 'gender = ?']
        for filter, field in zip(filters, fields):
            if field is not None:
                where += ' WHERE ' if where == '' else ' AND '
                where += filter
        sql += where
        # print(sql)
        self.cursor.execute(sql, fields)
        # convert sqlite3.Row object to list of dictionaries
        return [dict(r) for r in self.cursor.fetchall()]

    '''Update user information in the database. Return the number of rows affected.'''
    def update(self, email, age=None, gender=None, address=None):
        # len of field_values must match len of field_names
        field_values = [age, gender, address]
        field_names = ['age', 'gender', 'address']
        if all(f is None for f in field_values):
            return 0
        sql = 'UPDATE user SET '
        updateThese = [f for f in field_values if f is not None]
        sql += ', '.join([f'{k} = ?' for k in field_names if field_values.pop(0) is not None])
        sql += ' WHERE email = ?'
        affected_rows = self.cursor.execute(sql, updateThese + [email])
        self.conn.commit()
        return f"Updated {affected_rows.rowcount} row(s) for email: {email}"

    '''Delete users from the database based on the given criteria. Return the number of rows affected.'''
    def delete(self, gender=None):
        if gender is None or len(gender) != 1:
            return 0
        sql = 'DELETE FROM user WHERE gender = ?'
        affected_rows = self.cursor.execute(sql, (gender))
        self.conn.commit()
        return f"Deleted {affected_rows.rowcount} row(s)"

    '''Close the connection to the database when the object is deleted.'''
    def __del__(self):
        self.conn.close()
