import { InitialData, LanguageCode, Permission } from '@vendure/core';

export const initialData: InitialData = {
  paymentMethods: [
    {
      name: 'Standard Payment',
      handler: {
        code: 'dummy-payment-handler',
        arguments: [{ name: 'automaticSettle', value: 'true' }],
      },
    },
  ],
  roles: [
    {
      code: 'administrator',
      description: 'Administrator',
      permissions: [Permission.SuperAdmin],
    },
  ],
  defaultLanguage: LanguageCode.en,
  countries: [
    { name: 'United States', code: 'US', zone: 'Americas' },
    { name: 'United Kingdom', code: 'GB', zone: 'Europe' },
    { name: 'India', code: 'IN', zone: 'Asia' },
  ],
  defaultZone: 'Americas',
  taxRates: [
    { name: 'Standard Tax', percentage: 20 },
  ],
  shippingMethods: [
    { name: 'Standard Shipping', price: 500 },
  ],
  collections: [
    {
      name: 'Electronics',
      filters: [
        {
          code: 'facet-value-filter',
          args: { facetValueNames: ['Electronics'], containsAny: false },
        },
      ],
    },
    {
      name: 'Appliances',
      filters: [
        {
          code: 'facet-value-filter',
          args: { facetValueNames: ['Appliances'], containsAny: false },
        },
      ],
    },
    {
      name: 'Furniture',
      filters: [
        {
          code: 'facet-value-filter',
          args: { facetValueNames: ['Furniture'], containsAny: false },
        },
      ],
    },
  ],
};
