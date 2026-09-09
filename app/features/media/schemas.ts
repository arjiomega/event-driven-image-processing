import { z } from "zod";

export const presignedUploadRequestSchema = z.object({
  filename: z.string(),
  content_type: z.enum(["image/jpeg", "image/png", "image/webp"]),
});

export const presignedUploadResponseSchema = z.object({
  url: z.url(),
  storage_key: z.string(),
});

export const presignedDownloadRequestSchema = z.object({
  filename: z.string(),
});

export const presignedDownloadResponseSchema = z.object({
  url: z.url(),
});

export type PresignedUploadRequest = z.infer<
  typeof presignedUploadRequestSchema
>;

export type PresignedUploadResponse = z.infer<
  typeof presignedUploadResponseSchema
>;

export type PresignedDownloadRequest = z.infer<
  typeof presignedDownloadRequestSchema
>;

export type PresignedDownloadResponse = z.infer<
  typeof presignedDownloadResponseSchema
>;
