import { bootstrap, JobQueueService } from '@vendure/core';
import { config } from './vendure-config';

bootstrap(config)
  .then(async (app) => {
    console.log('--------------------------------------------------');
    console.log('Vendure Shop API running on: http://localhost:3000/shop-api');
    console.log('Vendure Admin UI running on: http://localhost:5001/admin');
    console.log('--------------------------------------------------');
    
    console.log('Starting JobQueueService...');
    await app.get(JobQueueService).start();
    console.log('JobQueueService active and listening for background tasks.');
  })
  .catch((err) => {
    console.error('Error bootstrapping Vendure server:', err);
    process.exit(1);
  });

