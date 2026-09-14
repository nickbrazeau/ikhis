# GitHub secret-scanning alert investigation

The alert on commit `a3e5475e` came from an AWS temporary access-key identifier inside a presigned URL in `research/cytokine/snapshots/search1.json`, line 4. The snapshot saved a public search result for a conference PDF hosted by `higherlogicdownload.s3.amazonaws.com`. There is no evidence from this finding that a project-owned AWS credential was used or exposed.

The link contained an access-key identifier, temporary security-token metadata and a request signature. It did not contain an AWS secret access key. Its recorded signing time was 2026-03-12 13:39:19 UTC, with a 3,600-second expiry: the configured URL deadline was **2026-03-12 14:39:19 UTC**, well before the September commit. AWS documents that a presigned URL expires at its configured deadline or earlier when the underlying credentials expire. [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html).

A saved search result is still repository content, so GitHub correctly recognized the credential-shaped identifier. The capture workflow should have removed these URL fields before saving the result. This was a snapshot-hygiene error.

## Local remediation

- Removed the credential, security-token and signature values from the working snapshot and its archived copy, retaining the source URL and biological text.
- Added a sanitizer and a compiler check that rejects source snapshots containing this AWS credential metadata. The sanitizer reports file paths and hashes without printing matched values.
- Scanned current research, data, report, provenance and release text files; no remaining matches were found with this targeted check. This is not a certification against every possible secret format.
- Preserved the original 0.1.0 manifest and documented the single security redaction in `releases/0.1.0/security_redactions.json`. Verification explicitly reports the exception and verifies the sanitized replacement bytes; it does not claim the original source bytes are unchanged.

These changes are local. The original Git commit and GitHub alert remain unchanged. No credentials were exercised, no AWS account changes were made, and Git history was not rewritten. The expired third-party URL does not provide a reason to rotate unrelated personal AWS credentials. The GitHub alert can be reviewed using this documented explanation.
