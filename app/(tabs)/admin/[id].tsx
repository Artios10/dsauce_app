import { Alert, Switch, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useEffect, useState } from "react";
import { useLocalSearchParams, useRouter } from "expo-router";

import CustomInput from "@/components/CustomInput";
import CustomButton from "@/components/CustomButton";
import RoleSelector from "@/components/RoleSelector";
import { deleteUser, getUser, updateUser } from "@/lib/api";
import useAuthStore from "@/store/auth.store";

const AdminEditUser = () => {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const userId = Number(id);
  const { user } = useAuthStore();
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    role: "customer",
    is_verified: false,
    is_active: true,
    is_staff: false,
  });

  useEffect(() => {
    const loadUser = async () => {
      try {
        const data = await getUser(userId);
        setForm({
          username: data.username,
          email: data.email,
          password: "",
          role: data.role,
          is_verified: data.is_verified,
          is_active: data.is_active ?? true,
          is_staff: data.is_staff ?? false,
        });
      } catch (error: any) {
        Alert.alert("Error", error.message);
      } finally {
        setIsLoading(false);
      }
    };

    if (Number.isNaN(userId)) {
      Alert.alert("Error", "Invalid user id.");
      router.replace("/admin");
      return;
    }

    if (user?.role !== "admin") {
      setIsLoading(false);
      return;
    }

    loadUser();
  }, [router, user?.role, userId]);

  const submit = async () => {
    if (!form.username || !form.email) {
      return Alert.alert("Error", "Username and email are required.");
    }

    setIsSubmitting(true);
    try {
      await updateUser(userId, {
        username: form.username,
        email: form.email,
        role: form.role,
        is_verified: form.is_verified,
        is_active: form.is_active,
        is_staff: form.is_staff,
        ...(form.password ? { password: form.password } : {}),
      });
      Alert.alert("Success", "User updated.");
      router.replace("/admin");
    } catch (error: any) {
      Alert.alert("Error", error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = () => {
    Alert.alert("Delete user", "Are you sure you want to delete this user?", [
      { text: "Cancel", style: "cancel" },
      {
        text: "Delete",
        style: "destructive",
        onPress: async () => {
          try {
            await deleteUser(userId);
            router.replace("/admin");
          } catch (error: any) {
            Alert.alert("Error", error.message);
          }
        },
      },
    ]);
  };

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 bg-white">
        <View className="flex-1 items-center justify-center">
          <Text className="body-regular text-gray-500">Loading user...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-white">
      {user?.role !== "admin" ? (
        <View className="flex-1 items-center justify-center px-6">
          <Text className="base-semibold text-dark-100">You do not have access to this page.</Text>
        </View>
      ) : (
        <View className="px-5 py-6 gap-5">
          <Text className="h3-bold text-dark-100">Edit User</Text>
          <CustomInput
            label="Username"
            placeholder="Enter username"
            value={form.username}
            onChangeText={(text) => setForm((prev) => ({ ...prev, username: text }))}
          />
          <CustomInput
            label="Email"
            placeholder="Enter email"
            value={form.email}
            onChangeText={(text) => setForm((prev) => ({ ...prev, email: text }))}
            keyboardType="email-address"
          />
          <CustomInput
            label="Password (optional)"
            placeholder="Enter new password"
            value={form.password}
            onChangeText={(text) => setForm((prev) => ({ ...prev, password: text }))}
            secureTextEntry
          />
          <RoleSelector
            label="Role"
            value={form.role}
            options={[
              { label: "Customer", value: "customer" },
              { label: "Merchant", value: "merchant" },
              { label: "Admin", value: "admin" },
            ]}
            onChange={(value) => setForm((prev) => ({ ...prev, role: value }))}
          />
          <View className="flex-row items-center justify-between">
            <Text className="paragraph-medium text-dark-100">Verified</Text>
            <Switch
              value={form.is_verified}
              onValueChange={(value) => setForm((prev) => ({ ...prev, is_verified: value }))}
            />
          </View>
          <View className="flex-row items-center justify-between">
            <Text className="paragraph-medium text-dark-100">Active</Text>
            <Switch
              value={form.is_active}
              onValueChange={(value) => setForm((prev) => ({ ...prev, is_active: value }))}
            />
          </View>
          <View className="flex-row items-center justify-between">
            <Text className="paragraph-medium text-dark-100">Staff</Text>
            <Switch
              value={form.is_staff}
              onValueChange={(value) => setForm((prev) => ({ ...prev, is_staff: value }))}
            />
          </View>
          <CustomButton title="Save Changes" isLoading={isSubmitting} onPress={submit} />
          <CustomButton title="Delete User" style="bg-error" onPress={handleDelete} />
        </View>
      )}
    </SafeAreaView>
  );
};

export default AdminEditUser;
