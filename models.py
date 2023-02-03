from __future__ import unicode_literals

from django.db import models


table_preference = (("Family table", "Family table"),
                    ("Outdoor seating", "Outdoor seating"),
                    ("Table for two", "Table for two"),
                    ("Table on second floor(sea view)", "Table on second floor(sea view)"))

time_choices = (
    ("10:00", "10:00"),
    ("11:00", "11:00"),
    ("12:00", "12:00"),
    ("13:00", "13:00"),
    ("14:00", "14:00"),
    ("15:00", "15:00"),
    ("16:00", "16:00"),
    ("17:00", "17:00"),
    ("18:00", "18:00"),
    ("19:00", "19:00"),
    ("20:00", "20:00"),
    ("21:00", "21:00"),
    ("22:00", "22:00"),
    )


# Create your models here.
class Guest(models.Model):
    """ Customer information model """
    customer_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, default="")

    def __str__(self):
        # return the full name as this is easier for the admin to read
        return self.full_name


class Table(models.Model):
    """ Restaurant table model """
    table_id = models.AutoField(primary_key=True)
    table_name = models.CharField(
        max_length=10, default="New table", unique=True)
    max_no_people = models.IntegerField()

    def __str__(self):
        return self.table_name
jhjhj

class BookATable(models.Model):

    number_of_guests = models.IntegerField()
    restaurant = models.ForeignKey("restaurant", on_delete=models.PROTECT)
    time = models.DateTimeField()


class restaurant(models.Model):
    le_chere = models.CharField(max_length=20)
    table = models.ForeignKey("table", on_delete=models.PROTECT)


def __str__(self):
    return self.restaurant_name

