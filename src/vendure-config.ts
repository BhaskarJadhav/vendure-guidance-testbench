import {
  dummyPaymentHandler,
  DefaultJobQueuePlugin,
  DefaultSearchPlugin,
  VendureConfig,
} from '@vendure/core';
import { AssetServerPlugin } from '@vendure/asset-server-plugin';
import { AdminUiPlugin } from '@vendure/admin-ui-plugin';
import path from 'path';
import dotenv from 'dotenv';

dotenv.config();

const IS_DEV = process.env.APP_ENV === 'dev' || process.env.NODE_ENV !== 'production';

export const config: VendureConfig = {
  apiOptions: {
    port: parseInt(process.env.PORT || '3000'),
    apiPath: 'shop-api',
    adminApiPath: 'admin-api',
    // In development, allow playground for testing
    ...(IS_DEV ? {
      adminApiPlayground: {
        settings: { 'request.credentials': 'include' },
      },
      shopApiPlayground: {
        settings: { 'request.credentials': 'include' },
      },
    } : {}),
  },
  authOptions: {
    tokenMethod: ['bearer', 'cookie'],
    superadminCredentials: {
      identifier: process.env.SUPERADMIN_USERNAME || 'superadmin',
      password: process.env.SUPERADMIN_PASSWORD || 'superadmin',
    },
    cookieOptions: {
      secret: process.env.COOKIE_SECRET || 'cookie-secret-12345678',
    },
  },
  dbConnectionOptions: {
    type: 'postgres',
    // We use synchronize: true only in development/testbench to easily create tables
    synchronize: true,
    logging: false,
    database: process.env.DB_NAME || 'vendure',
    schema: 'public',
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432'),
    username: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'postgres',
  },
  paymentOptions: {
    paymentMethodHandlers: [dummyPaymentHandler],
  },
  customFields: {},
  plugins: [
    AssetServerPlugin.init({
      route: 'assets',
      assetUploadDir: path.join(__dirname, '../static/assets'),
      // Serve assets locally on the VM's port
      assetUrlPrefix: undefined,
    }),
    DefaultJobQueuePlugin.init({}),
    DefaultSearchPlugin.init({
      bufferUpdates: false,
    }),
    AdminUiPlugin.init({
      route: 'admin',
      port: 5001,
      adminUiConfig: {
        apiHost: 'auto',
        apiPort: 'auto',
      },
    }),
  ],
};
