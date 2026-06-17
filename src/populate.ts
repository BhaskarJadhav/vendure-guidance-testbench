import { bootstrap } from '@vendure/core';
import { populate } from '@vendure/core/cli';
import { config } from './vendure-config';
import { initialData } from './my-initial-data';
import path from 'path';

const productsCsvFile = path.join(__dirname, 'products.csv');

const populateConfig = {
  ...config,
  dbConnectionOptions: {
    ...config.dbConnectionOptions,
    synchronize: true,
  },
};

console.log('Starting database population process...');
populate(
  () => bootstrap(populateConfig),
  initialData,
  productsCsvFile
)
  .then((app) => {
    console.log('--------------------------------------------------');
    console.log('Database successfully populated with products and categories!');
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
