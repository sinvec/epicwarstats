"""

    EpicWarStore
    
    Класс, реализущий хранилище для карт

"""

class EpicWarStore:

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create_cursor(self):
        self.cursor = self.db_conn.cursor()

    def close_cursor(self):
        self.cursor.close()

    def create_table(self):

        self.create_cursor()

        self.cursor.execute('CREATE TABLE map( '
                                'id SERIAL PRIMARY KEY NOT NULL, '
                                'name VARCHAR(100), '
                                'author VARCHAR(50), '
                                'category VARCHAR(50), '
                                'tileset VARCHAR(20), '
                                'dims VARCHAR(9), '
                                'area VARCHAR(9), '
                                'players VARCHAR(20), '
                                'size DECIMAL(5, 2), '
                                'sub TIMESTAMP, '
                                'good INT, '
                                'bad INT, '
                                'downloads INT'
                            ')')
        
        self.close_cursor()
        self.db_conn.commit()
    
    def add_map(self, obj):

        for attr in ('category', 'tileset', 'dims', 'area', 
                'players'):
            if attr not in obj:
                obj[attr] = None

        self.cursor.execute('INSERT INTO map(id, name, author, '
                'category, tileset, dims, area, players, size, '
                'sub, good, bad, downloads) VALUES(%(id)s, '
                '%(name)s, %(author)s, %(category)s, %(tileset)s, '
                '%(dims)s, %(area)s, %(players)s, %(size)s, '
                '%(sub)s, %(good)s, %(bad)s, %(downloads)s)', obj)
        
        self.db_conn.commit()

    def is_exists(self, mid):
        self.cursor.execute('SELECT id FROM map WHERE id = %s', (mid,))
        if (len(self.cursor.fetchall()) > 0):
            return True
        else: 
            return False

    def delete_table(self):
        self.create_cursor()
        self.cursor.execute('DROP TABLE "map"')
        self.close_cursor()
        self.db_conn.commit()

    def clear_table(self):
        self.create_cursor()
        self.cursor.execute('DELETE FROM "map"')
        self.close_cursor()
        self.db_conn.commit()
    
    def get_last_id(self):
        self.cursor.execute('SELECT id FROM map ORDER BY id DESC LIMIT 1')
        return self.cursor.fetchone()[0]
        