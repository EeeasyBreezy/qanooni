import re
from typing import List, Optional

from app.services.interfaces.IMetadataExtractor import IMetadataExtractor
from app.services.model.DocumentMetadata import DocumentMetadata


class MetadataExtractor(IMetadataExtractor):
    AGREEMENT_KEYWORDS = {
        "nda": "Non-Disclosure Agreement",
        "non-disclosure agreement": "Non-Disclosure Agreement",
        "confidentiality agreement": "Non-Disclosure Agreement",
        "msa": "Master Services Agreement",
        "master services agreement": "Master Services Agreement",
        "service agreement": "Service Agreement",
        "services agreement": "Service Agreement",
        "employment agreement": "Employment Agreement",
        "lease agreement": "Lease Agreement",
        "supply agreement": "Supply Agreement",
        "license agreement": "License Agreement",
        "licence agreement": "License Agreement",
        "data processing agreement": "Data Processing Agreement",
        "dpa": "Data Processing Agreement",
    }

    INDUSTRY_KEYWORDS = {
        "saas": "Software",
        "software": "Software",
        "healthcare": "Healthcare",
        "pharma": "Pharmaceuticals",
        "pharmaceutical": "Pharmaceuticals",
        "bank": "Finance",
        "fintech": "Finance",
        "finance": "Finance",
        "insurance": "Insurance",
        "energy": "Energy",
        "retail": "Retail",
        "telecom": "Telecommunications",
        "telecommunications": "Telecommunications",
        "manufacturing": "Manufacturing",
        "logistics": "Logistics",
        "media": "Media",
    }

    # Short curated set of common jurisdictions; extend as needed
    JURISDICTIONS = [
        # US states
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
        "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
        "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
        "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
        "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
        "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
        "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
        "Wisconsin", "Wyoming",
        # Countries (sample)
        "United States", "USA", "Canada", "United Kingdom", "UK", "Germany", "France", "Spain",
        "Italy", "Netherlands", "Australia", "India", "China", "Japan", "Brazil", "Mexico",
        "United Arab Emirates", "UAE", "Saudi Arabia", "Singapore",
        # Other common jurisdictions
        "Delaware", "England and Wales", "Scotland", "Ireland",
    ]

    def extract_metadata(self, text: str) -> DocumentMetadata:
        agreement_type = self._extract_agreement_type(text)
        jurisdiction = self._extract_jurisdiction(text)
        geography = self._extract_geographies(text)
        industry = self._extract_industry(text)

        meta = DocumentMetadata()
        meta.agreement_type = agreement_type or "Unknown"
        meta.jurisdiction = jurisdiction or "Unknown"
        meta.geography_mentioned = geography
        meta.industry = industry or "Unknown"
        return meta

    def _extract_agreement_type(self, text: str) -> Optional[str]:
        lowered = text.lower()
        # Check explicit keywords
        for key, label in self.AGREEMENT_KEYWORDS.items():
            if key in lowered:
                return label
        # Heuristic: look for "this <something> agreement"
        m = re.search(r"this\s+([\w\- ]+)\s+agreement", lowered)
        if m:
            raw = m.group(1).strip()
            # Normalize some common forms
            if "service" in raw:
                return "Service Agreement"
            if "master" in raw and "service" in raw:
                return "Master Services Agreement"
            if "employment" in raw:
                return "Employment Agreement"
            if "license" in raw or "licence" in raw:
                return "License Agreement"
        return None

    def _extract_jurisdiction(self, text: str) -> Optional[str]:
        # Try to extract from governing law clause
        # Examples: "governed by the laws of the State of California" or "governing law: England and Wales"
        m = re.search(
            r"govern(?:ed|ing)\s+by\s+(?:the\s+laws\s+of\s+)?([A-Za-z ,&-]+)",
            text,
            re.IGNORECASE,
        )
        if m:
            candidate = m.group(1).strip().rstrip(". ")
            # Return matched candidate if it resembles a known jurisdiction
            for j in self.JURISDICTIONS:
                if j.lower() in candidate.lower():
                    return j
            return candidate

        # Fallback: scan for known jurisdiction tokens present anywhere
        for j in self.JURISDICTIONS:
            if re.search(rf"\b{re.escape(j)}\b", text, re.IGNORECASE):
                return j
        return None

    def _extract_geographies(self, text: str) -> List[str]:
        found: List[str] = []
        for j in self.JURISDICTIONS:
            if re.search(rf"\b{re.escape(j)}\b", text, re.IGNORECASE):
                if j not in found:
                    found.append(j)
        return found

    def _extract_industry(self, text: str) -> Optional[str]:
        lowered = text.lower()
        for key, label in self.INDUSTRY_KEYWORDS.items():
            if key in lowered:
                return label
        return None