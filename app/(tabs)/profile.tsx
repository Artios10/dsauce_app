import { Image, ScrollView, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import CustomButton from "@/components/CustomButton";
import { images } from "@/constants";
import useAuthStore from "@/store/auth.store";

const Profile = () => {
  const { user, signOut } = useAuthStore();

  const username = user?.username || "User";
  const role = user?.role ? user.role.replaceAll("_", " ") : "normal user";
  const bio = user?.bio || "No bio yet";

  return (
    <SafeAreaView className="flex-1 bg-white">
      <ScrollView contentContainerClassName="px-5 pb-32 pt-5">
        <View className="items-center gap-4 mb-8">
          <Image
            source={images.avatar}
            className="profile-avatar"
            resizeMode="cover"
          />
          <View className="items-center gap-1">
            <Text className="h3-bold text-dark-100 capitalize">{username}</Text>
            <Text className="body-regular text-gray-500 capitalize">{role}</Text>
          </View>
        </View>

        <View className="bg-white rounded-2xl shadow-md shadow-black/10 p-4 mb-6">
          <View className="profile-field">
            <View className="profile-field__icon">
              <Image source={images.envelope} className="size-5" resizeMode="contain" tintColor="#D33B0D" />
            </View>
            <View className="flex-1">
              <Text className="small-bold text-gray-400 uppercase">Email</Text>
              <Text className="paragraph-semibold text-dark-100">{user?.email || "—"}</Text>
            </View>
          </View>

          <View className="profile-field mb-0">
            <View className="profile-field__icon">
              <Image source={images.pencil} className="size-5" resizeMode="contain" tintColor="#D33B0D" />
            </View>
            <View className="flex-1">
              <Text className="small-bold text-gray-400 uppercase">Bio</Text>
              <Text className="paragraph-medium text-dark-100">{bio}</Text>
            </View>
          </View>
        </View>

        <CustomButton
          title="Sign Out"
          style="bg-dark-100"
          leftIcon={<Image source={images.logout} className="size-5 mr-2" resizeMode="contain" tintColor="#fff" />}
          onPress={signOut}
        />
      </ScrollView>
    </SafeAreaView>
  );
};

export default Profile
