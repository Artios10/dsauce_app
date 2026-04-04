import { Alert, Image, Text, TouchableOpacity, Platform } from "react-native";
import { MenuItem } from "@/type";
import { useCartStore } from "@/store/cart.store";
import useLocationStore from "@/store/location.store";

// 🔴 START: Menu item card component
// Description: Displays individual menu items with pricing and "Add to Cart" functionality.
//
// LOCATION-BASED PRICING:
// - Retrieves the user's selectedLocation from the location store
// - Looks up the price for that specific location: prices[selectedLocation]
// - If location not selected, displays placeholder text and prevents adding to cart
// - When user adds to cart, the item is stored with the location-specific price
//
// IMAGE HANDLING:
// - Tries to use local image first: item.image (require statement)
// - Falls back to image_url if available (for placeholder images)
// - Uses empty-state placeholder if neither is available
// - Images display as squares above the item name

const MenuCard = ({ item }: { item: MenuItem }) => {
  const selectedLocation = useLocationStore((state) => state.selectedLocation);
  const { addItem } = useCartStore();
  const itemId = item.id ?? item.$id ?? "";
  
  // Get location-specific price: if Lekki is selected, use prices.Lekki, etc.
  const price = selectedLocation ? item.prices[selectedLocation] ?? 0 : 0;
  
  // Image fallback chain: local image → URL → empty state placeholder
  const imageSource = item.image
    ? item.image
    : item.image_url
    ? { uri: item.image_url }
    : require("../assets/images/empty-state.png");

  const handleAddToCart = () => {
    if (!selectedLocation) {
      Alert.alert(
        "Location required",
        "Please select a location before adding items to the cart."
      );
      return;
    }

    // Add to cart with location-based price already captured
    addItem({
      id: itemId,
      name: item.name,
      price,
      selectedLocation,
      image: imageSource,
      customizations: [],
    });
  };

  return (
    <TouchableOpacity
      className="menu-card"
      style={Platform.OS === "android" ? { elevation: 10, shadowColor: "#878787" } : {}}
    >
      <Image source={imageSource} className="size-32 absolute -top-10" resizeMode="contain" />
      <Text className="text-center base-bold text-dark-100 mb-2" numberOfLines={1}>
        {item.name}
      </Text>
      <Text className="body-regular text-gray-200 mb-4">
        {selectedLocation ? `₦${price}` : "Select location first"}
      </Text>
      <TouchableOpacity onPress={handleAddToCart}>
        <Text className="paragraph-bold text-primary">Add to Cart +</Text>
      </TouchableOpacity>
    </TouchableOpacity>
  );
};

export default MenuCard;
