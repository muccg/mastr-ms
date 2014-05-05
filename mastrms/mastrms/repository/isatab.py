import re
import zipfile
from numbers import Number

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from .models import Project, NodeClient

class ISATabExportView(View):
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        basename = self._archive_filename(project)

        response = HttpResponse(content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename="%s.zip"' % basename

        return self._assemble_archive(project, response, basename + "/")

    def _assemble_archive(self, project, response, prefix=""):
        archive = zipfile.ZipFile(response, "w", zipfile.ZIP_DEFLATED)
        inv = self._create_investigation(project)
        archive.writestr(prefix + self._investigation_filename(project), inv)

        for exp in project.experiment_set.all():
            study = self._create_study(exp)
            archive.writestr(prefix + self._study_filename(exp), study)
            assay = self._create_assay(exp)
            archive.writestr(prefix + self._assay_filename(exp), assay)

        return response

    def _create_investigation(self, project):
        managers = project.managers.order_by("last_name")

        def getdesc(o, a):
            x = getattr(o, a)
            return x() if callable(x) else x

        md = dict((a, tuple(getdesc(mgr, a) for mgr in managers))
                  for a in ("last_name", "first_name", "email",
                            "telephoneNumber", "get_address",
                            "businessCategory"))

        fields = [
            ("ONTOLOGY SOURCE REFERENCE", None),
            ("Term Source Name", "OBI"),
            ("Term Source File", "http://obi-ontology.org"),
            ("Term Source Version", ""),
            ("Term Source Description", "Ontology for Biomedical Investigations"),
            ("INVESTIGATION", None),
            ("Investigation Identifier", self._investigation_identifier(project)),
            ("Investigation Title", project.title),
            ("Investigation Description", project.description),
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
            ("Investigation Person Last Name", md["last_name"]),
            ("Investigation Person First Name", md["first_name"]),
            ("Investigation Person Mid Initials", ""),
            ("Investigation Person Email", md["email"]),
            ("Investigation Person Phone", md["telephoneNumber"]),
            ("Investigation Person Fax", ""),
            ("Investigation Person Address", md["get_address"]),
            ("Investigation Person Affiliation", md["businessCategory"]),
            ("Investigation Person Roles", "Research Scientist"),
            ("Investigation Person Roles Term Accession Number", ""),
            ("Investigation Person Roles Term Source REF", ""),
            ("", None),  # Empty Line
        ]

        for exp in project.experiment_set.all():
            # Each experiment in mastr-ms is be detailed in a STUDY

            machines = exp.run_set.values_list("machine")
            machines = NodeClient.objects.filter(id__in=machines)
            machines = list(machines.values_list("station_name", flat=True))

            fields.extend([
                ("STUDY", None),
                ("Study Identifier", self._study_identifier(exp)),
                ("Study Title", exp.title),
                ("Study Submission Date", ""),
                ("Study Public Release Date", ""),
                ("Study Description", exp.description),
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
                ("Study Assay Technology Platform", machines),
                ("Study Assay File Name", self._assay_filename(exp)),
                ("STUDY PROTOCOLS", None),
                # fixme: protocols need to be TAB separated
                ("Study Protocol Name", ("Sample collection", "Extraction", "Chromatography", "Mass spectrometry")),
                ("Study Protocol Type", ("Sample collection", "Extraction", "Chromatography", "Mass spectrometry")),
                ("Study Protocol Type Term Accession Number", ""),
                ("Study Protocol Type Term Source REF", ""),
                ("Study Protocol Description", exp.sample_preparation_notes),
                ("Study Protocol URI", ""),
                ("Study Protocol Version", ""),
                ("Study Protocol Parameters Name", ("",
                                                    ["Post Extraction", "Derivatization"],
                                                    ["Chromatography Instrument", "Column type",
                                                     "Column model"],
                                                    ["Scan polarity", "Scan m/z range", "Instrument",
                                                     "Mass analyzer", "Ion source"])),
                ("Study Protocol Parameters Name Term Accession Number", ""),
                ("Study Protocol Parameters Name Term Source REF", ""),
                ("Study Protocol Components Name", ""),
                ("Study Protocol Components Type", ""),
                ("Study Protocol Components Type Term Accession Number", ""),
                ("Study Protocol Components Type Term Source REF", ""),

                ("STUDY CONTACT", None),
                ("Study Person Last Name", md["last_name"]),
                ("Study Person First Name", md["first_name"]),
                ("Study Person Mid Initials", ""),
                ("Study Person Email", md["email"]),
                ("Study Person Phone", md["telephoneNumber"]),
                ("Study Person Fax", ""),
                ("Study Person Address", md["get_address"]),
                ("Study Person Affiliation", md["businessCategory"]),
                ("Study Person Roles", ("Operational research officer",) * len(managers)),
                ("Study Person Roles Term Accession Number", ("",) * len(managers)),
                ("Study Person Roles Term Source REF", ("SNOMEDCT",) * len(managers)),

                ("", None),  # Empty Line
            ])

        return self._tab_format(fields)
    @staticmethod
    def _tab_format(fields):
        """
        Returns an ISA-Tab format string for the list of given field names
        and values.
        """
        def q(s):
            """
            Quotes a value string if it contains a tab or newline
            character. Quote characters are escaped by doubling them.
            """
            if "\t" in s or "\n" in s:
                return '"%s"' % s.replace('"', '""')
            return s

        def fmt(value):
            if isinstance(value, list):
                return "; ".join(map(q, value))
            elif isinstance(value, tuple):
                return "\t".join(map(fmt, value))
            return q(str(value))

        def make_entry((name, value)):
            return "%s\t%s" % (name, fmt(value)) if value is not None else name

        return "\n".join(map(make_entry, fields))

    def _create_study(self, experiment):
        return "\n"  # to be determined

    def _create_assay(self, experiment):
        return "\n"  # to be determined

    @staticmethod
    def _choose_basename(title):
        "Generates a clean filename from a title string"
        repls = ((r"\s+", "_"), ("\n", "_"), ("'", ""), ('"', ""),
                 (r"_+", "_"), (r"^_", ""), (r"_$", ""))
        cleaner = lambda s, (pat, repl): re.sub(pat, repl, s)
        return reduce(cleaner, repls, title)

    def _archive_filename(self, project):
        return "mastrmsPR_%s_%s" % (project.id, self._choose_basename(project.title))

    def _investigation_identifier(self, project):
        return "mastrmsPR_%s" % project.id

    def _investigation_filename(self, project):
        return "i_mastrmsPR_%s.txt" % project.id

    def _study_identifier(self, exp):
        return "mastrmsPR_%s_EX_%s" % (exp.project.id, exp.id)

    def _study_filename(self, exp):
        # return "s_%s-%s.txt" % (self._choose_basename(exp.title), exp.id)
        return "s_mastrmsPR_%s_EX_%s.txt" % (exp.project.id, exp.id)

    def _assay_filename(self, exp):
        return "a_mastrmsPR_%s_EX_%s.txt" % (exp.project.id, exp.id)
