# Get Drug Info

**Example**

- Method: `GET`
- Base URL: `http://localhost:8000/api/scan/`
- Param: `code`, type: `str`
- Example:
```url
http://localhost:8000/api/scan/?code=05909990840229
```

**Response**
- *When found*
```json
{
    "found": true,
    "drug": {
        "name": "Heviran",
        "common_name": "Aciclovirum",
        "power": "800 mg",
        "form": "Tabletki powlekane",
        "package_size": null,
        "marketing_authorization_holder": "Zakłady Farmaceutyczne POLPHARMA S.A.",
        "marketing_authorization_number": "08402",
        "active_substance": "Aciclovirum",
        "code_info": {
            "value": "05909990840229",
            "type": "GTIN"
        },
        "atc_code": "J05AB01",
        "expiration_date": "Bezterminowe",
        "procedure_type": "NAR",
        "specimen_type": "Ludzki"
    }
}
```

- *When not found*
```json
{
    "found": false,
    "scanned_code": "05909990840228",
    "identified_type": "GTIN"
}
```