from model import Model


if __name__ == '__main__':
    Model.set_db_fp('client.db')
    Model.create_db('res/create.sql')

