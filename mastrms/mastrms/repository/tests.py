# -*- encoding: utf-8 -*-
"""
This file contains unit tests for the repository application.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.utils import unittest
from io import StringIO
from decimal import Decimal
from mastrms.repository.views import CSVUploadViewCaptureCSV, CSVUploadViewFile
from mastrms.repository.models import Project, Experiment, Sample, InstrumentMethod, RunSample
from mastrms.mdatasync_server.models import NodeClient
import json, logging
logger = logging.getLogger(__name__)

class SampleCsvUploadTest(TestCase):
    """
    Unit tests for parsing of uploaded samples CSV. The target
    function is `_handle_uploaded_sample_csv`.
    """

    urls = 'mastrms.repository.urls'
    def setUp(self):
        project = Project.objects.create(title="Test Project",
                                         description="Test",
                                         client=None)
        self.experiment = Experiment.objects.create(title="Test Experiment",
                                                    description="Test",
                                                    comment="Test",
                                                    job_number="001",
                                                    project=project,
                                                    instrument_method=None)

    def upload_csv(self, text):
        return CSVUploadViewFile.handle_csv(StringIO(text), self.experiment)

    def test_simple_noheader(self):
        """
        Basic valid CSV file without header
        """
        text = "Sample Label,1.0,Comment about the sample\n"

        import urls

        result = self.upload_csv(text)
        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test_simple_header(self):
        """
        Basic valid CSV file with header.
        """
        text = """label,weight,comment
Sample Label,1.0,Comment about the sample
"""

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test_simple_header_order(self):
        """
        Basic valid CSV file with header, different column order.
        """
        text = """weight,label,comment
1.0,Sample Label,Comment about the sample
"""

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test_simple_header_capitalized(self):
        """
        Basic valid CSV file with capitalized headers.
        """
        text = """LABEL,Weight,cOmmENT
Sample Label,1.0,Comment about the sample
"""

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test_extra_columns(self):
        """
        Valid CSV file, no header, extra columns.
        """
        text = "Sample Label,1.0,Comment about the sample,an interesting column,,,4,5,6,lah,\n"

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test_extra_headers(self):
        """
        Valid CSV file, extra columns with headers.
        """
        text = """colour,label,weight,units,comment,size
Green,Sample Label,1.0,kg,Comment about the sample,Large
"""

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test_whitespace(self):
        """
        Valid CSV file, columns have some whitespace.
        """
        text = """    Label, Weight  , Comment
    Sample Label,  1.0  ,  Comment about the sample
"""

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "    Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "  Comment about the sample")

    def test_msdos_newlines(self):
        """
        Valid CSV file with dos/windows newlines.
        """
        text = "Label,Weight,Comment\r\nSample Label,1.0,Comment about the sample\r\nSample Label,1.0,Comment about the sample\r\n\r\n"

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 2)
        for sample in samples:
            self.assertEqual(sample.experiment, self.experiment)
            self.assertEqual(sample.label, "Sample Label")
            self.assertEqual(sample.weight, Decimal("1.0"))
            self.assertEqual(sample.comment, "Comment about the sample")

    def test_mac_newlines(self):
        """
        Valid CSV file with mac newlines (carriage returns).
        """
        text = "Label,Weight,Comment\rSample Label,1.0,Comment about the sample\rSample Label,1.0,Comment about the sample\r"

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 2)
        for sample in samples:
            self.assertEqual(sample.experiment, self.experiment)
            self.assertEqual(sample.label, "Sample Label")
            self.assertEqual(sample.weight, Decimal("1.0"))
            self.assertEqual(sample.comment, "Comment about the sample")

    def test_empty(self):
        """
        Empty file. Should return an error message to client.
        """
        text = "\n"

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertFalse(result["success"])
        self.assertTrue(bool(result.get("msg", "")))
        self.assertEqual(len(samples), 0)

    def test_empty_with_header(self):
        """
        Single header line. Should return an error message to client.
        """
        text = "label,weight,comment\n"

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertFalse(result["success"])
        self.assertTrue(bool(result.get("msg", 0)))
        self.assertEqual(len(samples), 0)

    @unittest.skip("haven't implemented unicode csv reading yet")
    def test_unicode_data(self):
        """
        Valid CSV with utf-8 encoded text in column data.
        """
        text = u"Sample µ,1.0,☃ Snowman ☃\n"

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample µ")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "☃ Snowman ☃")

    @unittest.skip("haven't implemented unicode csv reading yet")
    def test_unicode_header(self):
        """
        Valid CSV with utf-8 encoded text in additional headers.
        """
        text = u"""label,weight,comment,µ,☃,❄,🐈
Sample Label,1.0,Comment about the sample,µ,☃,❄,🐈
"""

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test_invalid_decimal(self):
        """
        CSV with non-numeric weight value.
        """
        text = """label,weight,comment
Sample Label,not a number,Comment about the sample
"""

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertFalse(result["success"])
        self.assertIn("decimal", result.get("msg", "").lower())
        self.assertEqual(result.get("invalid_lines", -1), [2])
        self.assertEqual(len(samples), 0)

    def test_some_invalid_lines(self):
        """
        CSV with one valid line, and one with a non-numeric weight value.
        """
        text = """label,weight,comment
Sample Label,1.0,Comment about the sample
Sample Label,not a number,Comment about the sample
"""

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertFalse(result["success"])
        self.assertIn("decimal", result.get("msg", "").lower())
        self.assertEqual(result.get("invalid_lines", -1), [3])

        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test_missing_column(self):
        """
        CSV which is valid, except missing an essential column.
        """
        text = """label,weight
Sample Label,1.0
"""

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertFalse(result["success"])
        self.assertIn("comment", result.get("msg", "").lower())
        self.assertIn("missing", result.get("msg", "").lower())
        self.assertEqual(len(samples), 0)

    def test_missing_columns(self):
        """
        CSV is missing two essential columns.
        """
        text = """label
Sample Label
"""

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertFalse(result["success"])
        self.assertIn("comment", result.get("msg", "").lower())
        self.assertIn("weight", result.get("msg", "").lower())
        self.assertIn("missing", result.get("msg", "").lower())
        self.assertEqual(len(samples), 0)

    def test_multiple_samples(self):
        """
        CSV exported from mastrms with 2 samples.
        """
        text = "# id, sample_id, sample_class, sample_class__unicode, experiment, experiment__unicode, label, comment, weight, sample_class_sequence, \n1,,1,class_1,1,exp,label 1,comment,42,1\n2,,1,class_1,1,exp,label 2,comment,43,1\n"

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 2)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "label 1")
        self.assertEqual(samples[0].weight, Decimal("42.0"))
        self.assertEqual(samples[0].comment, "comment")
        self.assertEqual(samples[1].experiment, self.experiment)
        self.assertEqual(samples[1].label, "label 2")
        self.assertEqual(samples[1].weight, Decimal("43.0"))
        self.assertEqual(samples[1].comment, "comment")

    def make_more_samples(self):
        for sid in ["001", "002"]:
            Sample.objects.create(sample_id=sid,
                                  experiment=self.experiment,
                                  label="", comment="", weight=None)
        return Sample.objects.all()

    def test_sample_update(self):
        """
        Valid CSV containing sample id column, used to update existing
        samples.
        """
        samples = self.make_more_samples()

        self.assertEqual(len(samples), 2)

        # Exported CSV is actually created with javascript so we can't
        # reuse code here... hence formatting
        text = """# id, sample_id, sample_class, sample_class__unicode, experiment, experiment__unicode, label, comment, weight, sample_class_sequence,
%d,,1,class_1,1,exp,label A,comment A,42,1
%d,,1,class_1,1,exp,label B,comment B,43,1
""" % (samples[0].id, samples[1].id)

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 2)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "label A")
        self.assertEqual(samples[0].weight, Decimal("42.0"))
        self.assertEqual(samples[0].comment, "comment A")
        self.assertEqual(samples[1].experiment, self.experiment)
        self.assertEqual(samples[1].label, "label B")
        self.assertEqual(samples[1].weight, Decimal("43.0"))
        self.assertEqual(samples[1].comment, "comment B")

    def test_sample_update_create(self):
        """
        Valid CSV containing sample id column, used to update existing
        samples, and to create more samples.
        """
        samples = self.make_more_samples()

        self.assertEqual(len(samples), 2)

        # Exported CSV is actually created with javascript so we can't
        # reuse code here... hence formatting
        text = """# id, sample_id, sample_class, sample_class__unicode, experiment, experiment__unicode, label, comment, weight, sample_class_sequence,
%d,,1,class_1,1,exp,label A,comment A,42,1
%d,,1,class_1,1,exp,label B,comment B,43,1
,,1,class_1,1,exp,label C,comment C,44,1
""" % (samples[0].id, samples[1].id)

        result = self.upload_csv(text)

        samples = Sample.objects.all()

        self.assertEqual(len(samples), 3)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "label A")
        self.assertEqual(samples[0].weight, Decimal("42.0"))
        self.assertEqual(samples[0].comment, "comment A")
        self.assertEqual(samples[1].experiment, self.experiment)
        self.assertEqual(samples[1].label, "label B")
        self.assertEqual(samples[1].weight, Decimal("43.0"))
        self.assertEqual(samples[1].comment, "comment B")
        self.assertEqual(samples[2].experiment, self.experiment)
        self.assertEqual(samples[2].label, "label C")
        self.assertEqual(samples[2].weight, Decimal("44.0"))
        self.assertEqual(samples[2].comment, "comment C")

        self.assertTrue(result["success"])
        self.assertEqual(result["num_created"], 1)
        self.assertEqual(result["num_updated"], 2)

class UploadRunCaptureCSVTest(TestCase):
    """
    Unit tests for parsing of uploaded samples CSV. The target
    function is `uploadRunCaptureCSV`. CSV quirk tests are in
    SampleCsvUploadTest, and as CSV parsing is in common they are
    not replicated here.
    """

    urls = 'mastrms.repository.urls'
    def upload_csv(self, text):
        return CSVUploadViewCaptureCSV.handle_csv(
            StringIO(text),
            self.experiment,
            self.machine,
            self.method,
            'A Test Run',
            get_user_model().objects.all()[0])

    def setUp(self):
        project = Project.objects.create(title="Test Project",
                                         description="Test",
                                         client=None)
        self.experiment = Experiment.objects.create(title="Test Experiment",
                                                    description="Test",
                                                    comment="Test",
                                                    job_number="001",
                                                    project=project,
                                                    instrument_method=None)
        self.machine = NodeClient.objects.create(
            organisation_name = "Murdoch University",
            site_name = "CCG",
            station_name = "linuxpc"
            )
        self.method = InstrumentMethod.objects.create(
            title = "Test Case",
            method_path = "/test",
            method_name = "rusty python",
            version = "2.7.3",
            creator = get_user_model().objects.all()[0]
            )

    def test_upload_runcapture(self):
        """
        Upload single file to be captured from external run
        """
        text = "filename\ncat.jpg"
        result = self.upload_csv(text)
        run_samples = RunSample.objects.all()
        self.assertEqual(len(run_samples), 1)

        self.assertEqual(run_samples[0].filename, "cat.jpg")

        self.assertEqual(result['num_created'], 1)

    def test_upload_runcapture_no_header(self):
        """
        Upload single file to be captured from external run (no header line)
        """
        text = "cat.jpg"
        result = self.upload_csv(text)
        run_samples = RunSample.objects.all()
        self.assertEqual(len(run_samples), 1)

        self.assertEqual(run_samples[0].filename, "cat.jpg")

        self.assertEqual(result['num_created'], 1)

    def test_upload_multiple(self):
        """
        Upload multiple files to be captured from external run
        """
        text = "filename\ncat.jpg\ndog.jpg\nbudgie.jpg"
        result = self.upload_csv(text)
        run_samples = RunSample.objects.all()
        self.assertEqual(len(run_samples), 3)

        self.assertEqual(run_samples[0].filename, "cat.jpg")
        self.assertEqual(run_samples[1].filename, "dog.jpg")
        self.assertEqual(run_samples[2].filename, "budgie.jpg")

        self.assertEqual(result['num_created'], 3)

    def test_upload_multiple_no_header(self):
        """
        Upload multiple files to be captured from external run (no heaer line)
        """
        text = "cat.jpg\ndog.jpg\nbudgie.jpg"
        result = self.upload_csv(text)
        run_samples = RunSample.objects.all()
        self.assertEqual(len(run_samples), 3)

        self.assertEqual(run_samples[0].filename, "cat.jpg")
        self.assertEqual(run_samples[1].filename, "dog.jpg")
        self.assertEqual(run_samples[2].filename, "budgie.jpg")

        self.assertEqual(result['num_created'], 3)
