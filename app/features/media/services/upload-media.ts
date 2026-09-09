import { PresignedUploadRequest, PresignedUploadResponse } from "../schemas";

export async function uploadProductMedia(
  file: File,
  getPresignedUrl: ({
    filename,
    content_type,
  }: PresignedUploadRequest) => Promise<PresignedUploadResponse>,
) {
  const { url, storage_key } = await getPresignedUrl({
    filename: file.name,
    content_type: file.type as "image/jpeg" | "image/png" | "image/webp",
  });

  const response = await fetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": file.type,
    },
    body: file,
  });

  if (!response.ok) {
    throw new Error(`Failed to upload ${file.name}`);
  }

  return { storage_key };
}
