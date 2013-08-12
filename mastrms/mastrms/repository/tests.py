# -*- encoding: utf-8 -*-
"""
This file contains unit tests for the repository application.
"""

from django.test import TestCase
from django.utils import unittest
from StringIO import StringIO
from decimal import Decimal
from mastrms.repository.wsviews import _handle_uploaded_sample_csv
from mastrms.repository.models import Project, Experiment, Sample
import logging
logger = logging.getLogger(__name__)

class SampleCsvUploadTest(TestCase):
    """
    Unit tests for parsing of uploaded samples CSV. The target
    function is `_handle_uploaded_sample_csv`.
    """
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

    def test01_simple_noheader(self):
        """
        Basic valid CSV file without header
        """
        text = "Sample Label,1.0,Comment about the sample\n"

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test02_simple_header(self):
        """
        Basic valid CSV file with header.
        """
        text = """label,weight,comment
Sample Label,1.0,Comment about the sample
"""

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test03_simple_header_order(self):
        """
        Basic valid CSV file with header, different column order.
        """
        text = """weight,label,comment
1.0,Sample Label,Comment about the sample
"""

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test04_simple_header_capitalized(self):
        """
        Basic valid CSV file with capitalized headers.
        """
        text = """LABEL,Weight,cOmmENT
Sample Label,1.0,Comment about the sample
"""

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test05_extra_columns(self):
        """
        Valid CSV file, no header, extra columns.
        """
        text = "Sample Label,1.0,Comment about the sample,an interesting column,,,4,5,6,lah,\n"

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test06_extra_headers(self):
        """
        Valid CSV file, extra columns with headers.
        """
        text = """colour,label,weight,units,comment,size
Green,Sample Label,1.0,kg,Comment about the sample,Large
"""

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test07_whitespace(self):
        """
        Valid CSV file, columns have some whitespace.
        """
        text = """    Label, Weight  , Comment
    Sample Label,  1.0  ,  Comment about the sample
"""

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "    Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "  Comment about the sample")

    def test07_msdos_newlines(self):
        """
        Valid CSV file with dos/windows newlines.
        """
        text = "Label,Weight,Comment\r\nSample Label,1.0,Comment about the sample\r\nSample Label,1.0,Comment about the sample\r\n\r\n"

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 2)
        for sample in samples:
            self.assertEqual(sample.experiment, self.experiment)
            self.assertEqual(sample.label, "Sample Label")
            self.assertEqual(sample.weight, Decimal("1.0"))
            self.assertEqual(sample.comment, "Comment about the sample")

    def test07_empty(self):
        """
        Empty file. Should return an error message to client.
        """
        text = "\n"

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertFalse(result["success"])
        self.assertTrue(bool(result.get("msg", "")))
        self.assertEqual(len(samples), 0)

    def test08_empty_with_header(self):
        """
        Single header line. Should return an error message to client.
        """
        text = "label,weight,comment\n"

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertFalse(result["success"])
        self.assertTrue(bool(result.get("msg", 0)))
        self.assertEqual(len(samples), 0)

    @unittest.skip("haven't implemented unicode csv reading yet")
    def test09_unicode_data(self):
        """
        Valid CSV with utf-8 encoded text in column data.
        """
        text = u"Sample µ,1.0,☃ Snowman ☃\n"

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample µ")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "☃ Snowman ☃")

    @unittest.skip("haven't implemented unicode csv reading yet")
    def test10_unicode_header(self):
        """
        Valid CSV with utf-8 encoded text in additional headers.
        """
        text = u"""label,weight,comment,µ,☃,❄,🐈
Sample Label,1.0,Comment about the sample,µ,☃,❄,🐈
"""

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertTrue(result["success"])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test11_invalid_decimal(self):
        """
        CSV with non-numeric weight value.
        """
        text = """label,weight,comment
Sample Label,not a number,Comment about the sample
"""

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertFalse(result["success"])
        self.assertIn("decimal", result.get("msg", "").lower())
        self.assertEqual(result.get("invalid_lines", -1), [2])
        self.assertEqual(len(samples), 0)

    def test11_some_invalid_lines(self):
        """
        CSV with one valid line, and one with a non-numeric weight value.
        """
        text = """label,weight,comment
Sample Label,1.0,Comment about the sample
Sample Label,not a number,Comment about the sample
"""

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertFalse(result["success"])
        self.assertIn("decimal", result.get("msg", "").lower())
        self.assertEqual(result.get("invalid_lines", -1), [3])

        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].experiment, self.experiment)
        self.assertEqual(samples[0].label, "Sample Label")
        self.assertEqual(samples[0].weight, Decimal("1.0"))
        self.assertEqual(samples[0].comment, "Comment about the sample")

    def test12_missing_column(self):
        """
        CSV which is valid, except missing an essential column.
        """
        text = """label,weight
Sample Label,1.0
"""

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertFalse(result["success"])
        self.assertIn("comment", result.get("msg", "").lower())
        self.assertIn("missing", result.get("msg", "").lower())
        self.assertEqual(len(samples), 0)

    def test13_missing_columns(self):
        """
        CSV is missing two essential columns.
        """
        text = """label
Sample Label
"""

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

        samples = Sample.objects.all()

        self.assertFalse(result["success"])
        self.assertIn("comment", result.get("msg", "").lower())
        self.assertIn("weight", result.get("msg", "").lower())
        self.assertIn("missing", result.get("msg", "").lower())
        self.assertEqual(len(samples), 0)

    def test14_multiple_samples(self):
        """
        CSV exported from mastrms with 2 samples.
        """
        text = "# id, sample_id, sample_class, sample_class__unicode, experiment, experiment__unicode, label, comment, weight, sample_class_sequence, \n1,,1,class_1,1,exp,label 1,comment,42,1\n2,,1,class_1,1,exp,label 2,comment,43,1\n"

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

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

    def test15_sample_update(self):
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

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

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

    def test16_sample_update_create(self):
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

        result = _handle_uploaded_sample_csv(self.experiment, StringIO(text))

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
