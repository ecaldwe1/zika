# Copyright (C) 2016, University of Notre Dame
# All rights reserved
from django.contrib.auth.models import User
from django.db import models


class Location(models.Model):
    """
    Represents location in the database
    """
    department = models.TextField(blank=True)
    department_code = models.TextField(blank=True)
    municipality = models.TextField(blank=True)
    municipality_code = models.TextField(blank=True)
    creation_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "location"
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        # get_latest_by specifies the default field to use in your model Manager's latest() and earliest() methods.
        get_latest_by = "creation_timestamp"
        managed = True  # Django manages the database table's lifecycle.
        ordering = ["department", "municipality"]  # The default ordering for the object, for use when obtaining lists of objects:

    def __str__(self):
        return "%s - %s" % (self.municipality, self.department)


class Simulation(models.Model):
    name = models.TextField()
    model_name = models.TextField(blank=True)
    disease = models.TextField(default="ZVD")
    date_output_generated = models.DateField(null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, related_name="simulations")
    data_file = models.FileField(upload_to="simulation_files")

    class Meta:
        db_table = "simulation"
        verbose_name = "Simulation"
        verbose_name_plural = "Simulation"
        # get_latest_by specifies the default field to use in your model Manager's latest() and earliest() methods.
        get_latest_by = "creation_timestamp"
        managed = True  # Django manages the database table's lifecycle.
        ordering = ["date_output_generated"]  # The default ordering for the object, for use when obtaining lists of objects:

    def __str__(self):
        return "%s" % self.name


class Data(models.Model):
    """ Simulation data """
    # ??? Do we even need that ???
    #  uuid - For compatibility with EpiJSON format
    uuid = models.TextField(blank=True)
    location = models.ForeignKey(Location)
    value_low = models.FloatField(null=False)
    value_mid = models.FloatField(null=True, blank=True)
    value_high = models.FloatField(null=True, blank=True)
    date = models.DateField(null=False)
    simulation = models.ForeignKey(Simulation, related_name="data")
    creation_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "data"
        verbose_name = "Data"
        verbose_name_plural = "Data"
        # get_latest_by specifies the default field to use in your model Manager's latest() and earliest() methods.
        get_latest_by = "date"
        managed = True  # Django manages the database table's lifecycle.
        ordering = ["date"]  # The default ordering for the object, for use when obtaining lists of objects:

    def __str__(self):
        return "%s" % self.value_mid