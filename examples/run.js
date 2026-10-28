// Minimal example: run the remote-jobs-worldwide-scraper Actor and print the results.
// Usage: APIFY_TOKEN=... node run.js   (Node 18 or later, npm install apify-client)
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set the APIFY_TOKEN environment variable first.');
    process.exit(1);
}

const client = new ApifyClient({ token });

const input = {
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
};

const run = await client.actor('bibian/remote-jobs-worldwide-scraper').call(input);
const { items } = await client.dataset(run.defaultDatasetId).listItems();

console.log(`${items.length} results`);
for (const item of items) {
    const pay = item.salaryMin ?? item.salaryMax
        ? `${item.salaryMin ?? '-'}-${item.salaryMax ?? '-'} ${item.salaryCurrency ?? ''}/${item.salaryPeriod ?? '?'}`
        : 'n/a';
    console.log(`${item.title} | ${item.companyName ?? 'confidential'} | ${item.locationLabel ?? 'remote'} | ${item.source} | ${pay}`);
}
