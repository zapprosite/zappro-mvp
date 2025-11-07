"""add materials and documents tables

Revision ID: 50f65d6954fa
Revises: 5c4145c0ad90
Create Date: 2025-11-07 01:12:07.759598
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '50f65d6954fa'
down_revision = '5c4145c0ad90'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'materials',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('stock', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('supplier', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_materials_name', 'materials', ['name'], unique=False)
    op.create_index('ix_materials_project_id', 'materials', ['project_id'], unique=False)

    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=True),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_documents_project_id', 'documents', ['project_id'], unique=False)
    op.create_index('ix_documents_task_id', 'documents', ['task_id'], unique=False)
    op.create_index('ix_documents_type', 'documents', ['type'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_documents_type', table_name='documents')
    op.drop_index('ix_documents_task_id', table_name='documents')
    op.drop_index('ix_documents_project_id', table_name='documents')
    op.drop_table('documents')

    op.drop_index('ix_materials_project_id', table_name='materials')
    op.drop_index('ix_materials_name', table_name='materials')
    op.drop_table('materials')
