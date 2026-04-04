import { View, Text, FlatList } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useCartStore } from "@/store/cart.store";
import useLocationStore from "@/store/location.store";
import CustomHeader from "@/components/CustomHeader";
import cn from "clsx";
import CustomButton from "@/components/CustomButton";
import CartItem from "@/components/CartItem";
import { PaymentInfoStripeProps } from "@/type";

const PaymentInfoStripe = ({
  label,
  value,
  labelStyle,
  valueStyle,
}: PaymentInfoStripeProps) => (
  <View className="flex-between flex-row my-1">
    <Text className={cn("paragraph-medium text-gray-200", labelStyle)}>{label}</Text>
    <Text className={cn("paragraph-bold text-dark-100", valueStyle)}>{value}</Text>
  </View>
);

const Cart = () => {
  const { items, getTotalItems, getTotalPrice, getTotalPlatform, getTotalVendor } = useCartStore();
  const selectedLocation = useLocationStore((state) => state.selectedLocation);

  const totalItems = getTotalItems();
  const totalPrice = getTotalPrice();
  const totalPlatform = getTotalPlatform();
  const totalVendor = getTotalVendor();

  return (
    <SafeAreaView className="bg-white h-full">
      <FlatList
        data={items}
        renderItem={({ item }) => <CartItem item={item} />}
        keyExtractor={(item) => `${item.id}-${item.selectedLocation}`}
        contentContainerClassName="pb-28 px-5 pt-5"
        ListHeaderComponent={() => <CustomHeader title="Your Cart" />}
        ListEmptyComponent={() => <Text>Cart Empty</Text>}
        ListFooterComponent={() =>
          totalItems > 0 && (
            <View className="gap-5">
              <View className="mt-6 border border-gray-200 p-5 rounded-2xl">
                <Text className="h3-bold text-dark-100 mb-5">Payment Summary</Text>
                <Text className="paragraph-medium text-dark-100 mb-3">
                  Location: {selectedLocation ?? "Not selected"}
                </Text>

                <PaymentInfoStripe
                  label={`Items Subtotal (${totalItems})`}
                  value={`₦${totalPrice.toFixed(0)}`}
                />
                <PaymentInfoStripe
                  label={`Platform Fee`}
                  value={`₦${totalPlatform.toFixed(0)}`}
                />
                <PaymentInfoStripe label={`Delivery Fee`} value={`₦500`} />
                <PaymentInfoStripe
                  label={`Discount`}
                  value={`- ₦0`}
                  valueStyle="!text-success"
                />
                <View className="border-t border-gray-300 my-2" />
                <PaymentInfoStripe
                  label={`Total Paid by Customer`}
                  value={`₦${(totalPrice + 500).toFixed(0)}`}
                  labelStyle="base-bold !text-dark-100"
                  valueStyle="base-bold !text-dark-100 !text-right"
                />
                <PaymentInfoStripe
                  label={`Vendor Receives`}
                  value={`₦${totalVendor.toFixed(0)}`}
                  labelStyle="paragraph-medium text-gray-200"
                  valueStyle="paragraph-bold text-success"
                />
              </View>

              <CustomButton title="Order Now" />
            </View>
          )
        }
      />
    </SafeAreaView>
  );
};

export default Cart;
