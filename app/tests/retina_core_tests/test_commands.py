import pytest
from io import StringIO
from django.core.management import call_command
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from guardian.core import ObjectPermissionChecker

from grandchallenge.retina_core.management.commands.setannotationpermissions import (
    ANNOTATION_CODENAMES,
    WARNING_TEXT,
    SUCCESS_TEXT,
)
from config.settings import PERMISSION_TYPES


@pytest.mark.django_db
class TestCommand:
    nr_of_mlps = len(ANNOTATION_CODENAMES) * len(PERMISSION_TYPES)
    nr_of_olps = 22 * len(
        PERMISSION_TYPES
    )  # 22 == nr of annotation models in AnnotationSet fixture

    def test_setannotationpermissions_no_annotations(self):
        out = StringIO()
        call_command("setannotationpermissions", stdout=out)
        output = out.getvalue()
        assert WARNING_TEXT.format(self.nr_of_mlps, "assigned") in output

    def test_setannotationpermissions_no_annotations_remove(self):
        out = StringIO()
        call_command("setannotationpermissions", remove=True, stdout=out)
        output = out.getvalue()
        assert WARNING_TEXT.format(self.nr_of_mlps, "removed") in output

    def test_setannotationpermissions_no_retina_grader_annotations(
        self, AnnotationSet
    ):
        out = StringIO()
        call_command("setannotationpermissions", stdout=out)
        output = out.getvalue()
        assert WARNING_TEXT.format(self.nr_of_mlps, "assigned") in output

    def test_setannotationpermissions(self, AnnotationSet):
        AnnotationSet.grader.groups.add(
            Group.objects.get(name=settings.RETINA_GRADERS_GROUP_NAME)
        )
        out = StringIO()
        call_command("setannotationpermissions", stdout=out)
        output = out.getvalue()
        assert (
            SUCCESS_TEXT.format(self.nr_of_mlps, self.nr_of_olps, "assigned")
            in output
        )

    def test_setannotationpermissions_remove(self, AnnotationSet):
        AnnotationSet.grader.groups.add(
            Group.objects.get(name=settings.RETINA_GRADERS_GROUP_NAME)
        )
        out = StringIO()
        call_command("setannotationpermissions", remove=True, stdout=out)
        output = out.getvalue()
        assert (
            SUCCESS_TEXT.format(self.nr_of_mlps, self.nr_of_olps, "removed")
            in output
        )

    def test_setannotationpermissions_sets_correct_permissions(
        self, AnnotationSet
    ):
        admins_group = Group.objects.get(
            name=settings.RETINA_ADMINS_GROUP_NAME
        )
        graders_group = Group.objects.get(
            name=settings.RETINA_GRADERS_GROUP_NAME
        )
        AnnotationSet.grader.groups.add(graders_group)
        call_command("setannotationpermissions")

        checker = ObjectPermissionChecker(AnnotationSet.grader)
        group_perms = Permission.objects.filter(
            group=admins_group
        ).values_list("codename", flat=True)

        for (annotation_model, annotation_codename) in ANNOTATION_CODENAMES:
            for annotation in annotation_model.objects.all():
                perms = checker.get_perms(annotation)
                for permission_type in PERMISSION_TYPES:
                    assert f"{permission_type}_{annotation_codename}" in perms

                for permission_type in PERMISSION_TYPES:
                    assert (
                        f"{permission_type}_{annotation_codename}"
                        in group_perms
                    )

    def test_setannotationpermissions_removes_correct_permissions(
        self, AnnotationSet
    ):
        admins_group = Group.objects.get(
            name=settings.RETINA_ADMINS_GROUP_NAME
        )
        graders_group = Group.objects.get(
            name=settings.RETINA_GRADERS_GROUP_NAME
        )
        AnnotationSet.grader.groups.add(graders_group)
        call_command("setannotationpermissions")

        call_command("setannotationpermissions", remove=True)

        checker = ObjectPermissionChecker(AnnotationSet.grader)
        group_perms = Permission.objects.filter(
            group=admins_group, content_type__app_label="annotations"
        ).values_list("codename", flat=True)
        assert len(group_perms) == 0

        for (annotation_model, annotation_codename) in ANNOTATION_CODENAMES:
            for annotation in annotation_model.objects.all():
                perms = checker.get_perms(annotation)
                assert len(perms) == 0
