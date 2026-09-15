# Google API key in a publisher snapshot

Remediated locally on 15 September 2026. [GitHub alert #2](https://github.com/nickbrazeau/ikhis/security/secret-scanning/2)

The detected value came from the `impactGoogleMapsApiKey` field in the browser configuration embedded in a saved Frontiers article page. It was present in the working HTML snapshot and its unreviewed candidate copy. No IKHIS application configuration or use of this key was found. GitHub reports its validity as unknown and identifies other public copies of the same publisher-page configuration. No request was made using the key, and no revocation is claimed.

Both local HTML copies now contain a redaction marker. The source file manifest was updated, and the unreviewed candidate was rebuilt so its provenance hashes match the sanitized files. All 51 database tables were compared before and after: the differences are confined to source-dependency hashes and candidate input hashes. Scientific records, review states and baseline tables are unchanged. Frozen releases were not edited.

The shared sanitizer now handles Google API keys as well as AWS credential metadata, across all UTF-8 filenames. The dictionary compiler rejects unsanitized inputs. The legacy influenza downloader now uses the same bounded, sanitized fetcher. A repository workflow runs the scanner on pushes and pull requests. Synthetic test examples have explicit exact-hash exceptions; a file change invalidates its exception.

Original and sanitized hashes are retained in [the redaction record](../provenance/security_redactions_2026-09-15.json). The original migration receipt is preserved, with subsequent maintenance changes recorded separately in [the post-migration change log](../../data_dictionary/provenance/post_migration_changes.json).

## GitHub follow-up

The local fix must be committed and pushed before the default branch reflects the removal. The original commit remains in Git history; no history rewrite was performed. Removing a value does not automatically close a secret-scanning alert ([GitHub guidance](https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-secret-scanning-alerts/resolving-alerts)).

The alert is still open. The available GitHub connector has no secret-alert write operation, the local Git credential helper did not provide authentication, and Chrome's fallback automation routes lack the required permissions. No security settings were relaxed to bypass these limits.

After publishing the fix, close this alert with a reason explaining that it is a third-party publisher key copied from public webpage configuration. Do not mark it revoked: only the key's owner can verify its restrictions or revoke it. Suggested resolution is **Won't fix** for the third-party credential itself, with this explanation:

> This is a Google Maps key embedded in Frontiers' public article-page configuration, captured in a research snapshot and its candidate copy. No IKHIS use was found. The repository copies have been sanitized and snapshot safeguards expanded. The key's validity/restrictions are unknown; we do not own it and have not revoked it.

Only use the last sentence about repository sanitization after the fix has been pushed. Google documents application/API restrictions for Maps keys in its [security guidance](https://developers.google.com/maps/api-security-best-practices).
