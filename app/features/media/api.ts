import { apiClient } from "@/lib/api/client";
import {
  PresignedDownloadRequest,
  presignedDownloadResponseSchema,
  PresignedUploadRequest,
  presignedUploadResponseSchema,
} from "./schemas";

export async function createUploadMediaPresignedURL(
  data: PresignedUploadRequest,
) {
  const response = await apiClient<unknown>(`/media/upload-url`, {
    method: "POST",
    body: JSON.stringify(data),
  });

  return presignedUploadResponseSchema.parse(response);
}

export async function createDownloadMediaPresignedURL(
  data: PresignedDownloadRequest,
) {
  const response = await apiClient<unknown>(`/media/download-url`, {
    method: "POST",
    body: JSON.stringify(data),
  });

  return presignedDownloadResponseSchema.parse(response);
}
