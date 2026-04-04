import { Alert, Image, Text, TouchableOpacity, Platform } from "react-native";
import { MenuItem } from "@/type";
import { useCartStore } from "@/store/cart.store";
import useLocationStore from "@/store/location.store";

const MenuCard = ({ item }: { item: MenuItem }) => {
  const selectedLocation = useLocationStore((state) => state.selectedLocation);
  const { addItem } = useCartStore();
  const itemId = item.id ?? item.$id ?? "";
  const price = selectedLocation ? item.prices[selectedLocation] ?? 0 : 0;
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
