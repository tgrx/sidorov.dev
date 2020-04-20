from django.contrib import admin
from django.contrib.admin import ModelAdmin

from applications.resume.models import Framework
from applications.resume.models import Organization
from applications.resume.models import Project
from project.utils.xforms import gen_textinput_admin_form
from project.utils.xmodels import a


@admin.register(Framework)
class TechnologyAdminModel(ModelAdmin):
    form = gen_textinput_admin_form(
        Framework, (a(_f) for _f in (Framework.name, Framework.link, Framework.version))
    )


@admin.register(Project)
class ProjectAdminModel(ModelAdmin):
    form = gen_textinput_admin_form(
        Project,
        (
            a(_f)
            for _f in (
                Project.link,
                Project.name,
                Project.nda_name,
                Project.nda_organization_name,
                Project.position,
            )
        ),
    )


@admin.register(Organization)
class ResponsibilityAdminModel(ModelAdmin):
    form = gen_textinput_admin_form(
        Project, (a(_f) for _f in (Organization.name, Organization.link))
    )
