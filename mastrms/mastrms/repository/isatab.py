import re
import zipfile

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from .models import Project, NodeClient

class ISATabExportView(View):
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        filename = self._archive_filename(project)

        response = HttpResponse(content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename

        return self._assemble_archive(project, response)

    def _assemble_archive(self, project, response):
        archive = zipfile.ZipFile(response, "w", zipfile.ZIP_DEFLATED)
        inv = self._create_investigation(project)
        archive.writestr(self._investigation_filename(project), inv)

        for exp in project.experiment_set.all():
            study = self._create_study(exp)
            archive.writestr(self._study_filename(exp), study)

        return response

    def _create_investigation(self, project):
        def q(s):
            """
            Quotes a value string if it contains a tab or newline
            character. Quote characters are escaped by doubling them.
            """
            if "\t" in s or "\n" in s:
                return '"%s"' % s.replace('"', '""')
            return s

        client = project.client

        fields = [
            ("ONTOLOGY SOURCE REFERENCE", None),
            ("Term Source Name", "OBI"),
            ("Term Source File", "http://obi-ontology.org"),
            ("Term Source Version", ""),
            ("Term Source Description", "Ontology for Biomedical Investigations"),
            ("INVESTIGATION", None),
            ("Investigation Identifier", self._investigation_identifier(project)),
            ("Investigation Title", q(project.title)),
            ("Investigation Description", q(project.description)),
            ("Investigation Submission Date", ""),
            ("Investigation Public Release Date", ""),
            ("INVESTIGATION PUBLICATIONS", None),
            ("Investigation PubMed ID", ""),
            ("Investigation Publication DOI", ""),
            ("Investigation Publication Author List", ""),
            ("Investigation Publication Title", ""),
            ("Investigation Publication Status", ""),
            ("Investigation Publication Status Term Accession Number", ""),
            ("Investigation Publication Status Term Source REF", ""),
            ("INVESTIGATION CONTACTS", None),
            ("Investigation Person Last Name", q(client.last_name) if client else ""),
            ("Investigation Person First Name", q(client.first_name) if client else ""),
            ("Investigation Person Mid Initials", ""),
            ("Investigation Person Email", q(client.email) if client else ""),
            ("Investigation Person Phone", q(client.telephoneNumber) if client else ""),
            ("Investigation Person Fax", ""),
            ("Investigation Person Address", q(client.get_address()) if client else ""),
            ("Investigation Person Affiliation", q(client.businessCategory) if client else ""),
            ("Investigation Person Roles", "Research Scientist"),
            ("Investigation Person Roles Term Accession Number", ""),
            ("Investigation Person Roles Term Source REF", ""),
            ("", None),  # Empty Line
        ]

        for exp in project.experiment_set.all():
            # Each experiment in mastr-ms is be detailed in a STUDY

            machines = exp.run_set.values_list("machine")
            machines = NodeClient.objects.filter(id__in=machines)
            machines = ", ".join(machines.values_list("station_name", flat=True))

            fields.extend([
                ("STUDY", None),
                ("Study Identifier", self._study_identifier(exp)),
                ("Study Title", q(exp.title)),
                ("Study Submission Date", ""),
                ("Study Public Release Date", ""),
                ("Study Description", q(exp.description)),
                ("Study File Name", self._study_filename(exp)),
                ("STUDY DESIGN DESCRIPTORS", None),
                ("Study Design Type", ""),
                ("Study Design Type Term Accession Number", ""),
                ("Study Design Type Term Source REF", ""),
                ("STUDY PUBLICATIONS", None),
                ("Study PubMed ID", ""),
                ("Study Publication DOI", ""),
                ("Study Publication Author List", ""),
                ("Study Publication Title", ""),
                ("Study Publication Status", ""),
                ("Study Publication Status Term Accession Number", ""),
                ("Study Publication Status Term Source REF", ""),
                ("STUDY FACTORS", None),
                ("Study Factor Name", ""),
                ("Study Factor Type", ""),
                ("Study Factor Type Term Accession Number", ""),
                ("Study Factor Type Term Source REF", ""),
                ("STUDY ASSAYS", None),
                ("Study Assay Measurement Type", "metabolite profiling"),
                ("Study Assay Measurement Type Term Source REF", "OBI"),
                ("Study Assay Measurement Type Term Accession Number", "0000366"),
                ("Study Assay Technology Type", "mass spectrometry"),
                ("Study Assay Technology Type Term Source REF", "OBI"),
                ("Study Assay Technology Type Term Accession Number", ""),
                ("Study Assay Technology Platform", q(machines)),
                ("Study Assay File Name", q("TO BE DECIDED")),
                ("STUDY PROTOCOLS", None),
            ])

        def make_entry((name, value)):
            return "%s\t%s" % (name, value) if value is not None else name

        return "\n".join(map(make_entry, fields))

    def _create_study(self, experiment):
        return "\n"  # to be determined

    @staticmethod
    def _choose_basename(title):
        "Generates a clean filename from a title string"
        repls = ((r"\s+", "_"), ("\n", "_"), ("'", ""), ('"', ""),
                 (r"_+", "_"), (r"^_", ""), (r"_$", ""))
        cleaner = lambda s, (pat, repl): re.sub(pat, repl, s)
        return reduce(cleaner, repls, title)

    def _archive_filename(self, project):
        return "mastrmsPR_%s_%s.zip" % (project.id, self._choose_basename(project.title))

    def _investigation_identifier(self, project):
        return "mastrmsPR_%s" % project.id

    def _investigation_filename(self, project):
        return "i_mastrmsPR_%s.txt" % project.id

    def _study_identifier(self, exp):
        return "mastrmsPR_%s_EX_%s" % (exp.project.id, exp.id)

    def _study_filename(self, exp):
        # return "s_%s-%s.txt" % (self._choose_basename(exp.title), exp.id)
        return "s_mastrmsPR_%s_EX_%s.txt" % (exp.project.id, exp.id)
