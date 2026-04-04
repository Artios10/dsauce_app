import { useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  Modal,
  Pressable,
  Image,
} from "react-native";
import { images } from "@/constants";
import useLocationStore, { LOCATIONS } from "@/store/location.store";

// 🔴 START: Location selector component
// Description: Presents a modal location picker and stores the selected location globally.
const LocationSelector = () => {
  const selectedLocation = useLocationStore((state) => state.selectedLocation);
  const setLocation = useLocationStore((state) => state.setLocation);
  const [open, setOpen] = useState(false);

  const handleSelect = (location: string) => {
    setLocation(location as any);
    setOpen(false);
  };

  return (
    <>
      <TouchableOpacity
        className="flex-row items-center gap-x-2"
        onPress={() => setOpen(true)}
      >
        <Image
          source={images.location}
          className="size-4"
          resizeMode="contain"
          tintColor="#FF3B30"
        />
        <Text
          className={`body-semibold ${selectedLocation ? 'text-dark-100' : 'text-error'}`}
        >
          {selectedLocation ?? "Select location"}
        </Text>
      </TouchableOpacity>

      <Modal visible={open} transparent animationType="fade">
        <Pressable
          className="flex-1 justify-end bg-black/40"
          onPress={() => setOpen(false)}
        >
          <View className="bg-white rounded-t-3xl p-5">
            <Text className="h3-bold text-dark-100 mb-4">
              Choose your location
            </Text>

            {LOCATIONS.map((location) => (
              <TouchableOpacity
                key={location}
                className="py-4 px-4 rounded-2xl mb-3 bg-red-50"
                onPress={() => handleSelect(location)}
              >
                <Text className="base-semibold text-dark-100">
                  {location}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </Pressable>
      </Modal>
    </>
  );
};

export default LocationSelector;
// 🔴 END: Location selector component
