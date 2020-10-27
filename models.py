# coding: utf-8
from sqlalchemy import ARRAY, BigInteger, Boolean, Column, Date, Float, ForeignKey, Integer, SmallInteger, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Cleaningredient(Base):
    __tablename__ = 'cleaningredients'

    cleaningredientid = Column(Integer, primary_key=True)
    name = Column(String(255))

    recipes = relationship('Recipe', secondary='recipeingredientjoin')


t_pg_buffercache = Table(
    'pg_buffercache', metadata,
    Column('bufferid', Integer),
    Column('relfilenode', OID),
    Column('reltablespace', OID),
    Column('reldatabase', OID),
    Column('relforknumber', SmallInteger),
    Column('relblocknumber', BigInteger),
    Column('isdirty', Boolean),
    Column('usagecount', SmallInteger),
    Column('pinning_backends', Integer)
)


t_pg_stat_statements = Table(
    'pg_stat_statements', metadata,
    Column('userid', OID),
    Column('dbid', OID),
    Column('queryid', BigInteger),
    Column('query', Text),
    Column('calls', BigInteger),
    Column('total_time', Float(53)),
    Column('min_time', Float(53)),
    Column('max_time', Float(53)),
    Column('mean_time', Float(53)),
    Column('stddev_time', Float(53)),
    Column('rows', BigInteger),
    Column('shared_blks_hit', BigInteger),
    Column('shared_blks_read', BigInteger),
    Column('shared_blks_dirtied', BigInteger),
    Column('shared_blks_written', BigInteger),
    Column('local_blks_hit', BigInteger),
    Column('local_blks_read', BigInteger),
    Column('local_blks_dirtied', BigInteger),
    Column('local_blks_written', BigInteger),
    Column('temp_blks_read', BigInteger),
    Column('temp_blks_written', BigInteger),
    Column('blk_read_time', Float(53)),
    Column('blk_write_time', Float(53))
)


class Rawingredient(Base):
    __tablename__ = 'rawingredients'

    rawingredientid = Column(Integer, primary_key=True)
    cleaningredientid = Column(Integer)
    rawname = Column(String(255))
    rawnamelength = Column(Integer)
    processedname = Column(String(255))
    processednamelength = Column(Integer)


class Recipe(Base):
    __tablename__ = 'recipes'

    recipeid = Column(Integer, primary_key=True)
    name = Column(String(255))
    minutes = Column(Integer)
    contributorid = Column(Integer)
    submitteddate = Column(Date)
    tagslist = Column(ARRAY(Text()))
    nutritionlist = Column(ARRAY(Float(precision=53)))
    numsteps = Column(Integer)
    stepslist = Column(ARRAY(Text()))
    description = Column(Text)
    ingredientnamelist = Column(ARRAY(Text()))
    numingredients = Column(Integer)
    i = Column(Float(53))
    nametokenlist = Column(ARRAY(Integer()))
    ingredienttokenlist = Column(Text)
    steptokenlist = Column(ARRAY(Integer()))
    techniquelist = Column(ARRAY(Integer()))
    calorielevel = Column(Float(53))
    ingredientidlist = Column(ARRAY(Integer()))
    iscomplete = Column(Boolean)
    calories = Column(Float(53))
    fatpdv = Column(Float(53))
    sugarpdv = Column(Float(53))
    sodiumpdv = Column(Float(53))
    proteinpdv = Column(Float(53))
    saturatedfatpdv = Column(Float(53))
    carbspdv = Column(Float(53))

    tags = relationship('Tag', secondary='recipetagjoin')


class Tag(Base):
    __tablename__ = 'tags'

    tagid = Column(Integer, primary_key=True)
    tag = Column(String(255))
    numrecipes = Column(Integer)


class User(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key=True)
    techniqueslist = Column(ARRAY(Integer()))
    itemslist = Column(ARRAY(Integer()))
    numitems = Column(Integer)
    ratingslist = Column(ARRAY(Float(precision=53)))
    numratings = Column(Integer)


class Interaction(Base):
    __tablename__ = 'interactions'

    interactionid = Column(Integer, primary_key=True)
    recipeid = Column(ForeignKey('recipes.recipeid'))
    userid = Column(Integer)
    date = Column(Date)
    rating = Column(Integer)
    review = Column(Text)

    recipe = relationship('Recipe')


t_recipeingredientjoin = Table(
    'recipeingredientjoin', metadata,
    Column('recipeid', ForeignKey('recipes.recipeid'), primary_key=True, nullable=False),
    Column('cleaningredientid', ForeignKey('cleaningredients.cleaningredientid'), primary_key=True, nullable=False)
)


t_recipetagjoin = Table(
    'recipetagjoin', metadata,
    Column('recipeid', ForeignKey('recipes.recipeid'), primary_key=True, nullable=False),
    Column('tagid', ForeignKey('tags.tagid'), primary_key=True, nullable=False)
)
