import { Alert, FlatList, Pressable, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useCallback, useEffect, useState } from "react";
import { useRouter } from "expo-router";

import { deleteUser, getUsers } from "@/lib/api";
import { User } from "@/type";
import useAuthStore from "@/store/auth.store";
import CustomButton from "@/components/CustomButton";

const AdminUsers = () => {
  const router = useRouter();
  const { user } = useAuthStore();
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const loadUsers = useCallback(async () => {
    try {
      const data = await getUsers();
      setUsers(data);
    } catch (error: any) {
      Alert.alert("Error", error.message);
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    if (user?.role !== "admin") {
      setIsLoading(false);
      return;
    }
    loadUsers();
  }, [loadUsers, user?.role]);

  const handleDelete = (id: number) => {
    Alert.alert("Delete user", "Are you sure you want to delete this user?", [
      { text: "Cancel", style: "cancel" },
      {
        text: "Delete",
        style: "destructive",
        onPress: async () => {
          try {
            await deleteUser(id);
            await loadUsers();
          } catch (error: any) {
            Alert.alert("Error", error.message);
          }
        },
      },
    ]);
  };

  if (user?.role !== "admin") {
    return (
      <SafeAreaView className="flex-1 bg-white">
        <View className="flex-1 items-center justify-center px-6">
          <Text className="base-semibold text-dark-100">You do not have access to this page.</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-white">
      <FlatList
        data={users}
        keyExtractor={(item) => item.id.toString()}
        onRefresh={() => {
          setIsRefreshing(true);
          loadUsers();
        }}
        refreshing={isRefreshing}
        contentContainerClassName="px-5 pb-32"
        ListHeaderComponent={() => (
          <View className="my-5 gap-4">
            <Text className="h3-bold text-dark-100">User Management</Text>
            <CustomButton title="Create User" onPress={() => router.push("/admin/create")} />
          </View>
        )}
        ListEmptyComponent={() =>
          !isLoading ? <Text className="body-regular text-gray-500">No users found.</Text> : null
        }
        renderItem={({ item }) => (
          <View className="bg-white rounded-2xl shadow-md shadow-black/10 p-4 mb-4">
            <Text className="paragraph-semibold text-dark-100">{item.username}</Text>
            <Text className="body-regular text-gray-500">{item.email}</Text>
            <Text className="body-medium text-primary capitalize mt-1">{item.role}</Text>
            <View className="flex-row gap-3 mt-4">
              <Pressable
                className="px-4 py-2 rounded-full bg-primary"
                onPress={() => router.push(`/admin/${item.id}`)}
              >
                <Text className="text-white paragraph-semibold">Manage</Text>
              </Pressable>
              <Pressable
                className="px-4 py-2 rounded-full border border-error"
                onPress={() => handleDelete(item.id)}
              >
                <Text className="text-error paragraph-semibold">Delete</Text>
              </Pressable>
            </View>
          </View>
        )}
      />
    </SafeAreaView>
  );
};

export default AdminUsers;
