# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FarmLevel(models.Model):
    level = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True, null=True)
    hidden = models.BooleanField()
    raid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'farm_level'


class Users(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    basic_password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    sex = models.CharField(max_length=255, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class UsersFb(models.Model):
    user = models.ForeignKey(Users, models.DO_NOTHING)
    pay_id = models.IntegerField()
    fb_id = models.CharField(max_length=255)
    fb_key = models.CharField(max_length=255)
    created = models.DateTimeField()
    used = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'users_fb'


class UsersFormscript(models.Model):
    user = models.ForeignKey(Users, models.DO_NOTHING)
    form_kind = models.IntegerField()
    fb_id = models.PositiveIntegerField()
    level = models.PositiveIntegerField()
    option = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    start = models.BooleanField()
    running = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'users_formscript'


class UsersPay(models.Model):
    user = models.ForeignKey(Users, models.DO_NOTHING)
    membership = models.IntegerField()
    amount = models.IntegerField()
    payed = models.DateTimeField()
    period = models.IntegerField()
    next_pay = models.DateTimeField()
    publish = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'users_pay'
