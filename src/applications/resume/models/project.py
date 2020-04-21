from typing import Iterable

from django.db import models
from django.db.models import F

from project.utils.xdatetime import DateDelta
from project.utils.xdatetime import utcnow


class Project(models.Model):
    name = models.TextField()
    is_hidden = models.BooleanField(null=False, default=False, verbose_name="Hidden?")
    is_under_nda = models.BooleanField(
        null=False, default=False, verbose_name="Under NDA?"
    )
    nda_name = models.TextField(null=True, blank=True, verbose_name="Name under NDA")
    nda_organization_name = models.TextField(
        null=True, blank=True, verbose_name="Organization Name under NDA"
    )
    position = models.TextField(null=True, blank=True)
    started_at = models.DateField(default=utcnow)
    finished_at = models.DateField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    responsibilities_text = models.TextField(null=True, blank=True)
    achievements_text = models.TextField(null=True, blank=True)

    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="projects"
    )
    frameworks = models.ManyToManyField("Framework", related_name="projects")

    @property
    def actual_name(self):
        if self.is_under_nda:
            return self.nda_name or "(((NDA)))"
        return self.name

    @property
    def duration(self) -> DateDelta:
        delta = DateDelta.build(self.started_at, self.finished_at)
        return delta

    @property
    def on_air(self) -> bool:
        return not self.finished_at

    @property
    def achievements(self) -> Iterable[str]:
        return filter(
            bool, (_r.strip() for _r in (self.achievements_text or "").split("\n"))
        )

    @property
    def responsibilities(self) -> Iterable[str]:
        return filter(
            bool, (_r.strip() for _r in (self.responsibilities_text or "").split("\n"))
        )

    def __str__(self):
        return f"{self.name!r} @ {self.organization.name} ({self.pk})"

    class Meta:
        ordering = (
            F("finished_at").desc(nulls_last=False),
            "-started_at",
            "name",
        )
