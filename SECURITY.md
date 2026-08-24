# Security Policy

## Reporting a vulnerability

Please do not publish API keys, credentials, private workflow exports, or vulnerability details in a public issue.

If you discover a security problem, contact the repository owner privately through their GitHub profile before publishing details.

## API keys

JSON Logic Agent reads the OpenRouter API key from a local `.env` file.

Never commit a real key. The repository intentionally contains only `.env.example` with an empty `OPENROUTER_API_KEY=` value.

If a key is accidentally committed, revoke/rotate it immediately. Removing the value in a later commit is not enough because Git history may still contain it.

## n8n workflow privacy

Exported n8n workflows can contain sensitive information such as:

- webhook URLs and paths
- internal hostnames and API endpoints
- customer or business data embedded in node parameters
- email addresses
- credential names and credential IDs
- code snippets
- expressions and business rules

JSON Logic Agent does not need credential secret values to understand a workflow. Review workflow exports before sharing them publicly.

The deterministic `n8n --report-only` analysis runs locally. AI-assisted semantic analysis sends analysis context to the configured OpenRouter/model provider.

Do not use AI-assisted analysis on confidential workflow data unless your organization permits that data to be sent to the configured provider.

## Generated reports

Markdown and PDF reports can repeat information found in the source workflow. Treat generated reports with the same sensitivity as the original JSON.

For local work, `reports/` and `exports/` are ignored by Git so generated analyses can be kept out of commits by default.

## Public examples

Only synthetic/example workflows should be committed to this public repository. Do not commit production n8n exports without first removing confidential data, endpoints, identifiers, and credential references that should remain private.
