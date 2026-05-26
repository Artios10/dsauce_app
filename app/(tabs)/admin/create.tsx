import { Alert, Switch, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useState } from "react";
import { useRouter } from "expo-router";

import CustomInput from "@/components/CustomInput";
import CustomButton from "@/components/CustomButton";
import RoleSelector from "@/components/RoleSelector";
import { createUserAdmin } from "@/lib/api";
import useAuthStore from "@/store/auth.store";

const AdminCreateUser = () => {
  const router = useRouter();
  const { user } = useAuthStore();
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

  const submit = async () => {
    if (!form.username || !form.email || !form.password) {
      return Alert.alert("Error", "Please complete all required fields.");
    }

    setIsSubmitting(true);
    try {
      await createUserAdmin({
        username: form.username,
        email: form.email,
        password: form.password,
        role: form.role,
        is_verified: form.is_verified,
        is_active: form.is_active,
        is_staff: form.is_staff,
      });
      Alert.alert("Success", "User created.");
      router.replace("/admin");
    } catch (error: any) {
      Alert.alert("Error", error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <SafeAreaView className="flex-1 bg-white">
      {user?.role !== "admin" ? (
        <View className="flex-1 items-center justify-center px-6">
          <Text className="base-semibold text-dark-100">You do not have access to this page.</Text>
        </View>
      ) : (
      <View className="px-5 py-6 gap-5">
        <Text className="h3-bold text-dark-100">Create User</Text>
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
          label="Password"
          placeholder="Enter password"
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
        <CustomButton title="Create User" isLoading={isSubmitting} onPress={submit} />
      </View>
      )}
    </SafeAreaView>
  );
};

export default AdminCreateUser;
