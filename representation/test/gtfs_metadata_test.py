from unittest import TestCase
from unittest.mock import MagicMock
from representation.gtfs_metadata import GtfsMetadata


class GtfsMetadataTest(TestCase):

    def test_gtfs_metadata_with_none_md5_hash_should_raise_exception(self):
        self.assertRaises(TypeError, GtfsMetadata, None)

    def test_gtfs_metadata_with_invalid_md5_hash_string_should_raise_exception(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = int
        self.assertRaises(TypeError, GtfsMetadata, mock_md5_hash)

    def test_gtfs_metadata_with_valid_md5_hash_string_should_return_instance(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str

        under_test = GtfsMetadata(mock_md5_hash)
        self.assertIsInstance(under_test, GtfsMetadata)

    def test_gtfs_metadata_to_string_special_method_should_return_metadata_string(self):
        mock_md5_hash = MagicMock()
        mock_md5_hash.__class__ = str
        mock_md5_hash.__str__.return_value = 'test_md5_hash'

        test_metadata_string = "Timezone: \n" \
                               "Country code: \n" \
                               "Sub country code: \n" \
                               "Language code: \n" \
                               "Start service date: \n" \
                               "End service date: \n" \
                               "Start timestamp: \n" \
                               "End timestamp: \n" \
                               "Bounding box: \n" \
                               "Stable url: \n" \
                               "MD5 hash: test_md5_hash"

        gtfs_metadata = GtfsMetadata(str(mock_md5_hash))
        under_test = str(gtfs_metadata)
        self.assertEqual(under_test, test_metadata_string)
