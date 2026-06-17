import { bootstrap } from '@vendure/core';
import { config } from './vendure-config';

bootstrap(config)
  .then(() => {
    console.log('--------------------------------------------------');
    console.log('Vendure Shop API running on: http://localhost:3000/shop-api');
    console.log('Vendure Admin UI running on: http://localhost:5001/admin');
    console.log('--------------------------------------------------');
  })
  .catch((err) => {
    console.error('Error bootstrapping Vendure server:', err);
    process.exit(1);
  });
