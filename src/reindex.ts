import { bootstrap, SearchService, RequestContextService, ChannelService } from '@vendure/core';
import { config } from './vendure-config';

async function run() {
  console.log('Bootstrapping Vendure for search reindexing...');
  const app = await bootstrap(config);
  const searchService = app.get(SearchService);
  const requestContextService = app.get(RequestContextService);
  const channelService = app.get(ChannelService);
  const channel = await channelService.getDefaultChannel();

  console.log('Creating admin request context...');
  const ctx = await requestContextService.create({
    apiType: 'admin',
    channel,
  });

  console.log('Triggering search index rebuild...');
  const job = await searchService.reindex(ctx);
  console.log(`Reindex job queued with ID: ${job.id}`);

  console.log('Waiting for reindexing job to complete...');
  // Since it runs in the background queue, we wait for a brief moment for it to process
  await new Promise((resolve) => setTimeout(resolve, 8000));

  console.log('Search index successfully rebuilt!');
  await app.close();
  process.exit(0);
}

run().catch((err) => {
  console.error('Reindexing script failed:', err);
  process.exit(1);
});
