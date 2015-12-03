from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from tabulate import tabulate

NB = {'null': True, 'blank': True}


class PermissionQuerySet(models.QuerySet):
    def table(self):
        return tabulate([[
            perm.role, perm.agent, perm.target]
            for perm in self
        ])


class Permission(models.Model):
    role = models.CharField(max_length=255)

    agent_type = models.ForeignKey(
        ContentType,
        related_name='+',
        on_delete=models.PROTECT,
        **NB
    )
    agent_id = models.PositiveIntegerField(**NB)
    agent = GenericForeignKey('agent_type', 'agent_id')

    target_type = models.ForeignKey(
        ContentType,
        related_name='+',
        on_delete=models.PROTECT
    )
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_type', 'target_id')

    objects = PermissionQuerySet.as_manager()

    class Meta:
        unique_together = [
            'role',
            'agent_type',
            'agent_id',
            'target_type',
            'target_id'
        ]

    def __unicode__(self):
        return "%s %s" % (self.__class__.__name__, self.pk)
