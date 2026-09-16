# QuickAgeCalc – Magical Birthday Card launch checklist

Status: REVIEW ONLY. Do not merge to `main` until checkout, customer policies and delivery are ready.

## 1. Payment provider
Recommended launch path: Lemon Squeezy as Merchant of Record for the automated digital gift product.

Create the store, complete business/identity verification and add a bank payout method. Keep the store in test mode while integrating.

Create three products or one product with three variants:
- Magical Animated Card — USD 4.99
- Card + Stats Pack — USD 6.99
- Complete Birthday Pack — USD 9.99

Copy the reusable `/checkout/buy/...` URLs into `born-pages/birthday-in-numbers/payment-config.js` and keep `mode: "disabled"` until final test. Never use a single-use `/checkout/?cart=...` URL.

## 2. Checkout data
Pass only the minimum data required. The staged frontend is prepared to pass:
- product key
- recipient first name/nickname
- birth date
- celebration date

Do not place API keys or webhook secrets in frontend JavaScript.

## 3. Post-purchase delivery
Choose one before launch:
- MVP: manual fulfillment after paid order notification.
- Recommended: Cloudflare Worker webhook endpoint + D1/KV gift record + unique gift URL.

Recommended production flow:
1. Customer creates preview.
2. Customer chooses package.
3. Checkout opens.
4. Payment provider sends an `order_created` webhook.
5. Worker verifies the webhook signature.
6. Worker creates the gift/order record and a random public gift token.
7. Customer receives the success page and gift link.
8. Paid gift page loads the personalized fields and generated stats.

Do not rely only on the browser success redirect to confirm payment; use the webhook.

## 4. Customer-facing pages before launch
Add/review:
- Terms of Purchase / Terms of Service
- Refund Policy for digital products
- Delivery policy / what each pack includes
- Privacy Policy update naming the payment processor and explaining birthday-data usage
- Contact/support email

The checkout must clearly identify the item as a personalized digital birthday gift and state delivery format/timing.

## 5. Privacy/data minimization
A date of birth can be personal data. Store only what is required for fulfillment and define a retention period. Avoid putting full birthday details into public URLs. Use random gift tokens rather than encoding personal data in the URL.

## 6. Testing before launch
Test at minimum:
- normal birthday
- February 29 birthday in leap and non-leap celebration years
- end-of-month birthdays
- celebration date equal to birthday
- invalid date order
- long names/messages
- mobile Safari and Chrome
- payment success and cancellation
- webhook duplicate delivery/idempotency
- refund flow
- unique gift link access
- static PNG download

## 7. Activation steps
Only after the above passes:
1. Put live checkout URLs in `payment-config.js`.
2. Change `mode` from `disabled` to `live`.
3. Remove `<meta name="robots" content="noindex,nofollow">` from the product page.
4. Merge the review PR to `main`.
5. Add the page to sitemap and global navigation/homepage CTA.
6. Verify Cloudflare deployment and run one real low-value purchase end-to-end.
