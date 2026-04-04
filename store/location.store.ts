import { create } from "zustand";
import type { LocationName } from "@/type";

// 🔴 START: Location store
// Description: Global location state to keep the selected delivery location across screens.
export type LocationState = {
  selectedLocation?: LocationName;
  setLocation: (location: LocationName) => void;
};

export const LOCATIONS: LocationName[] = [
  "Isheri Berger",
  "Lekki",
  "First Tark",
  "Akute",
  "Arepo",
  "Magoro",
];

const useLocationStore = create<LocationState>((set) => ({
  selectedLocation: undefined,
  setLocation: (location) => set({ selectedLocation: location }),
}));

export default useLocationStore;
// 🔴 END: Location store
