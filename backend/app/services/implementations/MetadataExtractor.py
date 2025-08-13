import re
from typing import List, Optional, Tuple

from flashtext import KeywordProcessor
from rapidfuzz import process, fuzz
from geotext import GeoText
import us

from app.services.interfaces.IMetadataExtractor import IMetadataExtractor
from app.services.model.DocumentMetadata import DocumentMetadata


class MetadataExtractor(IMetadataExtractor):
    def __init__(self) -> None:
        self._agreement_kp = self._build_agreement_keyword_processor()
        self._industry_kp = self._build_industry_keyword_processor()

    def extract_metadata(self, text: str) -> DocumentMetadata:
        agreement_type = self._detect_agreement_type(text)
        jurisdiction, geos = self._extract_geo_and_jurisdiction(text)
        industry = self._detect_industry(text)

        meta = DocumentMetadata()
        meta.agreement_type = agreement_type or "Unknown"
        meta.jurisdiction = jurisdiction or "Unknown"
        meta.geography_mentioned = geos
        meta.industry = industry or "Unknown"
        return meta

    # -------- Agreement type --------
    def _build_agreement_keyword_processor(self) -> KeywordProcessor:
        kp = KeywordProcessor(case_sensitive=False)
        mapping = {
            # Non-disclosure
            "nda": "Non-Disclosure Agreement",
            "non disclosure agreement": "Non-Disclosure Agreement",
            "non-disclosure agreement": "Non-Disclosure Agreement",
            "confidentiality agreement": "Non-Disclosure Agreement",
            # Master/Service
            "msa": "Master Services Agreement",
            "master services agreement": "Master Services Agreement",
            "master service agreement": "Master Services Agreement",
            "service agreement": "Service Agreement",
            "services agreement": "Service Agreement",
            # Employment
            "employment agreement": "Employment Agreement",
            # License
            "license agreement": "License Agreement",
            "licence agreement": "License Agreement",
            # Supply/Lease
            "supply agreement": "Supply Agreement",
            "lease agreement": "Lease Agreement",
            # DPA
            "data processing agreement": "Data Processing Agreement",
            "dpa": "Data Processing Agreement",
        }
        for k, v in mapping.items():
            kp.add_keyword(k, v)
        return kp

    def _detect_agreement_type(self, text: str) -> Optional[str]:
        found = self._agreement_kp.extract_keywords(text)
        if found:
            # Return the most frequent/canonical label
            return max(set(found), key=found.count)
        # Heuristic: "this ... agreement"
        m = re.search(r"this\s+([\w\- ]+)\s+agreement", text, flags=re.I)
        if m:
            raw = m.group(1).lower()
            # try fuzzy against canon labels
            candidates = [
                "Non-Disclosure Agreement",
                "Master Services Agreement",
                "Service Agreement",
                "Employment Agreement",
                "License Agreement",
                "Supply Agreement",
                "Lease Agreement",
                "Data Processing Agreement",
            ]
            match = process.extractOne(raw, candidates, scorer=fuzz.WRatio)
            if match and match[1] >= 80:
                return match[0]
            if "service" in raw:
                return "Service Agreement"
        return None

    # -------- Geography & Jurisdiction --------
    def _extract_geo_and_jurisdiction(self, text: str) -> Tuple[Optional[str], List[str]]:
        # GeoText locations (cities/countries) + US states via 'us' helper
        geo = GeoText(text)
        locs = set(geo.cities) | set(geo.countries)
        # Add state names and abbreviations
        for state in us.states.STATES:
            if state.name in text or state.abbr in text:
                locs.add(state.name)
        all_geos_raw = list(locs)
        all_geos = [self._normalize_geo_name(g) for g in all_geos_raw]
        all_geos = [g for g in all_geos if g]

        # Jurisdiction via clause cues
        jurisdiction = None
        m = re.search(r"govern(?:ed|ing)\s+by\s+(?:the\s+laws\s+of\s+)?([A-Za-z ,&-]+)", text, re.I)
        if m:
            span = m.group(1)
            # pick first geo contained in the span
            for g in all_geos:
                if g.lower() in span.lower():
                    jurisdiction = g
                    break
            if not jurisdiction:
                # try fuzzy selection from geos
                if all_geos:
                    best = process.extractOne(span, all_geos, scorer=fuzz.WRatio)
                    if best and best[1] >= 85:
                        jurisdiction = best[0]

        if not jurisdiction and all_geos:
            jurisdiction = all_geos[0]

        # de-dup while preserving order
        seen = set()
        unique_geos = []
        for g in all_geos:
            if g not in seen:
                seen.add(g)
                unique_geos.append(g)
        return jurisdiction, unique_geos

    def _normalize_geo_name(self, name: str) -> str:
        n = name.strip()
        n = re.sub(r"^(state of|commonwealth of)\s+", "", n, flags=re.I)
        n = re.sub(r"^the\s+", "", n, flags=re.I)
        # Title-case common patterns; keep abbreviations like UK/USA
        if n.upper() in {"UK", "USA", "UAE"}:
            return n.upper()
        return n.title()

    # -------- Industry --------
    def _build_industry_keyword_processor(self) -> KeywordProcessor:
        kp = KeywordProcessor(case_sensitive=False)
        mapping = {
            "saas": "Software",
            "software": "Software",
            "healthcare": "Healthcare",
            "pharma": "Pharmaceuticals",
            "pharmaceutical": "Pharmaceuticals",
            "bank": "Finance",
            "banking": "Finance",
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
        for k, v in mapping.items():
            kp.add_keyword(k, v)
        return kp

    def _detect_industry(self, text: str) -> Optional[str]:
        found = self._industry_kp.extract_keywords(text)
        if found:
            return max(set(found), key=found.count)
        return None