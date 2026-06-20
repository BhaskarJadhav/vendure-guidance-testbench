import { bootstrap } from '@vendure/core';
import { populate } from '@vendure/core/cli';
import { config } from './vendure-config';
import path from 'path';
import fs from 'fs';

const productsCsvFile = path.join(__dirname, 'products.csv');
const initialDataFile = path.join(__dirname, 'initial-data.json');

const initialData = JSON.parse(fs.readFileSync(initialDataFile, 'utf-8'));

const populateConfig = {
  ...config,
  apiOptions: {
    ...config.apiOptions,
    port: 3005,
  },
  dbConnectionOptions: {
    ...config.dbConnectionOptions,
    synchronize: true,
  },
};

console.log('Starting database population process with official Vendure catalog...');
populate(
  () => bootstrap(populateConfig),
  initialData,
  productsCsvFile
)
  .then((app) => {
    console.log('--------------------------------------------------');
    console.log('Database successfully populated with official products and categories!');
    console.log('--------------------------------------------------');
    return app.close();
  })
  .then(() => {
    process.exit(0);
  })
  .catch((err) => {
    console.error('Error during population:', err);
    process.exit(1);
  });
