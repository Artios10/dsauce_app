import { SafeAreaView } from "react-native-safe-area-context";
import { FlatList, Image, Pressable, Text, View } from "react-native";
import { Fragment } from "react";
import cn from "clsx";

import CartButton from "@/components/CartButton";
import LocationSelector from "@/components/LocationSelector";
import { images, CATEGORIES } from "@/constants";
import useLocationStore from "@/store/location.store";

export default function Index() {
  const selectedLocation = useLocationStore((state) => state.selectedLocation);

  return (
    <SafeAreaView className="flex-1 bg-white">
      <FlatList
        data={CATEGORIES.slice(1)}
        renderItem={({ item, index }) => {
          const isEven = index % 2 === 0;

          return (
            <View>
              <Pressable
                className={cn("offer-card", isEven ? "flex-row-reverse" : "flex-row")}
                style={{ backgroundColor: "#D33B0D" }}
                android_ripple={{ color: "#fffff22" }}
              >
                {({ pressed }) => (
                  <Fragment>
                    <View className={"h-full w-1/2"}>
                      <Image source={images.emptyState} className={"size-full"} resizeMode={"contain"} />
                    </View>

                    <View className={cn("offer-card__info", isEven ? "pl-10" : "pr-10")}>
                      <Text className="h1-bold text-white leading-tight">{item.name}</Text>
                      <Image
                        source={images.arrowRight}
                        className="size-10"
                        resizeMode="contain"
                        tintColor="#ffffff"
                      />
                    </View>
                  </Fragment>
                )}
              </Pressable>
            </View>
          );
        }}
        contentContainerClassName="pb-28 px-5"
        ListHeaderComponent={() => (
          <View className="flex-between flex-row w-full my-5">
            <View className="flex-start">
              <Text className="small-bold text-primary">DELIVER TO</Text>
              <LocationSelector />
              {!selectedLocation && (
                <Text className="text-error body-regular mt-2">
                  Please select a location before ordering.
                </Text>
              )}
            </View>

            <CartButton />
          </View>
        )}
      />
    </SafeAreaView>
  );
}
