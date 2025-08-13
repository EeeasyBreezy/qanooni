import pytest

from app.services.implementations.MetadataExtractor import MetadataExtractor


class TestMetadataExtractor:
    def test_extracts_agreement_from_keywords(self):
        text = "This NDA is between Alpha and Beta."
        meta = MetadataExtractor().extract_metadata(text)
        assert meta.agreement_type == "Non-Disclosure Agreement"

    def test_extracts_agreement_from_heuristic_phrase(self):
        text = "This Master Services Agreement (MSA) is effective as of today."
        meta = MetadataExtractor().extract_metadata(text)
        assert meta.agreement_type in {"Master Services Agreement", "Service Agreement"}

    def test_extracts_jurisdiction_and_geographies(self):
        text = (
            "This Agreement is governed by the laws of the State of California. "
            "The parties also maintain offices in New York and Texas."
        )
        meta = MetadataExtractor().extract_metadata(text)
        assert meta.jurisdiction == "California"
        # Geography should include all mentioned tokens without duplicates
        assert "California" in meta.geography_mentioned
        assert "New York" in meta.geography_mentioned
        assert "Texas" in meta.geograpclahy_mentioned

    def test_extracts_industry_from_keywords(self):
        text = "We provide a SaaS analytics platform."
        meta = MetadataExtractor().extract_metadata(text)
        assert meta.industry == "Software"

    def test_handles_unknowns_gracefully(self):
        text = "This is a letter about a picnic at the park."
        meta = MetadataExtractor().extract_metadata(text)
        assert meta.agreement_type == "Unknown"
        assert meta.jurisdiction == "Unknown"
        assert meta.geography_mentioned == []
        assert meta.industry == "Unknown"


