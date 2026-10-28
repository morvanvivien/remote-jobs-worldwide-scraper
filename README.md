# Remote Jobs Worldwide Scraper: 8 Job Boards, One Schema

> **Run it now, no code: [remote-jobs-worldwide-scraper on the Apify Store](https://apify.com/bibian/remote-jobs-worldwide-scraper)** &nbsp;|&nbsp; $0.0012 per result &nbsp;|&nbsp; no login, no browser

Remote job postings are scattered across a dozen boards, each with its own fields, filters and pagination. This Actor queries 8 of the biggest remote-work boards in one run — [RemoteOK](https://remoteok.com), [Remotive](https://remotive.com), [We Work Remotely](https://weworkremotely.com), [Jobicy](https://jobicy.com), [Working Nomads](https://www.workingnomads.com), [Hacker News "Who is Hiring"](https://news.ycombinator.com), [Wellfound](https://wellfound.com) and [Get on Board](https://www.getonbrd.com) — and maps every posting to one unified schema, deduplicated across sources. This guide shows how to get worldwide remote job postings as clean structured data, from the console or from code.

Searches this page answers: remote jobs scraper, worldwide remote job postings, RemoteOK API, Remotive API, We Work Remotely scraper, remote job boards aggregator.

## What you get from the Remote Jobs Worldwide scraper

- Every remote posting from 8 major boards, newest first, with title, company, location, employment type and remote mode — in one unified schema regardless of source.
- Salary ranges (`salaryMin`, `salaryMax`, `salaryCurrency`, `salaryPeriod`) when the posting shows them.
- Skills as a list, plus location label, publication and expiry dates.
- Deduplication across sources: the same posting cross-listed on RemoteOK and We Work Remotely only counts once.
- Optional full description as plain text, with no personal data.

Export the dataset as JSON, CSV or Excel, or read it through the Apify API. A real sample (five results, one per source board, no personal data) is in [`sample-output.json`](sample-output.json).

## Output fields

| Field | What it is |
|---|---|
| `id`, `url` | Stable identifier (`<source>:<native id>`) and public link of the posting |
| `title` | Job title as published |
| `companyName`, `companyUrl` | Employer name and page; `companyName` is `null` when hidden (`confidentialCompany: true`) |
| `locationLabel`, `city`, `region`, `postalCode`, `country` | Location as displayed by the site, when published |
| `remote` | Always `remote`: every source in this pack is a remote-only board |
| `employmentType` | `full_time`, `part_time`, `contract`, `freelance`, `internship`, `apprenticeship`, `temporary` or `unknown` |
| `salaryMin`, `salaryMax`, `salaryCurrency`, `salaryPeriod` | Salary range, currency (ISO 4217) and period (`hour`, `day`, `month`, `year`) when shown |
| `datePosted`, `validThrough` | Publication and expiry dates, ISO 8601 |
| `description` | Plain-text description, only when `includeDescriptions` is on. No personal data. |
| `experienceLevel`, `industry` | As named by the site, when published |
| `skills` | Array of skills listed by the site, if any |
| `source`, `sourceId` | Host name of the source site and its native identifier |
| `scrapedAt` | Extraction timestamp, ISO 8601 |

Site-specific fields are kept in addition to these (never in place of them) — for example Jobicy's raw `geo` tag, RemoteOK's `tags`, or Wellfound's role slug and compensation string.

## Use cases

- **Search remote jobs across tech, sales, design and ops in one run**, instead of buying and maintaining 8 separate scrapers.
- **Compare pay across boards**: every record shares the same `salaryMin`/`salaryMax` and `employmentType` fields, whichever site it came from.
- **Monitor new postings daily**: schedule it with `onlyNew` checked and `publishedWithinDays: 1` to get, and pay for, only what is new since the last run.
- **Feed a job board or a newsletter**: use the unified schema and the canonical `url` to power a niche remote-job board or alert.

## Input

| Field | What it does |
|---|---|
| `keywords` | Job title, skill or trade, for example `backend engineer`. Empty means every posting. |
| `region` | Keep only postings open to this part of the world: `anywhere`, `europe`, `americas`, `asia`, `africa` or `oceania`. Best effort, based on whatever location the source itself publishes. |
| `location` | City or region text, used only by the sources that support it; ignored by the others. |
| `sources` | Which of the 8 remote job boards to query in this run. Defaults to all 8. |
| `publishedWithinDays` | Keep only postings published in the last N days. Use `1` for a daily monitoring run. |
| `maxItems` | The run stops once this many postings are saved, across all sources combined (default 50). |
| `includeDescriptions` | Add the job description as plain text (off by default, for a fast run). |
| `onlyNew` | For scheduled runs: skip postings an earlier run of this same search already delivered. |

Example input:

```json
{
  "keywords": "backend engineer",
  "region": "anywhere",
  "sources": [
    "remoteok",
    "remotive",
    "weworkremotely",
    "jobicy",
    "workingnomads",
    "hackernews",
    "wellfound",
    "getonbrd"
  ],
  "publishedWithinDays": 7,
  "maxItems": 100,
  "includeDescriptions": false
}
```

## Four ways to use it

### 1. Apify console, no code

1. Open [the Actor page](https://apify.com/bibian/remote-jobs-worldwide-scraper) and click **Try for free** (a free Apify account is enough).
2. Fill in the input form (keywords, region, sources and the maximum number of results) and click **Start**.
3. When the run finishes, open the **Output** tab, check the table, then **Export** as CSV, Excel or JSON.
4. For a daily alert, open **Schedules**, create a daily schedule for the Actor with `onlyNew` checked, and, optionally, add an integration that sends new results to Slack, e-mail or Google Sheets.

### 2. Apify API with JavaScript

```bash
npm install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
node examples/run.js
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('bibian/remote-jobs-worldwide-scraper').call({
    "keywords": "backend engineer",
    "region": "anywhere",
    "publishedWithinDays": 7,
    "maxItems": 100,
    "includeDescriptions": false
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
    console.log(`${item.title} | ${item.companyName} | ${item.source} | ${item.salaryMin ?? '-'}-${item.salaryMax ?? '-'} ${item.salaryCurrency ?? ''}`);
}
```

The complete file is [`examples/run.js`](examples/run.js) (ES module, Node 18 or later).

### 3. Apify API with Python

```bash
pip install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
python examples/run.py
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("bibian/remote-jobs-worldwide-scraper").call(run_input={
    "keywords": "backend engineer",
    "region": "anywhere",
    "publishedWithinDays": 7,
    "maxItems": 100,
    "includeDescriptions": False,
})

for item in client.dataset(run.default_dataset_id).iterate_items():
    print(f"{item['title']} | {item.get('companyName')} | {item.get('source')} | {item.get('salaryMin')}-{item.get('salaryMax')} {item.get('salaryCurrency')}")
```

The complete file is [`examples/run.py`](examples/run.py). Never put your token in the code: read it from the `APIFY_TOKEN` environment variable as above.

### 4. Zapier, Make and no-code tools

The Actor is listed on the Apify Store, so any integration that can call an Apify Actor (Zapier, Make, n8n, or a plain webhook) can trigger a run and read the resulting dataset without writing any code.

## Pricing

Pay per result: **$0.0012 per result**. You pay only for the results saved to the dataset. Apify's free plan includes monthly credits, enough to try it on a few hundred results. Prices are those shown on the [Store page](https://apify.com/bibian/remote-jobs-worldwide-scraper) when this guide was written; the Store page is the reference.

## Limits and honest notes

- Only what each board publishes is collected. Many postings do not show a salary, so `salaryMin` and `salaryMax` are often `null` (this is visible in `sample-output.json`).
- `region` is a best-effort filter: most remote boards publish a free-text location, not a structured continent field, so an unclear or missing location is kept rather than dropped.
- `employmentType` is read from each site's own field when it has one; when a source carries none, it is inferred from the title and description, and left `unknown` rather than guessed when nothing matches.
- The dataset contains job postings only. Recruiter and candidate contact details are never exported; only company names appear.
- Postings are the public ones: anything behind a login is out of scope.
- This is an unofficial tool, not affiliated with RemoteOK, Remotive, We Work Remotely, Jobicy, Working Nomads, Hacker News, Wellfound or Get on Board. Check each site's terms and the data protection rules that apply to your use.

## FAQ

**Does it need a browser or a proxy?**
No. The Actor reads the data directly from each source, so runs are fast and cheap.

**How do I only get new postings every day?**
Set `publishedWithinDays` to `1`, check `onlyNew`, and schedule the Actor once a day. Each run then returns, and charges, only what is new since the last run.

**Can I query only some of the 8 boards?**
Yes, set `sources` to any subset, for example `["remoteok", "remotive"]`.

**Are postings deduplicated between boards?**
Yes. The same job cross-listed on two boards is saved only once, keyed by a stable per-source identifier.

**Can I get the data in Excel or Google Sheets?**
Yes. Export the dataset as CSV, Excel or JSON from the Apify console, or connect the Apify Google Sheets integration.

## Try it

**[Open remote-jobs-worldwide-scraper on the Apify Store](https://apify.com/bibian/remote-jobs-worldwide-scraper)**

The code in `examples/` is released under the MIT license (see [LICENSE](LICENSE)). The data belongs to its original publishers.
