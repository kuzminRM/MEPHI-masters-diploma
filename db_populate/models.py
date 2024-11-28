from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Double, ForeignKeyConstraint, Identity, Index, PrimaryKeyConstraint, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Product(Base):
    __tablename__ = 'django_mapper_product'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='mapper_product_pkey'),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    uid = mapped_column(String(200), nullable=False)
    store = mapped_column(String(200), nullable=False)
    title = mapped_column(String(200), nullable=False)
    url = mapped_column(String(200), nullable=False)
    category = mapped_column(String(200), nullable=False)
    images = mapped_column(JSONB, nullable=False)
    price = mapped_column(Double(53), nullable=False)
    properties_as_text = mapped_column(Text, nullable=False)
    properties_art_codes = mapped_column(JSONB, nullable=False)
    properties_category_list_raw = mapped_column(JSONB, nullable=False)
    description = mapped_column(Text)
    images_0 = mapped_column(String(200))
    images_1 = mapped_column(String(200))
    images_2 = mapped_column(String(200))
    images_3 = mapped_column(String(200))
    images_4 = mapped_column(String(200))
    images_5 = mapped_column(String(200))
    properties_as_dict = mapped_column(JSONB)
    properties_brand = mapped_column(String(200))
    properties_label = mapped_column(String(200))
    properties_country = mapped_column(String(200))
    properties_color = mapped_column(String(200))
    properties_material = mapped_column(String(200))
    properties_mass_raw = mapped_column(String(200))
    properties_mass_num = mapped_column(Double(53))
    properties_mass_unit = mapped_column(String(200))
    properties_volume_raw = mapped_column(String(200))
    properties_volume_num = mapped_column(Double(53))
    properties_volume_unit = mapped_column(String(200))
    properties_dimensions_raw = mapped_column(String(200))
    properties_dimensions_d_list = mapped_column(JSONB)
    properties_dimensions_d_list_0 = mapped_column(Double(53))
    properties_dimensions_d_list_1 = mapped_column(Double(53))
    properties_dimensions_d_list_2 = mapped_column(Double(53))
    properties_dimensions_d_list_3 = mapped_column(Double(53))
    properties_dimensions_d_list_4 = mapped_column(Double(53))
    properties_dimensions_d_list_5 = mapped_column(Double(53))
    properties_dimensions_all_units_parsed = mapped_column(Boolean)
    properties_art_codes_0 = mapped_column(String(200))
    properties_art_codes_1 = mapped_column(String(200))
    properties_art_codes_2 = mapped_column(String(200))
    properties_art_codes_3 = mapped_column(String(200))
    properties_art_codes_4 = mapped_column(String(200))
    properties_art_codes_5 = mapped_column(String(200))
    properties_category_list_raw_0 = mapped_column(String(200))
    properties_category_list_raw_1 = mapped_column(String(200))
    properties_category_list_raw_2 = mapped_column(String(200))
    properties_category_list_raw_3 = mapped_column(String(200))
    properties_category_list_raw_4 = mapped_column(String(200))
    properties_category_list_raw_5 = mapped_column(String(200))

    django_mapper_match: Mapped[List['Match']] = relationship('Match', uselist=True, foreign_keys='[Match.product_1_id]', back_populates='product_1')
    django_mapper_match_: Mapped[List['Match']] = relationship('Match', uselist=True, foreign_keys='[Match.product_2_id]', back_populates='product_2')
    django_mapper_match_llm: Mapped[List['Match']] = relationship('MatchLLM', uselist=True, foreign_keys='[MatchLLM.product_1_id]', back_populates='product_1')
    django_mapper_match_llm_: Mapped[List['Match']] = relationship('MatchLLM', uselist=True, foreign_keys='[MatchLLM.product_2_id]', back_populates='product_2')


class Match(Base):
    __tablename__ = 'django_mapper_match'
    __table_args__ = (
        ForeignKeyConstraint(['product_1_id'], ['django_mapper_product.id'], deferrable=True, initially='DEFERRED', name='django_mapper_match_product_1_id_ca3f4a54_fk_django_ma'),
        ForeignKeyConstraint(['product_2_id'], ['django_mapper_product.id'], deferrable=True, initially='DEFERRED', name='django_mapper_match_product_2_id_51c9412b_fk_django_ma'),
        PrimaryKeyConstraint('id', name='django_mapper_match_pkey'),
        Index('django_mapper_match_product_1_id_ca3f4a54', 'product_1_id'),
        Index('django_mapper_match_product_2_id_51c9412b', 'product_2_id')
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    insurance = mapped_column(Double(53), nullable=False)
    updated_at = mapped_column(DateTime(True), nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False)
    product_1_id = mapped_column(BigInteger, nullable=False)
    product_2_id = mapped_column(BigInteger)

    product_1: Mapped['Product'] = relationship('Product', foreign_keys=[product_1_id], back_populates='django_mapper_match')
    product_2: Mapped[Optional['Product']] = relationship('Product', foreign_keys=[product_2_id], back_populates='django_mapper_match_')


class MatchLLM(Base):
    __tablename__ = 'django_mapper_matchllm'
    __table_args__ = (
        ForeignKeyConstraint(['product_1_id'], ['django_mapper_product.id'], deferrable=True, initially='DEFERRED', name='django_mapper_match_product_1_id_ca3f4a54_fk_django_ma'),
        ForeignKeyConstraint(['product_2_id'], ['django_mapper_product.id'], deferrable=True, initially='DEFERRED', name='django_mapper_match_product_2_id_51c9412b_fk_django_ma'),
        PrimaryKeyConstraint('id', name='django_mapper_match_pkey'),
        Index('django_mapper_match_product_1_id_ca3f4a54', 'product_1_id'),
        Index('django_mapper_match_product_2_id_51c9412b', 'product_2_id')
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    llm_map = mapped_column(Boolean, nullable=True)
    llm_insurance = mapped_column(BigInteger, nullable=True)
    llm_raw = mapped_column(String(20), nullable=True)
    updated_at = mapped_column(DateTime(True), nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False)
    product_1_id = mapped_column(BigInteger, nullable=False)
    product_2_id = mapped_column(BigInteger)

    product_1: Mapped['Product'] = relationship('Product', foreign_keys=[product_1_id], back_populates='django_mapper_match_llm')
    product_2: Mapped[Optional['Product']] = relationship('Product', foreign_keys=[product_2_id], back_populates='django_mapper_match_llm_')
