# -*- coding: utf-8 -*-
#
#   Copyright © 2011-2013 APINC Devel Team
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

import datetime
from dateutil.relativedelta import relativedelta
import crypt

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, UserManager, AbstractUser
from django.utils.translation import ugettext as _

#from apm.apps.utils import CONFIDENTIALITY_LEVELS, portal_website_confidential

ACTIVE = 6
INACTIVE = 2 


class PersonManager(UserManager):
    def get_sentinel_user(self):
        return Person.objects.get_or_create(username='deleted', first_name='Sentinel', last_name='User', is_active=False)[0]


class Person(AbstractUser):
    """The main class for a person"""
    # Inheriting from User
    SEX = (
           ('M', _('Male')),
           ('F', _('Female')),
           )

    # Extra civility
    maiden_name = models.CharField(verbose_name=_('maiden name'),
        max_length=100, blank=True, null=True)
    birth_date = models.DateField(verbose_name=_('Birth date'), blank=True,
        null=True)
    sex = models.CharField(verbose_name=_('sex'), max_length=1, choices=SEX)

    objects = PersonManager()

    class Meta:
        """person meta"""
        #db_table = 'auth_user' # nom de la table du modele standard auth.User
        verbose_name = _('person')
        #ordering = ['user__last_name', 'user__first_name']
        ordering = ['last_name', 'first_name']

    def __unicode__(self):
        """person unicode"""
        return unicode(self.get_full_name())

    def get_absolute_url(self):
        return reverse('apm.apps.members.views.details', args=[self.id])

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def set_password_hash(self, vhffs_hashed_passwd):
        self.password = vhffs_hashed_passwd

    def get_first_subscription_date(self):
        """Returns the oldest project creation date, none if no projects found"""
        projects = Project.objects.get_active_for(self)
        if projects:
            return projects[0].creation_date

        # log error
        return None


    def get_subscriptions(self):
        """
        /!\ local import to avoid recursive imports
        """
        from apm.apps.contributions.models import Contribution

        return Contribution.objects.filter(person=self).filter(type__extends_duration__gt=0)


    def pending_subscriptions(self):
        """
        /!\ local import to avoid recursive imports
        """
        from apm.apps.contributions.models import Contribution

        return Contribution.objects.filter(person=self).filter(
            validated=False).count() > 0

    def is_subscriber(self, date=None):
        """
        /!\ local import to avoid recursive imports
        """
        from apm.apps.contributions.models import Contribution

        if not date:
            date = datetime.date.today()

        result = False
        result = Contribution.objects.filter(person=self).filter(
            validated=True).exclude(start_date__gt=date).exclude(
            end_date__lt=date)
        return result

    def get_next_subscription_start_date(self):
        """
        /!\ local import to avoid recursive imports
        """
        from apm.apps.contributions.models import Contribution
        
        result = None

        if self.get_subscriptions().count() > 0:
            result = Contribution.objects.filter(person=self).order_by('-subscription_end_date')[0].subscription_end_date + relativedelta(days=+1)

        if self.get_first_subscription_date():
            result = self.get_first_subscription_date()

        return result


class Role(models.Model):
    
    name =  models.CharField(verbose_name=_('name'), max_length=100, unique=True)
    rank = models.IntegerField(verbose_name=_('default rank'))
    members = models.ManyToManyField(Person, through='MemberRole')

    def __unicode__(self):
        return self.name

    def add(self, member): #FIXME test unicite ?
        mr = MemberRole(role=self, user=member,
                start_date = datetime.date.today())
        mr.save()

    def remove(self, member): #FIXME test active_member ?
        member_role = memberRole.objects.get(role=self, member=member)
        member_role.end_date = datetime.date.today()
        member_role.save()


class MemberRoleManager(models.Manager):
    def get_active_members(self):
        from django.db.models import Q
        return self.filter(
            Q(start_date__lte=datetime.date.today()),
            (Q(end_date__gte=datetime.date.today()) | 
            Q(end_date__isnull=True)))
    
    #def all_members(self): #FIXME
    #    """all group members"""
    #    from django.db.models import Q
    #    return [ ms for ms in self.members.all() ]


class MemberRole(models.Model):
    """Store a role acted by a member"""

    role = models.ForeignKey(Role)
    member = models.ForeignKey(Person)

    start_date = models.DateField(verbose_name=_('start date'),
        default=datetime.date.today(), blank=True, null=True)
    end_date = models.DateField(verbose_name=_('end date'), blank=True,
        null=True)
    expiration_date = models.DateField(verbose_name=_('expiration date'),
        blank=True, null=True)

    objects = MemberRoleManager()

    def __unicode__(self):
        return "Role '%s' : Member '%s'" % (unicode(self.role), unicode(self.member))


class PersonPrivate(models.Model):
    """private data for a person"""

    person = models.OneToOneField(Person, verbose_name=_('person'), related_name="private")

    # Administration
    notes = models.TextField(verbose_name=_('Notes'), blank=True, null=True,
            default=_("Donnees privees accessibles seulement par les admins ou le secretariat apinc."))

    def __unicode__(self):
        """Person private unicode"""
        return unicode(self.person)

    class Meta:
        """Person Private meta"""
        verbose_name = _('Person Private Data')
        ordering = ['person']


@receiver(post_save, sender=Person)
def create_person_private(sender, instance, created, **kwargs):
    if created:
        person_private, created = PersonPrivate.objects.get_or_create(person=instance)


class ProjectManager(models.Manager):
    def get_active_for(self, person):
        return self.filter(owner=person).filter(status__exact=ACTIVE).order_by('creation_date')


class Project(models.Model):
    """Represents a vhffs group"""
    groupname = models.CharField(verbose_name=_('groupname'), max_length=50, unique=True)
    owner = models.ForeignKey(Person)
    creation_date = models.DateField(verbose_name=_('creation date'),
        null=True, blank=True)
    PROJECT_STATUS = (
        (ACTIVE, _('Active')),
        (INACTIVE, _('Inactive')),
    )
    status = models.IntegerField(choices=PROJECT_STATUS, default=ACTIVE)

    objects = ProjectManager()
