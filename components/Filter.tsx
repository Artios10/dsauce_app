import { Text, FlatList, TouchableOpacity, Platform } from 'react-native';
import { useState } from 'react';
import cn from 'clsx';

const Filter = ({
  categories,
  activeCategory,
  onCategoryChange,
}: {
  categories: string[];
  activeCategory: string;
  onCategoryChange: (category: string) => void;
}) => {
  const [active, setActive] = useState(activeCategory);

  const handlePress = (category: string) => {
    setActive(category);
    onCategoryChange(category);
  };

  return (
    <FlatList
      data={categories}
      keyExtractor={(item) => item}
      horizontal
      showsHorizontalScrollIndicator={false}
      contentContainerClassName="gap-x-2 pb-3"
      renderItem={({ item }) => (
        <TouchableOpacity
          className={cn('filter', active === item ? 'bg-primary' : 'bg-white')}
          style={Platform.OS === 'android' ? { elevation: 5, shadowColor: '#878787' } : {}}
          onPress={() => handlePress(item)}
        >
          <Text className={cn('body-medium', active === item ? 'text-white' : 'text-gray-200')}>
            {item}
          </Text>
        </TouchableOpacity>
      )}
    />
  );
};

export default Filter;
