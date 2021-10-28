"""
create table compra
date created: 2021-10-21 00:26:06.194530
"""


def upgrade(migrator):
    with migrator.create_table('compra') as table:
        table.primary_key('id_compra')
        table.foreign_key('TEXT', 'cliente_id', on_delete=None, on_update=None, references='usuario.username')
        table.int('total')
        table.date('fecha')


def downgrade(migrator):
    migrator.drop_table('compra')
