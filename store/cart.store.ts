import { CartCustomization, CartStore } from "@/type";
import { create } from "zustand";

// 🔴 START: Cart store with location-based pricing and platform fee deduction
// Description: Global cart state management using Zustand.
// 
// CART CALCULATIONS:
// - Each item stored with its price (already location-adjusted when added)
// - Platform fee of ₦500 is deducted from each item for vendor earnings
// - getTotalPrice() sums: (item.price + customization prices) * quantity (customer total)
// - getTotalCustomer() = getTotalPrice() (same as above)
// - getTotalPlatform() = sum of platform fees * quantity
// - getTotalVendor() = sum of vendor earnings * quantity
// - The selected location affects the price at the time of adding to cart
// - Once in cart, prices remain fixed until the user checks out
//
// PLATFORM FEE LOGIC:
// - PLATFORM_FEE = 500 (₦500 per item)
// - When adding item: platformFee = PLATFORM_FEE, vendorEarnings = price - PLATFORM_FEE
// - Fees are calculated per item, not per quantity (but multiplied in totals)
//
// CUSTOMIZATION HANDLING:
// - Items can have customizations (add-ons) that affect the final price
// - Customizations are compared by ID to group same item + same customizations together
// - Increasing qty of identical item+customizations combo increments the quantity counter
const PLATFORM_FEE = 500;
function areCustomizationsEqual(
  a: CartCustomization[] = [],
  b: CartCustomization[] = []
): boolean {
  if (a.length !== b.length) return false;

  const aSorted = [...a].sort((x, y) => x.id.localeCompare(y.id));
  const bSorted = [...b].sort((x, y) => x.id.localeCompare(y.id));

  return aSorted.every((item, idx) => item.id === bSorted[idx].id);
}

export const useCartStore = create<CartStore>((set, get) => ({
  items: [],

  addItem: (item) => {
    const customizations = item.customizations ?? [];
    // Calculate platform fee and vendor earnings per item
    const platformFee = PLATFORM_FEE;
    const vendorEarnings = item.price - PLATFORM_FEE;

    const existing = get().items.find(
      (i) =>
        i.id === item.id &&
        i.selectedLocation === item.selectedLocation &&
        areCustomizationsEqual(i.customizations ?? [], customizations)
    );

    if (existing) {
      set({
        items: get().items.map((i) =>
          i.id === item.id &&
          i.selectedLocation === item.selectedLocation &&
          areCustomizationsEqual(i.customizations ?? [], customizations)
            ? { ...i, quantity: i.quantity + 1 }
            : i
        ),
      });
    } else {
      set({
        items: [...get().items, { ...item, quantity: 1, customizations, platformFee, vendorEarnings }],
      });
    }
  },

  removeItem: (id, customizations = []) => {
    set({
      items: get().items.filter(
        (i) =>
          !(
            i.id === id &&
            areCustomizationsEqual(i.customizations ?? [], customizations)
          )
      ),
    });
  },

  increaseQty: (id, customizations = []) => {
    set({
      items: get().items.map((i) =>
        i.id === id &&
        areCustomizationsEqual(i.customizations ?? [], customizations)
          ? { ...i, quantity: i.quantity + 1 }
          : i
      ),
    });
  },

  decreaseQty: (id, customizations = []) => {
    set({
      items: get()
        .items.map((i) =>
          i.id === id &&
          areCustomizationsEqual(i.customizations ?? [], customizations)
            ? { ...i, quantity: i.quantity - 1 }
            : i
        )
        .filter((i) => i.quantity > 0),
    });
  },

  clearCart: () => set({ items: [] }),

  getTotalItems: () =>
    get().items.reduce((total, item) => total + item.quantity, 0),

  getTotalPrice: () =>
    get().items.reduce((total, item) => {
      const base = item.price;
      const customPrice =
        item.customizations?.reduce(
          (s: number, c: CartCustomization) => s + c.price,
          0
        ) ?? 0;
      return total + item.quantity * (base + customPrice);
    }, 0),

  // Total amount customer pays (same as getTotalPrice)
  getTotalCustomer: () => get().getTotalPrice(),

  // Total platform fees collected
  getTotalPlatform: () =>
    get().items.reduce((total, item) => {
      return total + item.quantity * item.platformFee;
    }, 0),

  // Total vendor earnings
  getTotalVendor: () =>
    get().items.reduce((total, item) => {
      return total + item.quantity * item.vendorEarnings;
    }, 0),
}));
