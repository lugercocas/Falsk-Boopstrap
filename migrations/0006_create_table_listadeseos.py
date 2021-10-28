"""
create table listadeseos
date created: 2021-10-21 00:26:06.195059
"""


def upgrade(migrator):
    with migrator.create_table('listadeseos') as table:
        table.primary_key('id')
        table.foreign_key('TEXT', 'usuario_id', on_delete=None, on_update=None, references='usuario.username')
        table.foreign_key('AUTO', 'producto_id', on_delete=None, on_update=None, references='producto.id_producto')


def downgrade(migrator):
    migrator.drop_table('listadeseos')
