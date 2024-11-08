from typing import Union
import random
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from tgbot.config import load_config

config = load_config(".env")


class Database:

    def init(self):
        self.pool: Union[Pool, None]

    async def create(self):
        self.pool = await asyncpg.create_pool(
            host=config.db.host,
            password=config.db.password,
            user=config.db.user,
            database=config.db.database
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_tovar_oplata(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS check_oplata(
        oplata_id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        tovar_id INT NOT NULL,
        amount INT,
        deliviry VARCHAR(100) NOT NULL,
        oplata_state INT,
        bill_id VARCHAR(255) UNIQUE
        )
        '''
        await self.execute(sql, execute=True)

    async def insert_in_tovar_oplata(self, user_id, tovar_id, amount, deliviry, oplata_state, bill_id):
        sql = '''
        INSERT INTO check_oplata(user_id, tovar_id, amount, deliviry, oplata_state, bill_id) VALUES($1, $2, $3, $4, $5, $6) returning *
                '''
        return await self.execute(sql, user_id, tovar_id, amount, deliviry, oplata_state, bill_id, fetchrow=True)

    async def update_price(self, bill_id):
        sql = 'UPDATE check_oplata SET oplata_state = 1 WHERE bill_id = $1'
        await self.execute(sql, bill_id, execute=True)

    async def check_bill_id(self, bill_id):
        sql = 'SELECT * FROM check_oplata WHERE bill_id = $1'
        return await self.execute(sql, bill_id, fetchrow=True)

    async def create_table_tovar(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS Katalog(
        tovar_id SERIAL PRIMARY KEY,
        img VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        price INT NOT NULL,
        amount INT NOT NULL,
        articul INT NOT NULL UNIQUE
        );
        '''
        await self.execute(sql, execute=True)

    async def amount_tovarov(self, tovar_id):
        sql = 'SELECT amount FROM katalog WHERE tovar_id = $1'
        return await self.execute(sql, tovar_id, fetchval=True)

    async def price_tovar_select(self, tovar_id):
        sql = 'SELECT price FROM katalog WHERE tovar_id = $1'
        return await self.execute(sql, tovar_id, fetchval=True)

    async def create_table_users_referal(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        priglos VARCHAR(255) NULL,
        referals INT DEFAULT 0,
        skidka INT DEFAULT 0
        );
        """
        await self.execute(sql, execute=True)

    async def add_tovar(self, img, name, description, price, amount, articul):
        sql = '''
        INSERT INTO katalog(img, name, description, price, amount, articul) VALUES($1, $2, $3, $4, $5, $6) returning *
        '''
        return await self.execute(sql, img, name, description, price, amount, articul, fetchrow=True)

    async def add_user(self, full_name, username, telegram_id, par):
        sql = '''
        INSERT INTO Users(full_name, username, telegram_id, priglos) VALUES($1, $2, $3, $4) returning *
        '''
        return await self.execute(sql, full_name, username, telegram_id, par, fetchrow=True)

    async def udoli_pls(self, articul):
        sql = 'DELETE FROM katalog WHERE articul = $1'
        return await self.execute(sql, articul, execute=True)

    async def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return await self.execute(sql, fetch=True)

    @staticmethod
    def format_args(sql, parametrs: dict):
        sql += ' AND '.join([
            f'{item} = ${num}' for num, item in enumerate(parametrs.keys(),
                                                          start=1)

        ])
        return sql, tuple(parametrs.values())

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parametrs = self.format_args(sql, parametrs=kwargs)
        return await self.execute(sql, *parametrs, fetchrow=True)

    async def count_users(self):
        sql = 'SELECT COUNT(*) FROM Users'
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = 'UPDATE Users SET username=$1 WHERE telegram_id = $2'
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute('DELETE FROM Users WHERE True', execute=True)

    async def drop_users(self):
        await self.execute('DROP TABLE Users', execute=True)

    async def args_id(self):
        sql = 'SELECT telegram_id FROM Users'
        return await self.execute(sql, fetch=True)

    async def count_referal(self, telegram_id):
        sql = 'UPDATE Users SET referals = referals + 1 WHERE telegram_id = $1'
        return await self.execute(sql, telegram_id, execute=True)

    async def count_skidka(self, telegram_id):
        sql = 'UPDATE Users SET skidka = skidka + 1 WHERE telegram_id = $1'
        return await self.execute(sql, telegram_id, execute=True)

    def gene_parol(self):
        pas = ''
        for x in range(7):  # Количество символов (16)
            pas = pas + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
        return pas

    async def priglos_id(self, telegram_id):
        sql = 'SELECT priglos FROM Users WHERE telegram_id = $1'
        return await self.execute(sql, telegram_id, fetchval=True)

    async def vse_paroli(self):
        sql = 'SELECT priglos FROM Users'
        return await self.execute(sql, fetch=True)

    async def count_referal2(self, priglos):
        sql = 'UPDATE Users SET referals = referals + 1 WHERE priglos = $1'
        return await self.execute(sql, priglos, execute=True)

    async def count_skidka2(self, priglos):
        sql = 'UPDATE Users SET skidka = skidka + 1 WHERE priglos = $1'
        return await self.execute(sql, priglos, execute=True)

    async def referalka1(self, telegram_id):
        sql = 'SELECT referals FROM Users WHERE telegram_id = $1'
        return await self.execute(sql, telegram_id, fetchval=True)

    async def referalka2(self, telegram_id):
        sql = 'SELECT skidka FROM Users WHERE telegram_id = $1'
        return await self.execute(sql, telegram_id, fetchval=True)

    async def pol_vse(self):
        sql = "SELECT * FROM katalog ORDER BY name;"
        return await self.execute(sql, fetch=True)

    async def select_name(self, text):
        sql = 'SELECT * FROM katalog WHERE name ILIKE $1 OR description ILIKE $1'
        return await self.execute(sql, text, fetch=True)

    async def pokasi_id(self):
        sql = 'SELECT tovar_id FROM katalog'
        return await self.execute(sql, fetch=True)

    async def photo_for_deep_link(self, tovar_id):
        sql = 'SELECT img FROM katalog WHERE tovar_id = $1'
        return await self.execute(sql, tovar_id, fetchval=True)

    async def articul_deep_link(self, tovar_id):
        sql = 'SELECT articul FROM katalog WHERE tovar_id = $1'
        return await self.execute(sql, tovar_id, fetchval=True)

    async def poluchit_vse_deep_link(self, tovar_id):
        sql = 'SELECT * FROM katalog WHERE tovar_id = $1'
        return await self.execute(sql, tovar_id, fetchrow=True)

    async def oplata_set_state(self, bill_id):
        sql = 'SELECT amount, tovar_id FROM check_oplata WHERE bill_id = $1'
        return await self.execute(sql, bill_id, fetchrow=True)

    async def update_amount_tovarov(self, amount, tovar_id):
        sql = 'UPDATE katalog SET amount = amount - $1 WHERE tovar_id = $2'
        await self.execute(sql, amount, tovar_id, execute=True)

    async def prosmot_tovar_bought(self, user_id):
        sql = '''SELECT name, check_oplata.amount FROM check_oplata INNER JOIN katalog ON katalog.tovar_id = 
        check_oplata.tovar_id WHERE user_id = $1 AND oplata_state = 1;'''
        return await self.execute(sql, user_id, fetch=True)

    async def poluchit_skidka(self, user_id):
        sql = 'SELECT skidka FROM Users WHERE telegram_id = $1'
        return await self.execute(sql, user_id, fetchval=True)

    async def ubrat_skidku(self, reset_sidka, user_id):
        sql = 'UPDATE Users SET skidka = $1 WHERE telegram_id = $2'
        await self.execute(sql, reset_sidka, user_id, execute=True)

    async def dobavit_skidku(self, user_id, skidka):
        sql = 'UPDATE Users SET skidka = $2 WHERE telegram_id = $1'
        await self.execute(sql, user_id, skidka, execute=True)

    async def skidka_show_true(self, parol):
        sql = 'SELECT True FROM Users WHERE priglos = $1'
        return await self.execute(sql, parol, fetchval=True)

    async def right_udoli(self, articul):
        sql = 'SELECT True FROM katalog WHERE articul = $1'
        return await self.execute(sql, articul, fetchval=True)

    async def poluchit_id_inline_mod(self, telegram_id):
        sql = 'SELECT True FROM Users WHERE telegram_id = $1'
        return await self.execute(sql, telegram_id, fetchval=True)

    async def poluchit_poshalusta_id_true(self, telegram_id):
        sql = 'SELECT True FROM Users WHERE telegram_id = $1'
        return await self.execute(sql, telegram_id, fetchval=True)

    async def upgrade_price_articul(self, price, articul):
        sql = 'UPDATE katalog SET price = $1 WHERE articul = $2'
        await self.execute(sql, price, articul, execute=True)

    async def help_me(self, articul):
        sql = "SELECT True FROM katalog WHERE articul = $1"
        return await self.execute(sql, articul, fetchval=True)

    async def update_amount_articul(self, amount, articul):
        sql = 'UPDATE katalog SET amount = $1 WHERE articul = $2'
        await self.execute(sql, amount, articul, execute=True)

    async def true_articul(self, articul):
        sql = 'SELECT True FROM katalog WHERE articul = $1'
        return await self.execute(sql, articul, fetchval=True)
