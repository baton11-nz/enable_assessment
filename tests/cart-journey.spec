import { test, expect } from '@playwright/test';

const USERNAME = 'standard_user';
const PASSWORD = 'secret_sauce';

test.describe('Test Cart Journey', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('Login > add two products > view cart > verify cart controls', async ({ page }) => {
    // Login
    await page.goto('/');
    await login(page);

    // Open first product: Sauce Labs Backpack
    // Add Sauce Labs Backpack product to cart
    // Return to Product page
      await addProductFromInventory(page, 'Sauce Labs Backpack');
      await expect(page.locator('.shopping_cart_badge')).toHaveText('1');

    // Open second product: Sauce Labs Bike Light
    // Add Sauce Labs Bike Light product to cart
    await addProductFromInventory(page, 'Sauce Labs Bike Light');
    await expect(page.locator('.shopping_cart_badge')).toHaveText('2');

    // View cart
    await page.locator('.shopping_cart_link').click();
    await expect(page).toHaveURL(/cart\.html/);
    await expect(page.locator('.title')).toHaveText('Your Cart');

    // Verify products
    await expect(page.getByText('Sauce Labs Backpack', { exact: true })).toBeVisible();

    await expect(page.getByText('Sauce Labs Bike Light', { exact: true })).toBeVisible();

    // Verify points
    // a. Remove button exists per product
    await expect(page.locator('[data-test="remove-sauce-labs-backpack"]')).toBeVisible();

    await expect(page.locator('[data-test="remove-sauce-labs-bike-light"]')).toBeVisible();

    // b. Continue Shopping exists
    await expect(page.locator('[data-test="continue-shopping"]')).toBeVisible();

    // c. Checkout exists
    await expect(page.locator('[data-test="checkout"]')).toBeVisible();});

});

async function login(page: import('@playwright/test').Page) {
  await page.locator('#user-name').fill(USERNAME);
  await page.locator('#password').fill(PASSWORD);
  await page.locator('#login-button').click();

  await expect(page.locator('.title')).toHaveText('Products');
}

async function addProductFromInventory(
  page: import('@playwright/test').Page,
  productName: string
) {
  await page.getByText(productName, { exact: true }).click();

  await expect(page.locator('.inventory_details_name')).toHaveText(productName);

  await page.locator('[data-test="add-to-cart"]').click();

  await page.locator('[data-test="back-to-products"]').click();

  await expect(page.locator('.title')).toHaveText('Products');
}
