#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import time, uuid

from orm import Model, StringField, BooleanField, DoubleField, TextField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    __table__ = 'user'

    email = StringField(column_type='varchar(50)', primary_key=True)
    password = StringField(column_type='varchar(50)')
    nickname = StringField(column_type='varchar(50)')
    avatar = StringField(column_type='varchar(200)')
    introduction = TextField()
    city = StringField(column_type='varchar(50)')
    created_at = DoubleField(default=time.time)
    isadmin = BooleanField()
    enjoy_sugar = BooleanField()
    enjoy_milk = BooleanField()
    single_espresso = BooleanField()

class Cafe(Model):
    __table__ = 'cafe'

    email = StringField(column_type='varchar(50)', primary_key=True)
    password = StringField(column_type='varchar(50)')
    image = StringField(column_type='varchar(200)')
    name = StringField(column_type='varchar(50)')
    city = StringField(column_type='varchar(50)')
    address = StringField(column_type='varchar(200)')
    introduction = TextField()

class Activity(Model):
    __table__ = 'activity'

    idactivity = StringField(column_type='varchar(50)', primary_key=True, default=next_id)
    start_at = DoubleField()
    end_at = DoubleField()
    image = StringField(column_type='varchar(200)')
    name = StringField(column_type='varchar(50)')
    introduction = TextField()
    belong_to = StringField(column_type='varchar(50)')
    created_from = StringField(column_type='varchar(50)')
    address = StringField(column_type='varchar(200)')
    signup_start_at = DoubleField(default=time.time)
    signup_end_at = DoubleField()

class Course(Model):
    __table__ = 'course'

    idcourse = StringField(column_type='varchar(50)', primary_key=True, default=next_id)
    image = StringField(column_type='varchar(200)')
    name = TextField()
    author = StringField(column_type='varchar(50)')
    created_at = DoubleField(default=time.time)
    introduction = TextField()    
    video = StringField(column_type='varchar(200)')
    israwbest = BooleanField()

class Article(Model):
    __table__ = 'article'

    idarticle = StringField(column_type='varchar(50)', primary_key=True, default=next_id)
    image = StringField(column_type='varchar(200)')
    name = TextField()
    author = StringField(column_type='varchar(50)')
    created_at = DoubleField(default=time.time)
    content = StringField(column_type='varchar(200)')
    family = StringField(column_type='varchar(50)')
    isknowledge = BooleanField()
    isnote = BooleanField()
    isdemand = BooleanField()
    about_cafe = StringField(column_type='varchar(50)')
    about_course = StringField(column_type='varchar(50)')
    about_drink = BooleanField()

class CommentArticle(Model):
    __table__ = 'comment_article'

    idcomment_article = StringField(column_type='varchar(50)', primary_key=True, default=next_id)
    created_from = StringField(column_type='varchar(50)')
    reply_to = StringField(column_type='varchar(50)')
    created_at = DoubleField(default=time.time)
    content = TextField()
    about = StringField(column_type='varchar(50)')

class CollectArticle(Model):
    __table__ = 'collect_article'

    user = StringField(column_type='varchar(50)', primary_key=True)
    article = StringField(column_type='varchar(50)', primary_key=True)
    created_at = DoubleField(default=time.time)

class LikeArticle(Model):
    __table__ = 'like_article'

    user = StringField(column_type='varchar(50)', primary_key=True)
    article = StringField(column_type='varchar(50)', primary_key=True)
    created_at = DoubleField(default=time.time)

class Coffee(Model):
    __table__ = 'coffee'

    name = StringField(column_type='varchar(50)', primary_key=True)

class Follow(Model):
    __table__ = 'follow'

    fromwho = StringField(column_type='varchar(50)', primary_key=True)
    towho = StringField(column_type='varchar(50)', primary_key=True)
    created_at = DoubleField(default=time.time)

class HaveCoffee(Model):
    __table__ = 'have_coffee'

    cafe = StringField(column_type='varchar(50)', primary_key=True)
    coffee = StringField(column_type='varchar(50)', primary_key=True)

class Enjoy(Model):
    __table__ = 'enjoy'

    user = StringField(column_type='varchar(50)', primary_key=True)
    coffee = StringField(column_type='varchar(50)', primary_key=True)

class Join(Model):
    __table__ = 'join'

    user = StringField(column_type='varchar(50)', primary_key=True)
    activity = StringField(column_type='varchar(50)', primary_key=True)
    created_at = DoubleField(default=time.time)

class LikeCafe(Model):
    __table__ = 'like_cafe'

    user = StringField(column_type='varchar(50)', primary_key=True)
    cafe = StringField(column_type='varchar(50)', primary_key=True)
    created_at = DoubleField(default=time.time)

class CommentCafe(Model):
    __table__ = 'comment_cafe'

    idcomment_cafe = StringField(column_type='varchar(50)', primary_key=True, default=next_id)
    created_from = StringField(column_type='varchar(50)')
    reply_to = StringField(column_type='varchar(50)')
    created_at = DoubleField(default=time.time)
    content = TextField()
    about = StringField(column_type='varchar(50)')

class CollectCafe(Model):
    __table__ = 'collect_cafe'

    user = StringField(column_type='varchar(50)', primary_key=True)
    cafe = StringField(column_type='varchar(50)', primary_key=True)
    created_at = DoubleField(default=time.time)

class CollectActivity(Model):
    __table__ = 'collect_activity'

    user = StringField(column_type='varchar(50)', primary_key=True)
    activity = StringField(column_type='varchar(50)', primary_key=True)
    created_at = DoubleField(default=time.time)

class NoteTag(Model):
    __table__ = 'note_tag'

    name = StringField(column_type='varchar(50)', primary_key=True)

class HaveNoteTag(Model):
    __table__ = 'have_note_tag'

    note = StringField(column_type='varchar(50)', primary_key=True)
    tag = StringField(column_type='varchar(50)', primary_key=True)

class CourseTag(Model):
    __table__ = 'course_tag'

    name = StringField(column_type='varchar(50)', primary_key=True)

class HaveCourseTag(Model):
    __table__ = 'have_course_tag'

    course = StringField(column_type='varchar(50)', primary_key=True)
    tag = StringField(column_type='varchar(50)', primary_key=True)

class Read(Model):
    __table__ = 'read'

    user = StringField(column_type='varchar(50)', primary_key=True)
    article = StringField(column_type='varchar(50)', primary_key=True)

class Look(Model):
    __table__ = 'look'

    user = StringField(column_type='varchar(50)', primary_key=True)
    course = StringField(column_type='varchar(50)', primary_key=True)

class CommentCourse(Model):
    __table__ = 'comment_course'

    idcomment_course = StringField(column_type='varchar(50)', primary_key=True, default=next_id)
    created_from = StringField(column_type='varchar(50)')
    reply_to = StringField(column_type='varchar(50)')
    created_at = DoubleField(default=time.time)
    content = TextField()
    about = StringField(column_type='varchar(50)')

class CollectCourse(Model):
    __table__ = 'collect_course'

    user = StringField(column_type='varchar(50)', primary_key=True)
    course = StringField(column_type='varchar(50)', primary_key=True)
    created_at = DoubleField(default=time.time)

class LikeCourse(Model):
    __table__ = 'like_course'

    user = StringField(column_type='varchar(50)', primary_key=True)
    course = StringField(column_type='varchar(50)', primary_key=True)
    created_at = DoubleField(default=time.time)
