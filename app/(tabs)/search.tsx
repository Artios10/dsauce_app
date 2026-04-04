import { FlatList, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useMemo, useState } from "react";
import CartButton from "@/components/CartButton";
import cn from "clsx";
import MenuCard from "@/components/MenuCard";
import LocationSelector from "@/components/LocationSelector";
import Filter from "@/components/Filter";
import SearchBar from "@/components/SearchBar";
import useLocationStore from "@/store/location.store";
import { MENU_CATEGORIES, MENU_ITEMS } from "@/lib/data";
import { MenuItem } from "@/type";

const Search = () => {
  const selectedLocation = useLocationStore((state) => state.selectedLocation);
  const [query, setQuery] = useState("");
  const [activeCategory, setActiveCategory] = useState("All");

  const categories = ["All", ...MENU_CATEGORIES];

  const filteredData = useMemo(() => {
    return MENU_ITEMS.filter((item) => {
      const matchesCategory = activeCategory === "All" || item.category === activeCategory;
      const matchesQuery = item.name.toLowerCase().includes(query.toLowerCase());
      return matchesCategory && matchesQuery;
    });
  }, [activeCategory, query]);

  return (
    <SafeAreaView className="bg-white h-full">
      <FlatList
        data={filteredData}
        renderItem={({ item, index }) => {
          const isFirstRightColItem = index % 2 === 0;

          return (
            <View className={cn("flex-1 max-w-[48%]", !isFirstRightColItem ? "mt-10" : "mt-0")}>
              <MenuCard item={item as MenuItem} />
            </View>
          );
        }}
        keyExtractor={(item) => item.id}
        numColumns={2}
        columnWrapperClassName="gap-7"
        contentContainerClassName="gap-7 px-5 pb-32"
        ListHeaderComponent={() => (
          <View className="my-5 gap-5">
            <View className="flex-between flex-row w-full">
              <View className="flex-start">
                <Text className="small-bold uppercase text-primary">Search</Text>
                <View className="flex-start flex-row gap-x-1 mt-0.5">
                  <Text className="paragraph-semibold text-dark-100">Find your favorite food</Text>
                </View>
                <View className="mt-4">
                  <LocationSelector />
                  {!selectedLocation && (
                    <Text className="text-error body-regular mt-2">
                      Please select a location before ordering.
                    </Text>
                  )}
                </View>
              </View>

              <CartButton />
            </View>

            <SearchBar query={query} onChangeQuery={setQuery} />
            <Filter categories={categories} activeCategory={activeCategory} onCategoryChange={setActiveCategory} />
          </View>
        )}
        ListEmptyComponent={() => filteredData.length === 0 && <Text>No results</Text>}
      />
    </SafeAreaView>
  );
};

export default Search;
