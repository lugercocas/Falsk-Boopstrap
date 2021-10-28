"""
create table detallecompra
date created: 2021-10-21 00:26:06.194836
"""


def upgrade(migrator):
    with migrator.create_table('detallecompra') as table:
        table.primary_key('id')
        table.foreign_key('AUTO', 'compra_id', on_delete=None, on_update=None, references='compra.id_compra')
        table.foreign_key('AUTO', 'producto_id', on_delete=None, on_update=None, references='producto.id_producto')
        table.int('costo')


def downgrade(migrator):
    migrator.drop_table('detallecompra')
