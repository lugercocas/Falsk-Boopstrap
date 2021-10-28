"""
create table producto
date created: 2021-10-21 00:26:06.193970
"""


def upgrade(migrator):
    with migrator.create_table('producto') as table:
        table.primary_key('id_producto')
        table.text('nombre_producto')
        table.int('precio')
        table.text('descripcion')
        table.text('descripcion_detallada')
        table.text('path_imagen')
        table.int('cantidad')
        table.text('unidad_medida')


def downgrade(migrator):
    migrator.drop_table('producto')
