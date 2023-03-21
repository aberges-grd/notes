import unittest
from pathlib import Path
from dirtree_helper import crawl_directory


class TestCrawlDirectory(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("myfolder")

    def test_no_limit(self):
        expected_output = {
            "notes": {
                "bibliography.bibtex": None,
                "clean_arch.md": None,
                "dvc_cml.md": None,
                "includes": {
                    "tree_l1.tex": None,
                    "tree_l2.tex": None,
                },
            }
        }
        self.assertEqual(crawl_directory(self.test_dir), expected_output)

    def test_limit_1(self):
        expected_output = {
            "notes": {
                "bibliography.bibtex": None,
                "clean_arch.md": None,
                "dvc_cml.md": None,
                "includes": None,
            }
        }
        self.assertEqual(crawl_directory(self.test_dir, level=1), expected_output)

    def test_alias(self):
        expected_output = {
            "my_notes": {
                "bibliography.bibtex": None,
                "clean_arch.md": None,
                "dvc_cml.md": None,
                "includes": {
                    "tree_l1.tex": None,
                    "tree_l2.tex": None,
                },
            }
        }
        self.assertEqual(
            crawl_directory(self.test_dir, alias="my_notes"), expected_output
        )


if __name__ == "__main__":
    unittest.main()
