# Security Checklist – L10 Automatic Warranty Request Classification

| No. | Security Item | Status | Evidence / Notes |
|---|---|---|---|
| 1 | No secrets or credentials are committed to the repository. | DONE | `.env` is ignored by `.gitignore` and is not tracked in the current Git index. A complete historical secret scan has not been performed. |
| 2 | Prediction input is validated before processing. | DONE | `src/predict.py` rejects non-string, empty and whitespace-only descriptions, and validates prediction output labels. |
| 3 | Dataset schema and category labels are validated. | DONE | Data validation and split-checking scripts verify required columns, descriptions and category labels. |
| 4 | Dependencies are explicitly version-pinned. | DONE | `requirements.txt` specifies exact versions for pandas, scikit-learn, joblib and matplotlib. No automated vulnerability scan has been performed. |
| 5 | Personal and sensitive data has undergone a documented privacy review. | NOT DONE | A formal privacy review has not been completed. The dataset and any future deployment data should be reviewed before production use. |
| 6 | Runtime environment has a healthcheck. | DONE | `scripts/healthcheck.py` checks required Python dependencies and the presence and basic structure of the raw dataset. |
| 7 | Automated tests verify important input and data-validation behavior. | DONE | `python -m unittest discover -s tests -v` currently runs 19 tests successfully. This does not replace penetration or security testing. |

## Summary

- DONE: 6 items
- NOT DONE: 1 item
- N/A: 0 items

## Security Limitations

This checklist records the security controls verified in the current prototype. It does not certify production security. Historical secret scanning, dependency vulnerability scanning, formal privacy review and penetration testing have not been completed.
