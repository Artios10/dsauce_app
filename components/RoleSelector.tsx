import { Pressable, Text, View } from "react-native";
import cn from "clsx";

type RoleOption = {
  label: string;
  value: string;
};

type RoleSelectorProps = {
  label: string;
  value: string;
  options: RoleOption[];
  onChange: (value: string) => void;
};

const RoleSelector = ({ label, value, options, onChange }: RoleSelectorProps) => (
  <View className="w-full">
    <Text className="label">{label}</Text>
    <View className="flex-row flex-wrap gap-2 mt-2">
      {options.map((option) => {
        const isActive = option.value === value;
        return (
          <Pressable
            key={option.value}
            onPress={() => onChange(option.value)}
            className={cn(
              "px-4 py-2 rounded-full border",
              isActive ? "bg-primary border-primary" : "bg-white border-gray-300"
            )}
          >
            <Text className={cn("body-regular", isActive ? "text-white" : "text-dark-100")}>
              {option.label}
            </Text>
          </Pressable>
        );
      })}
    </View>
  </View>
);

export default RoleSelector;
