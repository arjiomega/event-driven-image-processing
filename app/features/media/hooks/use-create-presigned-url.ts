import { useMutation } from "@tanstack/react-query";
import { createUploadMediaPresignedURL } from "../api";
import { PresignedUploadRequest } from "../schemas";

type CreateProductMediaPresignedURLVariables = {
  data: PresignedUploadRequest;
};

export function useCreateProductMediaPresignedURL() {
  return useMutation({
    mutationFn: ({ data }: CreateProductMediaPresignedURLVariables) => {
      return createUploadMediaPresignedURL(data);
    },

    retry: 2,
  });
}
