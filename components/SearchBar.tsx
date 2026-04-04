import { images } from "@/constants";
import { Image, TextInput, TouchableOpacity, View } from "react-native";

const SearchBar = ({
  query,
  onChangeQuery,
}: {
  query: string;
  onChangeQuery: (text: string) => void;
}) => {
  return (
    <View className="searchbar">
      <TextInput
        className="flex-1 p-5"
        placeholder="Search for shawarma, rice, grills..."
        value={query}
        onChangeText={onChangeQuery}
        placeholderTextColor="#A0A0A0"
        returnKeyType="search"
      />
      <TouchableOpacity className="pr-5" onPress={() => onChangeQuery(query)}>
        <Image
          source={images.search}
          className="size-6"
          resizeMode="contain"
          tintColor="#5D5F6D"
        />
      </TouchableOpacity>
    </View>
  );
};

export default SearchBar;
