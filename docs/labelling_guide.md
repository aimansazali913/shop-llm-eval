# Labelling Guide

## Label Definitions

- **order_status**: Use when the customer asks where their order, shipment, or parcel is.
- **product_enquiry**: Use when the customer asks about price, stock availability, clothing sizes, or product features.
- **payment_issue**: Use when the customer has paid but encountered a problem, failed payment, needs a refund, or got a wrong charge.
- **complaint**: Use when the customer is unhappy or dissatisfied with the product or service, and there is no more specific request.
- **other**: Use for expressions of thanks, greetings, spam, or anything else that doesn't fit the categories above.

## Tie-Break Rule

If a message fits into two or more labels, apply the following rules:

1. **Core Intent:** Label the message based on **what the customer wants done**.
2. **Priority Order (if still unclear):**
   1. `payment_issue` (Highest priority)
   2. `complaint`
   3. `order_status`
   4. `product_enquiry`
   5. `other` (Lowest priority)

_Note: Once these labels and rules are set, do not change them afterwards. If you change them later, you must re-label everything._
