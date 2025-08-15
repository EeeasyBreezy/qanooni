import json
import mimetypes
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode
import urllib.request
import urllib.error

from .dtos.AggregationResultDTO import AggregationResultDTO
from .dtos.DashboardStatsDTO import DashboardStatsDTO
from .dtos.PaginationDTO import PaginationDTO
from .dtos.QueryResponseDTO import QueryResponseDTO
from .dtos.QueryRowDTO import QueryRowDTO


class HttpError(Exception):
    def __init__(self, status: int, body: Optional[str] = None):
        super().__init__(f"HTTP {status}: {body}")
        self.status = status
        self.body = body


class ApiClient:
    def __init__(self, base_url: str) -> None:
        self._base = base_url.rstrip("/")

    def _request(self, method: str, path: str, *, headers: Optional[Dict[str, str]] = None, data: Optional[bytes] = None) -> Dict[str, Any]:
        url = f"{self._base}{path}"
        req = urllib.request.Request(url, method=method, data=data, headers=headers or {})
        try:
            with urllib.request.urlopen(req) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8") if e.fp else None
            raise HttpError(e.code, body)

    # Dashboard combined (agreement types + jurisdictions only)
    def get_dashboard(self) -> DashboardStatsDTO:
        data = self._request("GET", "/api/dashboard")
        return DashboardStatsDTO(agreement_types=data.get("agreement_types", {}), jurisdictions=data.get("jurisdictions", {}))

    def get_agreement_types(self) -> List[AggregationResultDTO]:
        data = self._request("GET", "/api/dashboard/agreement-types")
        return [AggregationResultDTO(category=i["category"], count=int(i["count"])) for i in data]

    def get_countries(self) -> List[AggregationResultDTO]:
        data = self._request("GET", "/api/dashboard/countries")
        return [AggregationResultDTO(category=i["category"], count=int(i["count"])) for i in data]

    def get_industries(self, *, limit: int, offset: int, sort: str = "desc") -> PaginationDTO:
        qs = urlencode({"limit": limit, "offset": offset, "sort": sort})
        data = self._request("GET", f"/api/dashboard/industries?{qs}")
        items = [AggregationResultDTO(category=i["category"], count=int(i["count"])) for i in data["items"]]
        return PaginationDTO(items=items, limit=int(data["limit"]), offset=int(data["offset"]), total=int(data["total"]))

    def run_query(self, *, question: str, limit: int, offset: int) -> QueryResponseDTO:
        qs = urlencode({"question": question, "limit": limit, "offset": offset})
        data = self._request("GET", f"/api/query?{qs}")
        items = [
            QueryRowDTO(
                document=i.get("document"),
                governing_law=i.get("governing_law"),
                agreement_type=i.get("agreement_type"),
                industry=i.get("industry"),
                score=i.get("score"),
            )
            for i in data.get("items", [])
        ]
        return QueryResponseDTO(items=items, limit=int(data["limit"]), offset=int(data["offset"]), total=int(data["total"]))

    def upload_file(self, *, filepath: str, request_id: str) -> None:
        # Build multipart/form-data manually with urllib
        boundary = "----Boundary7MA4YWxkTrZu0gW"
        mime_type, _ = mimetypes.guess_type(filepath)
        mime_type = mime_type or "application/octet-stream"
        with open(filepath, "rb") as f:
            file_bytes = f.read()

        parts: List[bytes] = []
        def add_field(name: str, value: str) -> None:
            parts.append(f"--{boundary}\r\n".encode())
            parts.append(f"Content-Disposition: form-data; name=\"{name}\"\r\n\r\n".encode())
            parts.append(f"{value}\r\n".encode())

        def add_file(name: str, filename: str, content_type: str, content: bytes) -> None:
            parts.append(f"--{boundary}\r\n".encode())
            header = f"Content-Disposition: form-data; name=\"{name}\"; filename=\"{filename}\"\r\n"
            parts.append(header.encode())
            parts.append(f"Content-Type: {content_type}\r\n\r\n".encode())
            parts.append(content)
            parts.append("\r\n".encode())

        add_field("request_id", request_id)
        add_file("file", filepath.split("/")[-1], mime_type, file_bytes)
        parts.append(f"--{boundary}--\r\n".encode())
        body = b"".join(parts)

        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
        }
        # This raises HttpError on non-2xx
        self._request("POST", "/api/upload", headers=headers, data=body)


