"""
create table usuario
date created: 2021-10-21 00:26:06.193698
"""


def upgrade(migrator):
    with migrator.create_table('usuario') as table:
        table.text('username')
        table.text('nombre')
        table.int('rol')
        table.text('direccion')
        table.text('telefono')
        table.text('clave')


def downgrade(migrator):
    migrator.drop_table('usuario')
