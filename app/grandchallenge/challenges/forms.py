from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    HTML,
    ButtonHolder,
    Div,
    Fieldset,
    Layout,
    Submit,
)
from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.text import format_lazy
from django_select2.forms import Select2MultipleWidget
from django_summernote.widgets import SummernoteInplaceWidget

from grandchallenge.challenges.models import (
    Challenge,
    ChallengeRequest,
    ExternalChallenge,
)
from grandchallenge.challenges.utils import ChallengeTypeChoices
from grandchallenge.subdomains.utils import reverse_lazy

common_information_items = (
    "title",
    "description",
    "task_types",
    "modalities",
    "structures",
    "organizations",
    "series",
    "publications",
    "hidden",
    "educational",
)

common_images_items = ("logo", "social_image")

event_items = ("event_url", "workshop_date")

registration_items = (
    "use_registration_page",
    "access_request_handling",
    "registration_page_text",
)


class ChallengeUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    "Information",
                    *common_information_items,
                    "display_forum_link",
                    "disclaimer",
                    "contact_email",
                ),
                Tab("Images", "banner", *common_images_items),
                Tab("Event", *event_items),
                Tab("Registration", *registration_items),
                Tab("Teams", "use_teams"),
            ),
            ButtonHolder(Submit("save", "Save")),
        )

    class Meta:
        model = Challenge
        fields = [
            *common_information_items,
            "display_forum_link",
            "disclaimer",
            "contact_email",
            "banner",
            *common_images_items,
            *event_items,
            *registration_items,
            "use_teams",
        ]
        widgets = {
            "workshop_date": forms.TextInput(attrs={"type": "date"}),
            "task_types": Select2MultipleWidget,
            "modalities": Select2MultipleWidget,
            "structures": Select2MultipleWidget,
            "organizations": Select2MultipleWidget,
            "series": Select2MultipleWidget,
            "publications": Select2MultipleWidget,
            "registration_page_text": SummernoteInplaceWidget(),
        }
        help_texts = {
            "publications": format_lazy(
                (
                    "The publications associated with this archive. "
                    'If your publication is missing click <a href="{}">here</a> to add it '
                    "and then refresh this page."
                ),
                reverse_lazy("publications:create"),
            )
        }

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data["hidden"] and not cleaned_data.get("logo"):
            raise ValidationError("A logo is required for public challenges")

        if not cleaned_data["hidden"] and not cleaned_data.get(
            "contact_email"
        ):
            raise ValidationError("A contact email is required")

        return cleaned_data


data_items = (
    "data_license_agreement",
    "data_stored",
    "number_of_training_cases",
    "number_of_test_cases",
)


class ExternalChallengeUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    "Information",
                    "short_name",
                    "homepage",
                    *common_information_items,
                ),
                Tab("Images", *common_images_items),
                Tab("Event", *event_items),
                Tab("Data", *data_items),
            ),
            ButtonHolder(Submit("save", "Save")),
        )

    class Meta:
        model = ExternalChallenge
        fields = (
            "short_name",
            "homepage",
            *common_information_items,
            *common_images_items,
            *event_items,
            *data_items,
        )
        widgets = {
            "workshop_date": forms.TextInput(attrs={"type": "date"}),
            "description": forms.Textarea,
            "task_types": Select2MultipleWidget,
            "modalities": Select2MultipleWidget,
            "structures": Select2MultipleWidget,
            "organizations": Select2MultipleWidget,
            "series": Select2MultipleWidget,
            "publications": Select2MultipleWidget,
        }
        help_texts = {
            "publications": format_lazy(
                (
                    "The publications associated with this archive. "
                    'If your publication is missing click <a href="{}">here</a> to add it '
                    "and then refresh this page."
                ),
                reverse_lazy("publications:create"),
            )
        }


class ChallengeRequestBudgetFieldValidationMixin:
    def clean(self):
        cleaned_data = super().clean()
        challenge_type = (
            cleaned_data["challenge_type"]
            if "challenge_type" in cleaned_data
            else self.instance.challenge_type
        )
        if challenge_type == ChallengeTypeChoices.T2:
            if not cleaned_data["average_size_of_test_image_in_mb"]:
                raise ValidationError(
                    "For a type 2 challenge, you need to provide the average "
                    "test image size."
                )
            if not cleaned_data["inference_time_limit_in_minutes"]:
                raise ValidationError(
                    "For a type 2 challenge, you need to provide an inference "
                    "time limit."
                )
            if (
                cleaned_data["phase_1_number_of_submissions_per_team"] is None
                or cleaned_data["phase_2_number_of_submissions_per_team"]
                is None
            ):
                raise ValidationError(
                    "For a type 2 challenge, you need to provide the number of "
                    "submissions per team for each phase. Enter 0 for phase 2 "
                    "if you only have 1 phase."
                )
            if (
                cleaned_data["phase_1_number_of_test_images"] is None
                or cleaned_data["phase_2_number_of_test_images"] is None
            ):
                raise ValidationError(
                    "For a type 2 challenge, You need to provide the number of "
                    "test images for each phase. Enter 0 for phase 2 if you "
                    "only have 1 phase."
                )
        return cleaned_data


general_information_items_1 = (
    "title",
    "short_name",
    "contact_email",
    "abstract",
    "start_date",
    "end_date",
    "long_term_commitment",
    "long_term_commitment_extra",
    "organizers",
    "affiliated_event",
)
general_information_items_2 = (
    "task_types",
    "structures",
    "modalities",
    "challenge_type",
    "challenge_setup",
    "data_set",
    "data_license",
    "data_license_extra",
    "submission_assessment",
    "challenge_publication",
    "code_availability",
    "expected_number_of_teams",
)
phase_1_items = (
    "phase_1_number_of_submissions_per_team",
    "phase_1_number_of_test_images",
)
phase_2_items = (
    "phase_2_number_of_submissions_per_team",
    "phase_2_number_of_test_images",
)
structured_challenge_submission_help_text = (
    "If you have uploaded a PDF or "
    "provided the DOI for your structured "
    "challenge submission form above, "
    "you can enter 'See structured submission form' here."
)


class ChallengeRequestForm(
    ChallengeRequestBudgetFieldValidationMixin, forms.ModelForm
):
    class Meta:
        model = ChallengeRequest
        fields = (
            *general_information_items_1,
            "structured_challenge_submission_form",
            "structured_challenge_submission_doi",
            *general_information_items_2,
            "number_of_tasks",
            "average_size_of_test_image_in_mb",
            "inference_time_limit_in_minutes",
            "budget_for_hosting_challenge",
            "algorithm_inputs",
            "algorithm_outputs",
            *phase_1_items,
            *phase_2_items,
            "comments",
        )
        widgets = {
            "start_date": forms.TextInput(attrs={"type": "date"}),
            "end_date": forms.TextInput(attrs={"type": "date"}),
            "challenge_type": forms.Select(
                attrs={"onchange": "updateBudgetFields();"}
            ),
            "long_term_commitment": forms.CheckboxInput(
                attrs={
                    "onchange": "updateExtraField('long_term_commitment', 'support this challenge long-term');"
                }
            ),
            "data_license": forms.CheckboxInput(
                attrs={
                    "onchange": "updateExtraField('data_license', 'use a CC-BY license for your data');"
                }
            ),
        }
        labels = {
            "short_name": "Acronym",
            "long_term_commitment": "We agree to support this challenge for up to 5 years. ",
            "data_license": "We agree to publish the data set for this challenge under a CC-BY license.",
            "phase_1_number_of_submissions_per_team": "Expected number of submissions per team to Phase 1",
            "phase_2_number_of_submissions_per_team": "Expected number of submissions per team to Phase 2",
            "budget_for_hosting_challenge": "Budget for hosting challenge in Euros",
            "inference_time_limit_in_minutes": "Average algorithm job run time in minutes",
            "structured_challenge_submission_doi": "DOI",
            "structured_challenge_submission_form": "PDF",
        }
        help_texts = {
            "title": "The name of the planned challenge.",
            "short_name": (
                "Acronym of your challenge title that will be used in the URL "
                "(e.g., https://{acronym}.grand-challenge.org/), specific css "
                "and files if the challenge is accepted. No spaces and special "
                "characters allowed. We prefer a single word with two digits at "
                "the end indicating the year (e.g. LUNA16). See "
                "<a href='https://www.grand-challenge.org/challenges' "
                "target='_blank'>other challenges</a> for examples."
            ),
            "abstract": (
                "Provide a summary of the challenge purpose. "
                "This should include a general introduction to the "
                "topic from both a biomedical as well as from a technical point of "
                "view. From a biomedical point of view, please elaborate on the "
                "specific task at hand, how the task is currently performed "
                "(i.e., manual vs (semi-)automatic) and how an algorithm may improve "
                "this task. From a technical point of view, please mention "
                "how current state-of-the-art algorithms perform on this task "
                "(e.g., dice coefficient for segmentation tasks) and under which "
                "circumstances this performance was achieved (i.e., dataset size, "
                "modality, etc.). Finally, we kindly ask you to clearly state the "
                "envisioned technical and/or biomedical impact of the challenge."
            ),
            "challenge_type": (
                "<b>Type 1 :</b> Prediction submission - "
                "test data are open, participants run their algorithms locally "
                "and submit their predictions on the website which are evaluated "
                "against a secret ground truth on our servers.<br>"
                "<b>Type 2:</b> Docker container submission – test data are "
                "secret, participants submit algorithms as docker "
                "containers on our website, which are run on the secret test set on "
                "our servers and then evaluated against a secret ground "
                "truth. <br>"
                "<b>We strongly encourage Type 2 challenges.</b> "
                "Please read our <a href="
                "'https://grand-challenge.org/documentation/challenges/' "
                "target='_blank'> challenge documentation</a> before making your "
                "choice."
            ),
            "code_availability": (
                "Will the participants’ code be accessible after "
                "the challenge? <br>We strongly encourage open science. For Type "
                "2 challenges, algorithms will be stored on Grand Challenge and "
                "we encourage organizers to incentivize an open source policy, "
                "for example by asking participants to publish their Github repo "
                "under an <a href='https://docs.github.com/en/repositories/managing-"
                "your-repositorys-settings-and-features/customizing-your-repository/"
                "licensing-a-repository' target='_blank'> open source license</a> "
                "(e.g., Apache 2.0, MIT) and <a href='https://grand-challenge.org/"
                "documentation/linking-a-github-repository-to-your-algorithm/'>"
                "link it to their algorithm</a> on Grand Challenge."
            ),
            "data_set": (
                f"{structured_challenge_submission_help_text} Otherwise, please "
                f"describe the training and test datasets you are planning to "
                f"use. <br>For Type 1 challenges, indicate where "
                f"you will store the data (read about the options <a href="
                f"'https://grand-challenge.org/documentation/data-storage/' "
                f"target='_blank'>here</a>).<br>For Type 2 challenges, the test "
                f"dataset will need to be uploaded to Grand Challenge (read more "
                f"about that <a href='https://grand-challenge.org/documentation/"
                f"data-storage-2/' target='_blank'>here</a>)."
            ),
            "number_of_tasks": (
                "If your challenge has multiple tasks, we multiply"
                "the phase 1 and 2 cost estimates by the number of tasks. "
                "For that to work, please provide the average number of "
                "test images and the average number of submissions across "
                "tasks for the two phases below. For examples check "
                "<a href='https://grand-challenge.org/documentation/"
                "create-your-own-challenge/'>here</a>."
            ),
            "challenge_setup": (
                "Describe the challenge set-up. How many tasks "
                "and <a href='https://www.grand-challenge.org/documentation/"
                "multiple-phases-multiple-leaderboards/' target='_blank'>phases</a>"
                " does the challenge have?"
            ),
            "inference_time_limit_in_minutes": (
                "The average time that you expect an algorithm job to take in minutes. "
                "This time estimate should account for everything that needs to happen "
                "for an algorithm container to process <u>one single image, including "
                "model loading, i/o, preprocessing and inference.</u>"
            ),
            "long_term_commitment": (
                "High-quality challenges typically remain relevant for years. "
                "Only when the submitted results to a challenge are hard to improve "
                "upon, or when a new challenge has been set up for a similar task "
                "that is more attractive to the research community, may it make sense "
                "to close a challenge. We have designed grand-challenge.org to keep "
                "algorithms and challenges long-term available. We expect the life "
                "cycle of a challenge to last between 3-5 years. Would you be willing "
                "to commit support for such a period? The amount of work would be "
                "minimal, but it would require that the organizing team remains "
                "responsive, and answers questions and queries in the forum. "
            ),
            "data_license": (
                "In the spirit of open science, we ask that the <b>public training "
                "data</b> for type 1 and type 2 challenges are released under a "
                "<a href='https://creativecommons.org/licenses/' target='_blank'>"
                "CC-BY license</a>. Note that this does not apply to the secret test "
                "data used to evaluate algorithm submissions in Type 2 challenges."
            ),
            "phase_1_number_of_test_images": (
                "Number of test images for this phase. If you're <a href="
                "'https://grand-challenge.org/documentation/create-your-own-challenge/#budget-batched-images'>"
                "bundling images</a>, enter the number of batches (not the number of single images)."
            ),
            "phase_2_number_of_test_images": (
                "Number of test images for this phase. If you're <a href="
                "'https://grand-challenge.org/documentation/create-your-own-challenge/#budget-batched-images'>"
                "bundling images</a>, enter the number of batches (not the number of single images)."
            ),
            "average_size_of_test_image_in_mb": (
                "Average size of test image in MB. If you're <a href="
                "'https://grand-challenge.org/documentation/create-your-own-challenge/#budget-batched-images'>"
                "bundling images</a>, provide the size of the batch (not the size of a single image)."
            ),
            "phase_1_number_of_submissions_per_team": (
                "How many submissions do you expect per team to this phase? "
                "You can enforce a submission limit in the settings for each phase "
                "to control this."
            ),
            "phase_2_number_of_submissions_per_team": (
                "How many submissions do you expect per team to this phase? "
                "You can enforce a submission limit in the settings for each phase "
                "to control this."
            ),
            "submission_assessment": (
                f"{structured_challenge_submission_help_text} Otherwise, "
                f"please define the metrics you will use "
                "to assess and rank participants’ submissions."
            ),
            "challenge_publication": (
                f"{structured_challenge_submission_help_text} Otherwise, "
                f"please indicate if you plan to coordinate a publication "
                f"of the challenge results."
            ),
        }

    def __init__(self, creator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.creator = creator
        self.fields["title"].required = True
        self.fields["data_license"].initial = True
        self.fields["long_term_commitment"].initial = True
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    HTML(
                        "<br><p>Thank you for considering to host your challenge"
                        " on our platform! </p><p>Please use this form to tell us "
                        "more about your planned challenge. "
                        "The answers you provide below will help our team of "
                        "reviewers decide whether and in what way we can "
                        "support your challenge.</p>"
                        "<p>Before you fill out this form, please read our <a href="
                        "'https://grand-challenge.org/documentation/challenges/'"
                        "target='_blank'>challenge documentation</a> and our <a href="
                        "'https://grand-challenge.org/challenge-policy-and-pricing/'"
                        "target='_blank'>challenge pricing policy</a>.</p><br>"
                    ),
                ),
                *general_information_items_1,
                Div(
                    HTML(
                        "<p class='mb-0'>Structured challenge submission form </p>"
                        "<small class='text-muted mb-2'> Have you registered this challenge "
                        "for a conference (e.g., MICCAI, ISBI) <a href='https://www.biomedical-challenges.org/' target='_blank'> "
                        "through this website</a>? If so, please provide the DOI for your submission form, or"
                        " upload the submission PDF here. If you want to <a href='https://www.midl.io/'>organize your challenge with MIDL</a>, "
                        "you <u>must</u> fill out the <a href='https://www.biomedical-challenges.org/'>structured submission form</a> and upload the PDF. "
                        "If you have added a link or PDF, please fill the below text boxes with 'See structured submission form'.</small>"
                    ),
                    Div(
                        "structured_challenge_submission_doi",
                        css_class="col-5 pl-0",
                    ),
                    Div(
                        HTML("<p>or</p>"),
                        css_class="col-1 pl-0 d-flex align-items-center justify-content-center",
                    ),
                    Div(
                        "structured_challenge_submission_form",
                        css_class="col-5 pl-0",
                    ),
                    css_class="container row m-0 p-0 justify-content-between",
                ),
                *general_information_items_2,
                Div(
                    "algorithm_inputs",
                    "algorithm_outputs",
                    id="type-2-fields",
                ),
                Div(
                    HTML(
                        "<h3 class='d-flex justify-content-center'>Type 2 challenge cost estimation</h3><br>"
                    ),
                    HTML(
                        "<p>Since Type 2 challenges involve running algorithm "
                        "containers on our AWS infrastructure on a hidden test "
                        "set, we need to know how computationally expensive "
                        "your challenge submissions will be and how much data "
                        "storage your challenge requires. Please read our "
                        "<a href="
                        "'https://grand-challenge.org/challenge-policy-and-pricing/'"
                        "target='_blank'>challenge pricing policy</a> before you continue. We will use the "
                        "below information to calculate a rough compute and storage cost estimate.</p>"
                        "<p> If you are unfamiliar with what a Type 2 challenge"
                        " entails, please <a href="
                        "'https://grand-challenge.org/documentation/type-ii-challenge-setup/'"
                        "target='_blank'> first read our Type 2 challenge documentation</a>.</p> "
                        "<p>To help you fill in the below form correctly, "
                        "<a href='https://grand-challenge.org/documentation/create-your-own-challenge/'"
                        "target='_blank'> we have assembled example budgets "
                        "here</a>. Please take a close look at those before "
                        "proceeding to fill in this form.</p><br>"
                    ),
                    "number_of_tasks",
                    "average_size_of_test_image_in_mb",
                    "inference_time_limit_in_minutes",
                    "budget_for_hosting_challenge",
                    HTML(
                        "<br><p>Type 2 challenges usually consist of 2 phases. "
                        "The first of those tends to be a "
                        "<b>preliminary test phase</b>, "
                        "and the second the <b>final test phase</b>. The "
                        "number of test images used for these phases and "
                        "often the amount of times that users can submit to "
                        "them differs, which is why we ask for separate "
                        "estimates for the two phases below."
                        " Should your challenge have only phase, enter 0 in "
                        "all fields for phase 2. Should your challenge have "
                        "multiple tasks and hence more than N*2 phases, "
                        "please provide the average numbers across tasks for "
                        "each phase below and indicate the number of "
                        "tasks above accordingly. For examples of those"
                        " and other scenarios, have a look "
                        "<a href='https://grand-challenge.org/documentation/create-your-own-challenge/'"
                        "target='_blank'>at our example budget calculations</a>"
                        ".</p><h4>Phase 1</h4>"
                    ),
                    *phase_1_items,
                    HTML("<h4>Phase 2</h4>"),
                    *phase_2_items,
                    id="budget-fields",
                    css_class="border rounded px-4 pt-4 my-5",
                ),
                "comments",
            ),
            ButtonHolder(Submit("save", "Save")),
        )

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
        if start and end and start >= end:
            raise ValidationError(
                "The start date needs to be before the end date."
            )
        return cleaned_data


class ChallengeRequestStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = ChallengeRequest
        fields = ("status",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].label = False
        self.fields["status"].choices = [
            c
            for c in self.Meta.model.ChallengeRequestStatusChoices.choices
            if c[0] != self.Meta.model.ChallengeRequestStatusChoices.PENDING
        ]
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div("status", css_class="col-lg-8 px-0 mt-3"),
                Div(
                    ButtonHolder(
                        Submit("save", "Save", css_class="btn-sm mt-lg-1")
                    ),
                    css_class="col-lg-4 pb-0 mt-lg-3 pl-lg-2",
                ),
                css_class="row container m-0 p-0",
            )
        )
        self.helper.attrs.update(
            {
                "hx-post": reverse(
                    "challenges:requests-status-update",
                    kwargs={"pk": self.instance.pk},
                ),
                # use 'this' to display form errors in place, when the form is valid,
                # a page refresh will be triggered (by setting HX-Refresh to true)
                "hx-target": "this",
                "hx-swap": "outerHTML",
            }
        )
        if (
            self.instance.status
            != self.instance.ChallengeRequestStatusChoices.PENDING
        ):
            self.fields["status"].disabled = True

    def clean_status(self):
        status = self.cleaned_data.get("status")
        if (
            status == self.instance.ChallengeRequestStatusChoices.ACCEPTED
            and Challenge.objects.filter(
                short_name=self.instance.short_name
            ).exists()
        ):
            raise ValidationError(
                f"There already is a challenge with short "
                f"name: {self.instance.short_name}. Contact "
                f"support@grand-challenge.org to accept this request.",
            )
        return status


class ChallengeRequestBudgetUpdateForm(
    ChallengeRequestBudgetFieldValidationMixin, forms.ModelForm
):
    class Meta:
        model = ChallengeRequest
        fields = (
            "expected_number_of_teams",
            "number_of_tasks",
            "inference_time_limit_in_minutes",
            "average_size_of_test_image_in_mb",
            "phase_1_number_of_submissions_per_team",
            "phase_1_number_of_test_images",
            "phase_2_number_of_submissions_per_team",
            "phase_2_number_of_test_images",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "budget"
        self.helper.attrs.update(
            {
                "hx-post": reverse(
                    "challenges:requests-budget-update",
                    kwargs={"pk": self.instance.pk},
                ),
                "hx-target": "#budget",
                "hx-swap": "outerHTML",
            }
        )
        self.helper.layout.append(Submit("save", "Save"))
