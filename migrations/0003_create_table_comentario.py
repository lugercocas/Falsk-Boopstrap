"""
create table comentario
date created: 2021-10-21 00:26:06.194248
"""


def upgrade(migrator):
    with migrator.create_table('comentario') as table:
        table.primary_key('id_comentario')
        table.foreign_key('TEXT', 'usuario_id', on_delete=None, on_update=None, references='usuario.username')
        table.foreign_key('AUTO', 'producto_id', on_delete=None, on_update=None, references='producto.id_producto')
        table.text('comentario')
        table.int('calificacion')


def downgrade(migrator):
    migrator.drop_table('comentario')
