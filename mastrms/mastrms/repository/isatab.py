import os.path
import re
import zipfile
from numbers import Number
from collections import OrderedDict
from itertools import imap
import csv
from StringIO import StringIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from .models import Project, NodeClient, MicrobialInfo, PlantInfo, AnimalInfo, HumanInfo, RunSample
from ..decorators import mastr_users_only, mastr_users_only_method

@mastr_users_only
def isa_study_view(request, project_id, experiment_id):
    from .models import Experiment
    exp = get_object_or_404(Experiment, project__id=project_id, id=experiment_id)
    v = ISATabExportView()
    return HttpResponse(v._create_study(exp), content_type="text/plain")

class ISATabExportView(View):
    @mastr_users_only_method
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        basename = self._archive_filename(project)

        response = HttpResponse(content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename="%s.zip"' % basename

        return self._assemble_archive(project, response, basename + "/")

    def _assemble_archive(self, project, response, prefix=""):
        archive = zipfile.ZipFile(response, "w", zipfile.ZIP_DEFLATED)

        # output experiments grouped by investigation
        for inv in project.investigation_set.all():
            exps = project.experiment_set.filter(investigation=inv)

            if len(exps) > 0:
                invtab = self._create_investigation(inv, exps)
                archive.writestr(prefix + self._investigation_filename(project, inv), invtab)
                self._write_project_experiments(archive, inv, exps, prefix)

        # output any experiments which don't have an investigation
        other_exps = project.experiment_set.filter(investigation__isnull=True)
        if len(other_exps) > 0:
            invtab = self._create_investigation_project(project, other_exps)
            archive.writestr(prefix + self._investigation_filename(project), invtab)
            self._write_project_experiments(archive, None, other_exps, prefix)

        return response

    def _write_project_experiments(self, archive, inv, experiments, prefix):
        for exp in experiments:
            study = self._create_study(exp)
            archive.writestr(prefix + self._study_filename(inv, exp), study)
            assay = self._create_assay(exp)
            archive.writestr(prefix + self._assay_filename(inv, exp), assay)

    def _create_investigation(self, inv, experiments):
        return self._create_investigation_base(inv.project, inv, inv.title,
                                               inv.description, experiments)

    def _create_investigation_project(self, project, experiments):
        return self._create_investigation_base(project, None, project.title,
                                               project.description, experiments)

    def _create_investigation_base(self, project, inv, title, description, experiments):
        identifier = self._investigation_identifier(project, inv)
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
            ("Term Source Name", ("OBI", "SNOMEDCT")),
            ("Term Source File", ("http://obi-ontology.org", "http://bioportal.bioontology.org/ontologies/46896")),
            ("Term Source Version", ("", "")),
            ("Term Source Description", ("Ontology for Biomedical Investigations", "SNOMED Clinical Terms")),
            ("INVESTIGATION", None),
            ("Investigation Identifier", identifier),
            ("Investigation Title", title),
            ("Investigation Description", description),
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

        for exp in experiments:
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
                ("Study File Name", self._study_filename(inv, exp)),
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
                ("Study Factor Name", ("Treatment", "Timeline")),
                ("Study Factor Type", ("", "")),
                ("Study Factor Type Term Accession Number", ("", "")),
                ("Study Factor Type Term Source REF", ("", "")),
                ("STUDY ASSAYS", None),
                ("Study Assay Measurement Type", "metabolite profiling"),
                ("Study Assay Measurement Type Term Source REF", "OBI"),
                ("Study Assay Measurement Type Term Accession Number", "0000366"),
                ("Study Assay Technology Type", "mass spectrometry"),
                ("Study Assay Technology Type Term Source REF", "OBI"),
                ("Study Assay Technology Type Term Accession Number", ""),
                ("Study Assay Technology Platform", machines),
                ("Study Assay File Name", self._assay_filename(inv, exp)),
                ("STUDY PROTOCOLS", None),
                ("Study Protocol Name", ("Sample collection", "Metabolite extraction", "Chromatography", "Mass spectrometry")),
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

                ("STUDY CONTACTS", None),
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
                ("Study Person Roles Term Source REF", ("",) * len(managers)),

                ("", None),  # Empty Line
            ])

        return self._tab_format(fields)

    def _create_study(self, experiment):
        def source_type(rs):
            if rs.sample and rs.sample.sample_class and rs.sample.sample_class.biological_source:
                return rs.sample.sample_class.biological_source.type.name
            return ""
        def source_name(rs):
            if rs.sample and rs.sample.sample_class and rs.sample.sample_class.organ:
                organ = rs.sample.sample_class.organ
                return organ.name or organ.abbreviation
            return ""
        def sample_notes(rs):
            if rs.sample and rs.sample.sample_class and rs.sample.sample_class.biological_source:
                return rs.sample.sample_class.biological_source.information
            return experiment.sample_preparation_notes
        def ncbi_id(rs):
            if rs.sample and rs.sample.sample_class and rs.sample.sample_class.biological_source:
                return rs.sample.sample_class.biological_source.ncbi_id
            return ""
        def protocol_ref(rs):
            return "; ".join(map(sop_url, experiment.standardoperationprocedure_set.all()))
        def sop_url(sop):
            kwargs = {"sop_id": sop.id, "filename": os.path.basename(sop.attached_pdf.name)}
            return "https://%s%s" % (Site.objects.first().domain,
                                     reverse("downloadSOPFile", kwargs=kwargs))

        columns = [("Source Name", source_type),
                   ("Characteristics[Organism]", sample_notes),
                   ("Term Source REF", ncbi_id),
                   ("Term Accession Number", const("")),
                   ("Characteristics[Organism part]", source_name),
                   #("Material Type", source_type),
        ]

        info_columns = {
            MicrobialInfo: [
                ("Characteristics[genus]", "genus"),
                ("Characteristics[species]", "species"),
                ("Characteristics[Culture collection Id]", "culture_collection_id"),
                ("Characteristics[Media]", "media"),
                ("Characteristics[Fermentation vessel]", "fermentation_vessel"),
                ("Characteristics[Fermentation mode]", "fermentation_mode"),
                ("Characteristics[Innoculation density]", "innoculation_density"),
                ("Characteristics[Fermentation volume]", "fermentation_volume"),
                ("Characteristics[Temperature]", "temperature"),
                ("Characteristics[Agitation]", "agitation"),
                ("Factor value[ph]", "ph"),
                ("Characteristics[Gas type]", "gas_type"),
                ("Characteristics[Gas flow rate]", "gas_flow_rate"),
                ("Characteristics[Gas delivery method]", "gas_delivery_method"),
            ],
            PlantInfo: [
                ("Characteristics[Development stage]", "development_stage"),
            ],
            AnimalInfo: [
                ("Characteristics[Sex]", "sex"),
                ("Characteristics[Age]", "age"),
                ("Characteristics[Parental line]", "parental_line"),
                ("Characteristics[Location]", "location"),
                #("Characteristics[notes]", "notes"),
            ],
            HumanInfo: [
                ("Characteristics[Sex]", "sex"),
                ("Characteristics[Date of birth]", "date_of_birth"),
                ("Characteristics[Body mass index]", "bmi"),
                ("Characteristics[Diagnosis]", "diagnosis"),
                ("Characteristics[Location]", "location"),
                #("Characteristics[Notes]", "notes"),
            ],
        }

        # set up columns based on the type of sources in the experiment
        for type_source in experiment.biologicalsource_set.order_by("type").distinct():
            BioInfo = type_source.get_info_cls()
            for (heading, attr) in info_columns.get(BioInfo, []):
                def mkgetter(type, attr):
                    def getter(rs):
                        if rs.sample and rs.sample.sample_class:
                            source = rs.sample.sample_class.biological_source
                            if source and source.type == type:
                                return getattr(source.get_info(), attr, "")
                        return ""
                    return getter
                columns.append((heading, mkgetter(type_source.type, attr)))

        columns.extend([("Protocol REF", protocol_ref),
                        ("Sample Name", RunSample.generate_filename)])

        columns = OrderedDict(columns)

        header = columns.keys()
        fields = columns.values()

        tabfile = [header]
        for run in experiment.run_set.order_by("created_on"):
            for rs in run.runsample_set.order_by("sample__id"):
                tabfile.append([field(rs) for field in fields])

        return self._csv_format(tabfile)

    def _create_assay(self, experiment):
        def sample_alt_name(runsample):
            return unicode(runsample.sample) if runsample.sample else unicode(runsample.id)
        def source_type(rs):
            if rs.sample and rs.sample.sample_class and rs.sample.sample_class.biological_source:
                src = rs.sample.sample_class.biological_source
                info = src.information.replace("\n", " ")
                return "%s_%s" % (src.type.name, info) if info else src.type.name
            return ""
        def sample_label(runsample):
            if runsample.sample:
                return "%s_%s" % (runsample.sample.label, runsample.sample.comment)
            return ""
        def sample_treatment(rs):
            if rs.sample and rs.sample.sample_class and rs.sample.sample_class.treatments:
                return rs.sample.sample_class.treatments.name
            return ""
        def sample_timeline(rs):
            if rs.sample and rs.sample.sample_class and rs.sample.sample_class.timeline:
                return rs.sample.sample_class.timeline.timeline
            return ""

        columns = (("Sample Name", RunSample.generate_filename),
                   ("Material Type", source_type),
                   ("Term Source REF", const("")),
                   ("Term Accession Number", const("")),
                   ("Protocol REF", const("Metabolite extraction")), # make sure that's in the investigation
                   ("Extract Name", RunSample.generate_filename),
                   ("Labeled Extract Name", RunSample.generate_filename),
                   ("Label", sample_label),
                   ("Term Source REF", const("")),
                   ("Term Accession Number", const("")),
                   ("MS Assay Name", RunSample.generate_filename_no_ext),
                   ("Raw Spectral Data File", RunSample.generate_filename),
                   ("Factor Value[Treatment]", sample_treatment),
                   ("Term Source REF", const("")),
                   ("Term Accession Number", const("")),
                   ("Factor Value[Timeline]", sample_timeline),
                   ("Unit", const("")),
                   ("Term Source REF", const("")),
                   ("Term Accession Number", const("")))

        header = [h for (h, f) in columns]
        fields = [f for (h, f) in columns]

        tabfile = [header]
        for run in experiment.run_set.order_by("created_on"):
            for rs in run.runsample_set.order_by("sample__id"):
                tabfile.append([field(rs) for field in fields])

        return self._csv_format(tabfile)

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

    @staticmethod
    def _csv_format(vals):
        out = StringIO()
        tabwriter = csv.writer(out, dialect="excel-tab")
        for row in vals:
            tabwriter.writerow(row)
        return out.getvalue()

    @staticmethod
    def _choose_basename(title):
        "Generates a clean filename from a title string"
        repls = ((r"\s+", "_"), ("\n", "_"), ("'", ""), ('"', ""),
                 (r"_+", "_"), (r"^_", ""), (r"_$", ""))
        cleaner = lambda s, (pat, repl): re.sub(pat, repl, s)
        return reduce(cleaner, repls, title)

    def _archive_filename(self, project):
        return "mastrmsPR_%s_%s" % (project.id, self._choose_basename(project.title))

    def _investigation_identifier(self, project, inv=None):
        suffix = "_INV_%s" % inv.id if inv else ""
        return "mastrmsPR_%s%s" % (project.id, suffix)

    def _investigation_filename(self, project, inv=None):
        return "i_%s.txt" % self._investigation_identifier(project, inv)

    def _study_identifier(self, exp):
        return "mastrmsPR_%s_EX_%s" % (exp.project.id, exp.id)

    def _study_filename(self, inv, exp):
        # return "s_%s-%s.txt" % (self._choose_basename(exp.title), exp.id)
        return "s_%s_EX_%s.txt" % (self._investigation_identifier(exp.project, inv), exp.id)

    def _assay_filename(self, inv, exp):
        return "a_%s_EX_%s.txt" % (self._investigation_identifier(exp.project, inv), exp.id)

const = lambda c: lambda x: c
