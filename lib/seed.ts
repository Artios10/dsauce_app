import { ID } from "react-native-appwrite";
import { appwriteConfig, databases, storage } from "./appwrite";
import dummyData from "./data";

interface MenuItem {
  name: string;
  description: string;
  image_url?: string;
  prices: Record<string, number>;
  category: string;
}

interface DummyData {
  categories: string[];
  menu: MenuItem[];
}

// ensure dummyData has correct shape
const data = dummyData as DummyData;

async function clearAll(collectionId: string): Promise<void> {
  const list = await databases.listDocuments(appwriteConfig.databaseId, collectionId);

  await Promise.all(
    list.documents.map((doc) =>
      databases.deleteDocument(appwriteConfig.databaseId, collectionId, doc.$id)
    )
  );
}

async function clearStorage(): Promise<void> {
  const list = await storage.listFiles(appwriteConfig.bucketId);

  await Promise.all(
    list.files.map((file) => storage.deleteFile(appwriteConfig.bucketId, file.$id))
  );
}

async function uploadImageToStorage(imageUrl: string) {
  const response = await fetch(imageUrl);
  const blob = await response.blob();

  const fileObj = {
    name: imageUrl.split("/").pop() || `file-${Date.now()}.jpg`,
    type: blob.type,
    size: blob.size,
    uri: imageUrl,
  };

  const file = await storage.createFile(appwriteConfig.bucketId, ID.unique(), fileObj);

  return storage.getFileViewURL(appwriteConfig.bucketId, file.$id);
}

async function seed(): Promise<void> {
  // 1. Clear all
  await clearAll(appwriteConfig.categoriesCollectionId);
  await clearAll(appwriteConfig.customizationsCollectionId);
  await clearAll(appwriteConfig.menuCollectionId);
  await clearAll(appwriteConfig.menuCustomizationsCollectionId);
  await clearStorage();

  // 2. Create Categories from the new menu data
  const categoryMap: Record<string, string> = {};
  const categories = Array.from(new Set(data.menu.map((item) => item.category)));

  for (const category of categories) {
    const doc = await databases.createDocument(
      appwriteConfig.databaseId,
      appwriteConfig.categoriesCollectionId,
      ID.unique(),
      {
        name: category,
        description: `${category} favorites`,
      }
    );
    categoryMap[category] = doc.$id;
  }

  // 3. Create Menu Items
  const menuMap: Record<string, string> = {};
  for (const item of data.menu) {
    const uploadUrl = item.image_url ?? "https://via.placeholder.com/720x720.png?text=Food";
    const uploadedImage = await uploadImageToStorage(uploadUrl);

    const doc = await databases.createDocument(
      appwriteConfig.databaseId,
      appwriteConfig.menuCollectionId,
      ID.unique(),
      {
        name: item.name,
        description: item.description,
        image_url: uploadedImage,
        price: item.prices["Isheri Berger"] ?? Object.values(item.prices)[0],
        rating: 4.5,
        calories: 0,
        protein: 0,
        categories: categoryMap[item.category],
      }
    );

    menuMap[item.name] = doc.$id;
  }

  console.log("✅ Seeding complete.");
}

export default seed;
