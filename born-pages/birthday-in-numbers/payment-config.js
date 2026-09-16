/* QuickAgeCalc Magical Birthday Card payment configuration.
   REVIEW MODE: keep disabled until checkout, policies and delivery are tested. */
window.QAC_BIRTHDAY_PAYMENTS={
  provider:"lemonsqueezy",
  mode:"disabled",
  currency:"USD",
  products:{
    magical:{name:"Magical Animated Card",price:4.99,checkoutUrl:""},
    stats:{name:"Card + Stats Pack",price:6.99,checkoutUrl:""},
    complete:{name:"Complete Birthday Pack",price:9.99,checkoutUrl:""}
  }
};
